import bpy # type: ignore

class MATERIAL_OT_clean_unused(bpy.types.Operator):
    bl_idname = "material.clean_unused"
    bl_label = "Remove Materials Not Used In Mesh"
    bl_description = "Removes material slots from objects where the material is not actually used"

    def execute(self, context):
        only_selected = context.scene.cleanup_selected_only
        objs = context.selected_objects if only_selected else bpy.data.objects

        removed_count = 0

        for obj in objs:
            if obj.type == 'MESH' and obj.data.materials:
                used_indices = {poly.material_index for poly in obj.data.polygons}
                total_slots = len(obj.material_slots)

                for i in reversed(range(total_slots)):
                    if i not in used_indices:
                        bpy.context.view_layer.objects.active = obj
                        obj.active_material_index = i
                        bpy.ops.object.material_slot_remove()
                        removed_count += 1

        self.report({'INFO'}, f"Removed {removed_count} unused material slot(s)")
        return {'FINISHED'}


class MATERIAL_OT_rename_clones(bpy.types.Operator):
    bl_idname = "material.rename_clones"
    bl_label = "Change Duplicate Materials To Original"
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


class MESH_OT_rename_mesh_data(bpy.types.Operator):
    bl_idname = "mesh.rename_mesh_data"
    bl_label = "Set Mesh Name To Assigned Object Name"
    bl_description = "Takes the name of the object the mesh is assigned to and uses the objects name as its own"

    def execute(self, context):
        only_selected = context.scene.cleanup_selected_only
        objs = context.selected_objects if only_selected else bpy.data.objects

        mod_count = 0

        for obj in objs:
            if obj.type == 'MESH':
                obj.data.name = obj.name
                mod_count += 1
        self.report({'INFO'}, f"Mesh data renamed on {mod_count} meshe(s)")
        return {'FINISHED'}


class SCENE_OT_clear_orphans(bpy.types.Operator):
    bl_idname = "scene.clear_orphans"
    bl_label = "Clear Orphan Data"
    bl_description = "Clear all orphan data-blocks without any users from the file. Performs the same action as the Purge button in the Outliner (Orphan Data mode)"

    def execute(self, context):
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        self.report({'INFO'}, "Orphan data cleared")
        return {'FINISHED'}


class MESH_OT_rename_uv_map(bpy.types.Operator):
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


class TOOL_PT_custom_tools(bpy.types.Panel):
    bl_label = "Lichi's Random Tools [1.1]"
    bl_idname = "TOOL_PT_custom_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cleanup Tools"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "cleanup_selected_only")
        
        layout.label(text="Material Tools :")
        layout.operator("material.clean_unused", icon='TRASH')
        layout.operator("material.rename_clones", icon='MATERIAL')

        layout.label(text="Mesh Tools :")
        layout.operator("mesh.rename_mesh_data", icon='OUTLINER_OB_MESH')

        layout.label(text="UV Renamer :")
        row = layout.row(align=True)
        row.prop(context.scene, "uv_rename_index", text="UV Index")
        row.prop(context.scene, "uv_rename_text", text="Set To")
        layout.operator("mesh.rename_uv_map", icon='GROUP_UVS')

        layout.label(text="Other Tools :")
        layout.operator("scene.clear_orphans", icon='ORPHAN_DATA')


classes = (
    MATERIAL_OT_clean_unused,
    MATERIAL_OT_rename_clones,
    MESH_OT_rename_mesh_data,
    MESH_OT_rename_uv_map,
    SCENE_OT_clear_orphans,
    TOOL_PT_custom_tools,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.cleanup_selected_only = bpy.props.BoolProperty(
        name="Apply Only On Selected Objects",
        description="Only apply cleanup to selected object(s)",
        default=False
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

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    try:
        del bpy.types.Scene.cleanup_selected_only
        del bpy.types.Scene.uv_rename_index
        del bpy.types.Scene.uv_rename_text
    except:
        pass

if __name__ == "__main__":
    register()