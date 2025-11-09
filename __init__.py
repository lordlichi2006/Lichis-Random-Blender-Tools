bl_info = {
    "name": "Lichi's Random Tools",
    "author": "Lichi",
    "version": (1, 3, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar > Lichi",
    "description": "Some tools that I needed for my workflow that AI helped me with, packaged into an addon :p",
    "warning": "",
    "doc_url": "https://github.com/lordlichi2006/",
    "category": "Object"
}


import bpy # type: ignore

class MATERIAL_cleanUnused(bpy.types.Operator):
    bl_idname = "material.clean_unused"
    bl_label = "Remove Unused Material Slots"
    bl_description = "Removes unassigned material slots from all objects"

    def execute(self, context):
        only_selected = context.scene.cleanup_selected_only
        objs = context.selected_objects if only_selected else context.scene.objects

        removed_count = 0

        for obj in objs:
            if obj.type == 'MESH' and obj.data.materials:
                # Collect indices of materials actually used by polygons
                used_indices = {poly.material_index for poly in obj.data.polygons}
                total_slots = len(obj.material_slots)

                # Rebuild material list keeping only used ones
                used_materials = [
                    slot.material for i, slot in enumerate(obj.material_slots)
                    if i in used_indices
                ]

                # If something was removed, rebuild the material slots
                if len(used_materials) < total_slots:
                    obj.data.materials.clear()
                    for mat in used_materials:
                        obj.data.materials.append(mat)
                    removed_count += total_slots - len(used_materials)

        self.report({'INFO'}, f"Removed {removed_count} unused material slot(s)")
        return {'FINISHED'}

class MATERIAL_renameClones(bpy.types.Operator):
    bl_idname = "material.rename_clones"
    bl_label = "Merge Material Duplicates"
    bl_description = "Gets all the Material copies (Material.0XX) and assigns them to the original"

    def execute(self, context):
        only_selected = context.scene.cleanup_selected_only
        objs = context.selected_objects if only_selected else bpy.data.objects

        materials = bpy.data.materials
        material_map = {}

        for mat in materials:
            if mat.name.endswith(tuple(f'.{str(i).zfill(3)}' for i in range(1, 999))):
                base_name = mat.name.rsplit('.', 1)[0]
                if base_name in materials:
                    material_map[mat] = materials[base_name]

        replaced_count = 0

        for obj in objs:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material in material_map:
                        slot.material = material_map[slot.material]
                        replaced_count += 1

        self.report({'INFO'}, f"Replaced {replaced_count} clone material reference(s)")
        return {'FINISHED'}


class MESH_renameMeshData(bpy.types.Operator):
    bl_idname = "mesh.rename_mesh_data"
    bl_label = "Sync Mesh/Object Names"
    bl_description = "Takes the name of the object the mesh is assigned to and uses the objects name as its own"

    def execute(self, context):
        only_selected = context.scene.cleanup_selected_only
        objs = context.selected_objects if only_selected else bpy.data.objects

        mod_count = 0

        for obj in objs:
            if obj.type == 'MESH':
                obj.data.name = obj.name
                mod_count += 1
        self.report({'INFO'}, f"Mesh data renamed on {mod_count} Meshe(s)")
        return {'FINISHED'}

class MESH_overrideVertCol(bpy.types.Operator):
    bl_idname = "mesh.reset_vert_color"
    bl_label = "Override Vertex Color"
    bl_description = "Removes any existing vertex colors, and replaces it with a vertex color in Face Corner Byte Color format with the selected color."

    def execute(self, context):
        only_selected = context.scene.cleanup_selected_only
        objs = context.selected_objects if only_selected else bpy.data.objects
        scene = context.scene

        mod_count = 0

        for obj in objs:
        
            # skip if object is not mesh
            if obj.type != 'MESH':
                continue

            mesh = obj.data

            # remove existing vertex colors
            while mesh.color_attributes:
                mesh.color_attributes.remove(mesh.color_attributes[0])
            # create new vertex color layer
            newVertCol = mesh.color_attributes.new(name="Color", type='BYTE_COLOR', domain='CORNER')

            # assign selected color to all vertices

            color = tuple(scene.vert_color_picker)

            data = [color] * len(mesh.vertices)

            for i in range(len(newVertCol.data)):
                newVertCol.data[i].color = color

            # make created vert color active
            mesh.color_attributes.active_color = newVertCol
            # add to the counter
            mod_count += 1

        self.report({'INFO'}, f"Vertex Color Overriden in {mod_count} meshe(s)")
        return {'FINISHED'}

class MESH_renameUVMaps(bpy.types.Operator):
    bl_idname = "mesh.rename_uv_map"
    bl_label = "Rename UV Map"
    bl_description = "Renames a specific UV map (by index) to a given name"

    def execute(self, context):
        only_selected = context.scene.cleanup_selected_only
        uv_index = context.scene.uv_rename_index
        new_name = context.scene.uv_rename_text

        objs = context.selected_objects if only_selected else bpy.data.objects
        renamed_count = 0

        for obj in objs:
            if obj.type == 'MESH' and obj.data.uv_layers:
                if uv_index < len(obj.data.uv_layers):
                    obj.data.uv_layers[uv_index].name = new_name
                    renamed_count += 1

        self.report({'INFO'}, f"Renamed UV map in {renamed_count} mesh(es)")
        return {'FINISHED'}


class SCENE_clearOrhpans(bpy.types.Operator):
    bl_idname = "scene.clear_orphans"
    bl_label = "Clear Orphan Data"
    bl_description = "Clear all orphan data-blocks without any users from the file. Performs the same action as the Purge button in the Outliner (Orphan Data mode)"

    def execute(self, context):
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        self.report({'INFO'}, "Orphan data cleared")
        return {'FINISHED'}

class SCENE_setRenderToVisible(bpy.types.Operator):

    bl_idname = "scene.render_visible_vieweport"
    bl_label = "Viewport to Render Visibility"
    bl_description = "Sets the render visibility based on the objects' visibility in the current viewport"

    def execute(self,context):
        only_selected = context.scene.cleanup_selected_only
        objs = context.selected_objects if only_selected else bpy.data.objects
        change_count = 0

        for obj in objs:
            is_visible = obj.visible_get()
            obj.hide_render = not is_visible
            change_count += 1
        self.report({'INFO'}, f"Render visibility updated from viewport visibility on {change_count} Object(s).")
        return {'FINISHED'}
    
class PANEL_toolPanel(bpy.types.Panel):
    bl_label = "Lichi's Random Tools [1.3]"
    bl_idname = "PANEL_toolPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Lichi's Tools"

    def draw(self, context):
        layout = self.layout
        
        # Affect Selected only Section
        layout.prop(context.scene, "cleanup_selected_only")

        box = layout.box()
        box.alert = True
        box.scale_y = 0.5 # make box padding
        box.label(text="This setting does not affect:") 
        box.label(text="Clear Orphan Data ", icon='ORPHAN_DATA')

        # Material Tools
        layout.label(text="Material Tools :")
        layout.operator("material.clean_unused", icon='TRASH')
        layout.operator("material.rename_clones", icon='MATERIAL')

        # Mesh Tools
        layout.label(text="Mesh Tools :")
        layout.operator("mesh.rename_mesh_data", icon='OUTLINER_OB_MESH')

        row = layout.row(align=True)
        row.operator("mesh.reset_vert_color", icon='COLOR')
        row.scale_x = 0.35 
        row.prop(context.scene, "vert_color_picker")

        # UV Renamer
        layout.label(text="UV Renamer :")
        row = layout.row(align=True)
        row.prop(context.scene, "uv_rename_index", text="UV Index")
        row.prop(context.scene, "uv_rename_text", text="Set To")
        layout.operator("mesh.rename_uv_map", icon='GROUP_UVS')

        # Scene Tools
        layout.label(text="Scene Tools :")
        layout.operator("scene.clear_orphans", icon='ORPHAN_DATA')
        layout.operator("scene.render_visible_vieweport",icon='RESTRICT_RENDER_OFF')


classes = (
    MATERIAL_cleanUnused,
    MATERIAL_renameClones,
    MESH_renameMeshData,
    MESH_renameUVMaps,
    MESH_overrideVertCol,
    SCENE_clearOrhpans,
    SCENE_setRenderToVisible,
    PANEL_toolPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.cleanup_selected_only = bpy.props.BoolProperty(
        name="Affect Selected Objects Only",
        description="Applies only to the objects currently selected in the viewport. Does not affect the Clear Orphan Data function.",
        default=True
    )
    bpy.types.Scene.uv_rename_index = bpy.props.IntProperty(
        name="UV Index",
        description="Index of the UV map to rename",
        default=0,
        min=0
    )
    bpy.types.Scene.uv_rename_text = bpy.props.StringProperty(
        name="New UV Name",
        description="New name for the selected UV map",
        default="UVMap"
    )
    # Register the color property on the scene
    bpy.types.Scene.vert_color_picker = bpy.props.FloatVectorProperty(
        name="",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        size=4  # RGBA
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    try:
        del bpy.types.Scene.cleanup_selected_only
        del bpy.types.Scene.uv_rename_index
        del bpy.types.Scene.uv_rename_text
        del bpy.types.Scene.vert_color_picker
    except:
        pass

if __name__ == "__main__":
    register()