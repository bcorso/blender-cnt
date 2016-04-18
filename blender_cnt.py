'''
Copyright (c) 2016 Brad Corso. All rights reserved.
https://github.com/bcorso/blender-cnt
The Blender-CNT software is licensed under GPL 2.0.
Images generated with Blender-CNT require an acknowledgment.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this library; if not, write to the
Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
Boston, MA  02110-1301, USA.

When you publish or redistribute any image created with Blender-CNT or any Blender-CNT
derivative work, you must accompany this image with the following acknowledgment:
  
  Generated with Blender-CNT (https://github.com/bcorso/blender-cnt).
'''

import numpy as np
from fractions import gcd
from math import cos, sin, acos, atan2, sqrt, copysign, pi

class Lattice:
    ''' 
    Defines a 2D lattice in terms of its unit vectors (a1, a2) 
    and atom positions (xList) internal to the unit cell.
    '''
    def __init__(self, a1, a2, xList):
        # Lattice vectors
        self.a1 = a1;
        self.a2 = a2;
        # Atom-Atom vectors in unit cell
        self.xList  = xList;

    def pos(self, i, j, k=None):
        ''' 
        returns the 2D point for the lattice given indices i, j
        if k is supplied, returns the atom position at i, j.
        '''
        return (i*self.a1) + (j*self.a2) + (0 if k == None else self.xList[k])

class LatticeCell:
    '''  Defines a 2D lattice cell given indices m, n '''
    def __init__(self, lattice, m, n):
        self.lattice = lattice
        self.m = m
        self.n = n

        # Chiral vector
        self.c = lattice.pos(m,n)
        self.magC = mag(self.c)
        # Translation vector 
        d = gcd(2*n+m,2*m+n)
        self.t = lattice.pos((2*n+m)/d, -(2*m+n)/d);
        self.magT = mag(self.t)
        # Chiral rotation matrix (rotate a1 along x-axis)
        self.theta = acos(norm(self.c)[0]*copysign(1, self.c[1]))
        self.rotM = np.array([
                [cos(self.theta), sin(self.theta)],
                [-sin(self.theta), cos(self.theta)]]).T

        # Calculate atoms and bonds in unit cell
        self._boundsErr = mag(lattice.pos(0,0,0) - lattice.pos(0,0,1))
        self.indices = self._calcIndices(m, n)
        self.atoms = self._calcAtoms(self.indices)
        self.bonds = self._calcBonds(self.indices)

    def pos(self, i, j, k):
        ''' 
        returns the 2D point in unit cell for the lattice indices 
        i, j, and atom k 
        '''
        # rotate by rotation matrix
        return np.dot(self.lattice.pos(i, j, k), self.rotM)

    def _calcIndices(self, m, n):
        ''' returns the i,j,k indices contained in the unit cell '''
        imin = 0
        imax = 2*(n+m); 
        jmin = -(2*m+n)
        jmax = n; 
        return [[i,j,k] for i in range(imin,imax+1) 
                        for j in range(jmin,jmax+1) 
                        for k in range(2) 
                        if self._isPosInCell(self.pos(i,j,k))]

    def _isPosInCell(self, p):
        ''' 
        returns true if p is in the unit cell bounds (plus/minus some error) 
        '''
        return (p[0] >= 0 - self._boundsErr/5
            and p[0] <= self.magC - self._boundsErr/5
            and p[1] >= 0 + self._boundsErr/10
            and p[1] <= self.magT + self._boundsErr/10)

    def _calcAtoms(self, indices):
        ''' returns the 2D lattice position as a list of points '''
        return [self.pos(*index) for index in indices]

    def _calcBonds(self, indices):
        ''' 
        returns the 2D lattice bonds as a list of pairs of points [p1, p2] 
        '''
        indices2D = [(i, j) for (i, j, k) in indices if k == 0]
        bonds = []
        for (i, j) in indices2D:
            p0 = self.pos(i  , j  , 0)
            p1 = self.pos(i  , j  , 1)
            p2 = self.pos(i-1, j  , 1)
            p3 = self.pos(i  , j-1, 1)
            
            if self._isBondInCell(p1):
                bonds.append([p0, p1])
            if self._isBondInCell(p2):
                bonds.append([p0, p2])
            if self._isBondInCell(p3):
                bonds.append([p0, p3])
        return bonds

    def _isBondInCell(self, p):
        ''' returns true if p is in the unit cell bounds (plus/minus some error) '''
        return (p[0] >= 0 - self._boundsErr
            and p[0] <= self.magC + self._boundsErr
            and p[1] >= 0 - self._boundsErr
            and p[1] <= self.magT + self._boundsErr)

