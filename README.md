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

By default, this will render a (m=5, n=5) graphene sheet:

![Graphene default operator](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/graphene_operator.png)

The **Create CNT** panel includes options to update the object in real-time:

* **Type:** (Graphene or CNT)
* **m:** index of Graphene/CNT cell
* **n:** index of Graphene/CNT cell
* **C-C bond length**
* **C atom radius**
* **C-C bond radius**

For example, switching the type to **CNT** will immediately render the CNT on the screen.

![CNT operator](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/cnt_operator.png)

The previous actions have been applied to a **single (m, n) cell** of the lattice. However, the lattice can be extended to include multiple cells by using an **array modifier**. The array modifiers are automatically setup during creation, and can be changed by going to the **Modifier** tab and increasing the **count**.

![CNT array modifier](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/array.png)

Finally, one has the ability to separately modify the atoms and bonds because they are created as separate objects. As an example, the atoms can be resized by clicking on the **atom** object and modifying the **scale** of the atom in the **Object** tab.

![Atom resizing](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/atoms.png)

Likewise, the bonds can be resized by clicking on the **bonds** object and modifying the **depth** parameter in the **Data** tab.

![Bond resizing](https://raw.githubusercontent.com/wiki/bcorso/blender-cnt/images/bonds.png)

License
=======

GPL 2.0 with an acknowledgement required to accompany the images generated.
See the NOTICE file for more details.

Support
=======

If you have a question, a suggestion or find a bug, enter a ticket at: https://github.com/bcorso/blender-cnt/issues/new
