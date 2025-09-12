# Lichi's Cleanup Tools

A Blender addon that automates tedious tasks that ive found made my work very slow.
Mainly coded by ai :C , i dont like that but it works for me and it might help someone else so.
Im actually not sure if some stuff optimizes the blender file or exported 3d model, but it does make it prettier and easier to work with

## Installation/Usage

Just like any Regular Blender addon, download the Release and install the .zip
Tested under 4.5 but im pretty sure anything above 4.2 or even earlier should work

To use it find the panel in 3D Viewport sidebar (toggle this with N by default) its called "Lichi's Tools"

Check  the "Only Selected Objects" checkbox to limit functionality to your current selection, or leave unchecked to apply to all objects in the scene (not reccomended, it might be buggy if you hav very complex stuff).

## Features / Things on the app

### Material Tools
- **Remove Unused Materials**: Removes material slots from objects where the material isn't actually used by any parts of the mesh, useful when you separate and join stuff since it often leaves materials
- **Assign Clone Materials to Original**: Finds duplicate materials (Material.001, Material.002, etc.) and reassigns them to use the original material instead, this of course requires proper material names, make sure that you "clone" materials are actually the same and not different stuff before running

### Mesh Tools
- **Rename Mesh to Object Name**: Changes mesh data names to match their parent object names, this is pretty usless, but it makes my eyes happy

### UV Tools
- **Rename UV Map**: Rename UV maps by index. Set the index (0-n) and new name, then apply to selected or all objects. for example, an index of 0 will replace the first UVs name to whatever you set, very useful when you join geometry so UVs join properly

### Other Tools
- **Clear Orphan Data**: Removes all unused data blocks from the file, This already exists but its hard to reach so i put it here

## Warning

Always save your work before running this. While these operations can usually be undone, it's better to be safe. 
This is especially important since its Ai slop. Dont get me wrong ive tested it and used it on my projects and havent encountered anything, but as a data hoarder, you should always backup things.