class Graphene:
    v1 = np.array([sqrt(3.0)/2.0, 1.0/2.0])
    v2 = np.array([sqrt(3.0)/2.0, -1.0/2.0])

    ''' Defines the points in a graphene unit cell '''
    def __init__(self, bL, m, n):
        self.bL = bL
        # graphene lattice vectors
        a1 = bL * self.v1
        a2 = bL * self.v2  

        # graphene atom vectors
        ccAtoms = np.array([      
            1.0/3.0 * (a1 + a2),
            2.0/3.0 * (a1 + a2)])

        # Define the graphene lattice
        self.lattice = Lattice(a1, a2, ccAtoms)

        self.cell = LatticeCell(self.lattice, m, n)
        self.atoms = [self.to3D(p) for p in self.cell.atoms]
        self.bonds = [(self.to3D(b[0]), self.to3D(b[1])) for b in self.cell.bonds]
        self.translation = (self.cell.magC, self.cell.magT, 0)

    def to3D(self, p):
        return np.array([p[0], p[1], 0])

class CNT:
    ''' Defines the points in a CNT wrapped by wrapFactor '''
    def __init__(self, bL, m, n, wrapFactor):
        # Create graphene
        graphene = Graphene(bL, m, n)
        self.cell = graphene.cell

        # Cell radius
        self.r = self.cell.magC / (2.0*pi)

        # Cell max radius
        self.x0 = min(min(p1[0],p2[0]) for p1,p2 in graphene.bonds)
        self.xf = max(max(p1[0],p2[0]) for p1,p2 in graphene.bonds)
        self.dr = 1.01*(self.xf - self.x0)/(2.0*pi)

        # Calculate atom and bond positions for wrapped CNT
        wrapFactor = wrapFactor * (self.dr / self.r)
        self.atoms = [self.wrap(p, wrapFactor) for p in self.cell.atoms]
        self.bonds = [(self.wrap(b[0], wrapFactor), 
                       self.wrap(b[1], wrapFactor)) for b in self.cell.bonds]

        self.translation = (self.cell.magC, self.cell.magT, 0)

    def wrap(self, p, wrapFactor):
        ''' 
        return position of CNT atom w.r.t. the graphene atom.
        @param p           : atom position in unwraped graphene
        @param wrapFactor : frational wrapping factor [0,1]
        '''
        x1 = p[0]
        theta = (x1 - self.x0)/self.dr - pi/2.0
        r1 = self.r * sqrt(2.0 + 2.0*sin(theta))

        # wrapped polar coordinates
        r = (r1 - x1)*wrapFactor + x1
        t = wrapFactor*atan2(1+sin(theta), cos(theta))

        return np.array([r*cos(t), p[1], r*sin(t)])

def mag(v):
    return np.sqrt(v.dot(v))

def norm(v):
    return v / mag(v)

''' 
Blender Operator Definition
================================= 
'''

import bpy

bl_info = {
    "name": "Create CNT",
    "category": "Object"
}

# registering and menu integration
def register():
    bpy.utils.register_class(BlenderCNTDialog)
 
# unregistering and removing menus
def unregister():
    bpy.utils.unregister_class(BlenderCNTDialog)

