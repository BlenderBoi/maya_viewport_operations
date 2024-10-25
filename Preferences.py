import bpy
from . Operator import *
import rna_keymap_ui

addon_keymaps = []
disabled_keymaps = []




class SP_user_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__


    Set_Smooth_Button : bpy.props.BoolProperty(default=True)
    No_Shade_Smooth: bpy.props.BoolProperty(default=False)

    subdivision_levels: bpy.props.IntProperty(default=2, min=1, soft_max=8)
    use_shade_smooth: bpy.props.BoolProperty(default=True)

    use_maya_mode: bpy.props.BoolProperty(default=True)

    def draw(self, context):


        layout = self.layout

        wm = bpy.context.window_manager
        box = layout.box()
        split = box.split()
        col = split.column()
        col.separator()


        keymap = context.window_manager.keyconfigs.user.keymaps['3D View']
        keymap_items = keymap.keymap_items
        km = keymap.active()



        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        for addon_keymap in addon_keymaps:
  
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, addon_keymap[0], addon_keymap[1], col, 0)
        
        box = layout.box()
        for disabled_keymap in disabled_keymaps:
            rna_keymap_ui.draw_kmi([], kc, disabled_keymap[0], disabled_keymap[1], box, 0)

        # else:
        #     col.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry")


        col.prop(self, "subdivision_levels", text="Subdivision Level")
        col.prop(self, "use_shade_smooth", text="Use Shade Smooth")
        col.prop(self, "maya_mode", text="Maya Mode")




def get_addon_preferences():
    ''' quick wrapper for referencing addon preferences '''
    addon_preferences = bpy.context.user_preferences.addons[__package__].preferences
    return addon_preferences



def add_hotkey():
    user_preferences = bpy.context.preferences
    addon_prefs = user_preferences.addons[__package__].preferences




    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon



    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("mvo.viewport_operations", type="ONE", value="PRESS")
    kmi.properties.mode = 1
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("mvo.viewport_operations", type="TWO", value="PRESS")
    kmi.properties.mode = 2
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("mvo.viewport_operations", type="THREE", value="PRESS")
    kmi.properties.mode = 3
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("mvo.viewport_operations", type="FOUR", value="PRESS")
    kmi.properties.mode = 4
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("mvo.viewport_operations", type="FIVE", value="PRESS")
    kmi.properties.mode = 5
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("mvo.viewport_operations", type="SIX", value="PRESS")
    kmi.properties.mode = 6
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new("mvo.viewport_operations", type="SEVEN", value="PRESS")
    kmi.properties.mode = 7
    addon_keymaps.append((km, kmi))



    kc_active = wm.keyconfigs.get(bpy.context.preferences.keymap.active_keyconfig)
    for km in kc_active.keymaps:
        for kmi in km.keymap_items:
            
            if km.name in ["Object Mode", "Mesh"]:
                
                for addon_keymap in addon_keymaps:
                    match = addon_keymap[1].compare(kmi)
                    if match:
                        kmi.active = False
                        disabled_keymaps.append((km, kmi))
                        print("disabled keymap - " + kmi.name + " - Key: " + kmi.to_string())
                        
 



class Template_Add_Hotkey(bpy.types.Operator):
    ''' Add hotkey entry '''
    bl_idname = "template.add_hotkey"
    bl_label = "Addon Preferences Example"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        add_hotkey()
        # self.report({'INFO'}, "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
        return {'FINISHED'}

def remove_hotkey():
    ''' clears all addon level keymap hotkeys stored in addon_keymaps '''
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

        # wm.keyconfigs.addon.keymaps.remove(km)

    addon_keymaps.clear()



classes = [SP_user_preferences, Template_Add_Hotkey]

def register():

    add_hotkey()



    for cls in classes:
        bpy.utils.register_class(cls)




    pass


def unregister():

    remove_hotkey()

    for cls in classes:
        bpy.utils.unregister_class(cls)



    pass

if __name__ == "__main__":
    register()
