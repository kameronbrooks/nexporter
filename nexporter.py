bl_info = {
    "name": "Export Collection Objects as FBX",
    "blender": (2, 93, 0),
    "category": "Object",
}

import bpy
import os
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

class OBJECT_OT_export_collection_fbx(Operator, ExportHelper):
    bl_idname = "object.export_collection_fbx"
    bl_label = "Export Collection Objects as FBX"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = ".fbx"
    
    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'},
        maxlen=255
    )
    
    def execute(self, context):
        # Get the directory path from the user input
        dir_path = os.path.dirname(self.filepath)

        # Check if the directory exists
        if not os.path.exists(dir_path):
            self.report({'ERROR'}, "Directory does not exist")
            return {'CANCELLED'}

        # Get the active collection
        active_collection = context.view_layer.active_layer_collection.collection
        
        # Get the current FBX Units Scale setting
        fbx_units_scale = context.scene.unit_settings.scale_length

        # Iterate through all objects in the active collection
        for obj in active_collection.objects:
            # Make the object the only selected and active object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj

            # Export the object as FBX with its name
            file_path = os.path.join(dir_path, obj.name + ".fbx")
            bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True, use_space_transform=True, bake_space_transform=True, global_scale=fbx_units_scale, apply_scale_options='FBX_SCALE_ALL', axis_forward='-Z', axis_up='Y')

        self.report({'INFO'}, "Exported objects to " + dir_path)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_export_collection_fbx.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_export_collection_fbx)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_export_collection_fbx)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()