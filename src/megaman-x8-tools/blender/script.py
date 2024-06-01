import bpy
from bpy_extras.io_utils import ImportHelper

from core.set import SetFile

bl_info = {
    "name": "Mega Man X8 Editor Scripts",
    "description": "",
    "author": "RainfallPianist",
    "version": (1, 0),
    "blender": (2, 81, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export"
}


class ImportSetFile(bpy.types.Operator, ImportHelper):
    """Set File Import Script"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "x8editor.import_set"
    bl_label = "[X8Editor] Import Set File"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".set"
    filter_glob = bpy.props.StringProperty(default="*.set",options={'HIDDEN'},)

    def execute(self, context):
        scene = context.scene

        # Loading set file data
        set_file = SetFile(self.filepath)
        self.report({"INFO"}, "Importing " + set_file.stage_name)

        collection_name = f'{set_file.stage_name} Enemies'
        enemy_collection = bpy.data.collections.new(collection_name)
        scene.collection.children.link(enemy_collection)
        for enemy in set_file.enemies:
            bpy.ops.mesh.primitive_cube_add()
            cube = bpy.context.active_object
            bpy.ops.collection.objects_remove_all()

            cube.name = enemy.type
            cube.location=(enemy.x, 0, enemy.y)
            bpy.data.collections[collection_name].objects.link(cube)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ImportSetFile)


def unregister():
    bpy.utils.unregister_class(ImportSetFile)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()

# print("BPY DATA Filepath", bpy.data.filepath)
# for enemy in set_file.enemies:
#     bpy.ops.mesh.primitive_cube_add()
#
#     # newly created cube will be automatically selected
#     cube = bpy.context.selected_objects[0]
#
#     # change name
#     cube.name = enemy.type
#
#     # change its location
#     z = 0.0
#     cube.location = (enemy.x, enemy.y, z)
