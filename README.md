blender-cnt
===============================

Blender add-on to create (n, m) chirality CNT and Graphene.

Quick Start
===========

## Installation

1. Download the script.
2. Install the script into Blender, and activate:
  
  **File >> User Preferences >> Add-Ons >> install from file** (Make sure you **enable** it by checking the box).

  ![Enable Blender-CNT addon](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/addons.png)

## Usage

To use the add-on: In **Object Mode** press the spacebar to bring up the search box. Search for **"cnt"**, and click on **Create CNT**.

![Search for Blender-CNT addon](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/find_cnt.png)

By default, this will render an unwrapped, a.k.a. graphene, (5,5) CNT:

![Graphene default operator](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/graphene_operator.png)

To transition to a wrapped CNT, slide the wrapping factor from 0 to 1:

![CNT operator](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/semiwrapped_operator.png)
![CNT operator](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/cnt_operator.png)

The **Create CNT** panel also includes other options that allow you to update the CNT in real-time:

* **wrap:** the wrapping factor of the CNT (0=graphene, 1=CNT)
* **m:** index of Graphene/CNT cell
* **n:** index of Graphene/CNT cell
* **Nx:** count of the x-array modifier
* **Ny:** count of the y-array modifier
* **C-C bond length**
* **C atom radius**
* **C-C bond radius**

## Properties

Once the **Create CNT** operator panel closes, you will not be able to reopen the panel for further modification of the CNT. However, most of the properties can be modified in alternative ways.

### Array Modifiers
The **Nx** and **Ny** properties allow the lattice to be extended along the x or y directions using **array modifiers**. Once the operator panel is closed, these properties can be changed by going to the **Modifier** tab and adjusting the **count**.

![CNT array modifier](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/array.png)

### Atom Size
The **C atom radius** property allows the atom to be resized using scaling. Once the operator panel is closed, this property can be changed by clicking on the **atom** object and modifying the **scale** in the **Object** tab.

![Atom resizing](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/atoms.png)

### Bond Size
The **C-C bond radius** property allows the bond radius to be resized using the `bezier-curve` depth factor. Once the operator panel is closed, this property can be changed by clicking on the **bonds** object and modifying the **depth** parameter in the **Data** tab.

![Bond resizing](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/bonds.png)

License
=======

The script is under GPL 2.0, to comply with Blenders license (https://www.blender.org/support/faq/). 
The generated images are not under any license; however, they do require an acknowledgement (See the NOTICE file for more details).

Support
=======

If you have a question, a suggestion or find a bug, enter a ticket at: https://github.com/bcorso/blender-cnt/issues/new