class BlenderCNTDialog(bpy.types.Operator):
    bl_idname = "object.blender_cnt"
    bl_label = "Create CNT"
    bl_options = {'REGISTER', 'UNDO'}
    
    gtype = bpy.props.EnumProperty(
                name="Type",
                items=(('CNT', "CNT", ""),),
                default='CNT')
    wrap = bpy.props.FloatProperty(name="Wrap factor", default=0, min=0, max=1)
    index_m = bpy.props.IntProperty(name="m", default=5, min=1)
    index_n = bpy.props.IntProperty(name="n", default=5, min=1)
    count_x = bpy.props.IntProperty(name="Nx", default=1, min=1)
    count_y = bpy.props.IntProperty(name="Ny", default=1, min=1)
    bL = bpy.props.FloatProperty(name="C-C Bond Length", default=.246, step=.246)
    bR = bpy.props.FloatProperty(name="C-C Bond Radius", default=.01, step=1)
    aR = bpy.props.FloatProperty(name="C Atom Radius", default=.04, step=1)
    
    def execute(self, context):
        if self.gtype == 'CNT':
            cnt = CNT(self.bL, self.index_m, self.index_n, self.wrap)
            count = (self.count_x, self.count_y)
            self.render(cnt.atoms, cnt.bonds, self.aR, self.bR, cnt.translation, count)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="CNT Properties")
        col.prop(self, "wrap")
        row = col.row()
        row.prop(self, "index_m")
        row.prop(self, "index_n")
        row = col.row()
        row.prop(self, "count_x")
        row.prop(self, "count_y")
        col.prop(self, "bL")
        col.prop(self, "bR")
        col.prop(self, "aR")

    def render(self, atoms, bonds, atomR, bondR, delta, count):
        import bmesh, bpy_extras
        # Generate mesh point for each atom
        mesh = bpy.data.meshes.new("Atoms")
        bm = bmesh.new()

        atom0 = atoms[0]
        for atom in atoms:
            bm.verts.new(atom - atom0)

        bm.to_mesh(mesh) 
        mesh.update()
        bpy_extras.object_utils.object_data_add(bpy.context, mesh)
        self.addArrayModifier(delta, count)
        points = bpy.context.object

        # Generate sphere to be used as atom
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.mesh.primitive_uv_sphere_add()
        bpy.ops.object.shade_smooth()
        sphere = bpy.context.object
        sphere.name = "Atom"
        sphere.scale = (atomR, atomR, atomR)
        sphere.location = (0,0,0)

        # Duplicate sphere for each mesh point because
        # creating individual spheres is very slow
        sphere.parent = points
        points.dupli_type = "VERTS"

        # Create bezier curve to represent bond
        bpy.ops.curve.primitive_bezier_curve_add()
        curve = bpy.context.object
        curve.name = "Bonds"
        curve.data.name = "Bonds"
        curve.data.dimensions = '3D'
        curve.data.fill_mode = 'FULL'
        curve.data.bevel_depth = bondR
        curve.data.bevel_resolution = 1

        c_splines = curve.data.splines
        c_splines.remove(c_splines[0])

        # For each bond, extend the bezier curve
        for p1, p2 in bonds:
            spline = c_splines.new('BEZIER')
            spline.bezier_points[0].co = p1 - atom0
            spline.bezier_points[0].handle_left_type = 'VECTOR'
            spline.bezier_points[0].handle_right_type = 'VECTOR'

            spline.bezier_points.add(1)
            spline.bezier_points[1].co = p2 - atom0
            spline.bezier_points[1].handle_left_type = 'VECTOR'
            spline.bezier_points[1].handle_right_type = 'VECTOR'

        self.addArrayModifier(delta, count)

    def addArrayModifier(self, delta, count):
        ''' Adds an "Array Modifier" to the object by offset "delta" '''
        for (i, d) in enumerate(delta):
            if d > 0:
                name = 'Array.' + str(i)
                bpy.ops.object.modifier_add(type='ARRAY')
                bpy.context.active_object.modifiers['Array'].name = name
                bpy.context.active_object.modifiers[name].count=count[i]
                bpy.context.active_object.modifiers[name].use_relative_offset=False
                bpy.context.active_object.modifiers[name].use_constant_offset=True
                bpy.context.active_object.modifiers[name].constant_offset_displace[i] = d

if __name__ == "__main__":
    register()
