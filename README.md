# Lichi's Random Tools

A Blender addon that speeds up my workflow (Mainly related to BeamNG.Drive modding).

Mainly coded by AI :C , i dont like that but it works for me and it might help someone else so.
>Im finally starting to Learn Python so i can code most of the stuff myself and use less AI ^-^

Im not sure if all of the tools have an actual impact on performance, but it does make my scene prettier :p
 
## Installation / Usage

Just like any Regular Blender addon, download the Release and install the .zip

Tested under **Blender 4.5.4 LTS** but im pretty sure anything above **4.2** or even earlier should work

To use it find the panel in 3D Viewport SideBar, if you cant find it, by default you open this sidebar by pressing the key **N** then you will the panel under the **Lichi's Tools** Section

Use the ```Affect Selected Objects Only``` checkbox incase you have many objects on your scene, especially if you have some hidden objects , some of the crappy AI code doenst like that.

## Features

### Material Tools
- **Remove Unused Material Slots**: Removes material slots from objects where the material isn't actually used by any parts of the mesh, useful when you separate and join stuff since it often leaves unused materials behind.
- **Merge Material Duplicates**: Finds duplicate materials (Material.001, Material.002, etc.) and reassigns them to use the original material instead, this of course requires proper material names, make sure that you "clone" materials are actually the same and not different stuff before running

### Mesh Tools
- **Sync Mesh/Object Names**: Changes mesh data names to match their parent object names, this is pretty usless, but it makes my eyes happy
- **Override Vertex Color**: Removes all vertex colors of the selected objects and replaces them with a new one with the selected color, uses Face Corner - Byte Color, since thats what i need for BeamNG.Drive
### UV Tools
- **Rename UV Map**: Rename UV maps by index. Set the index (0-n) and new name, then apply to selected or all objects. for example, an index of 0 will replace the first UVs name to whatever you set, very useful when you join geometry so UVs join properly

### Scene Tools
- **Clear Orphan Data**: Removes all unused data blocks from the file, This already exists but its hard to reach so i put it here
- **Vieweport to Render Visibility** Sets The render visibility (camera icon to the right of an object) using the current vieweport visibility.

## Warning

Always save your work before running this. While these operations can usually be undone, it's better to be safe. 

This is especially important since parts of this is AI slop, and the rest is amateur code. I have personally tested everything (Since these tools only exist because i need them) but better safe than sorry.