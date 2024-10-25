import bpy

def get_nodegroup(name):
    return bpy.data.node_groups.get(name)

def ensure_nodegroup(name, create_node):
    node_group = get_nodegroup(name)

    if node_group is None:
        node_group =  create_node()

    return node_group

def create_geometry_nodegroup(name):
    node_group = bpy.data.node_groups.new(name, type="GeometryNodeTree")
    node_group.is_modifier = True
    node_group.interface.new_socket(name="Geo In", in_out ="INPUT", socket_type="NodeSocketGeometry")
    node_group.interface.new_socket(name="Geo Out", in_out ="OUTPUT", socket_type="NodeSocketGeometry")


    return node_group

def create_node_chain(node_group, node_names, node_offset=300):
    essential_node_names = ["NodeGroupInput"] + node_names
    essential_node_names.append("NodeGroupOutput")

    node_chain = []

    for node_name in essential_node_names:
        node = node_group.nodes.new(node_name)
        node_chain.append(node)


    for i, node in enumerate(node_chain):
        node.location.x = i * node_offset

        if i == 0:
            continue
        
        prev_node = node_chain[i-1]
        node_group.links.new(prev_node.outputs[0], node.inputs[0])


    

def create_smooth_preview():

    pos_offset = 300

    node_group = create_geometry_nodegroup("smooth_preview")

    socket = node_group.interface.new_socket("Level", socket_type="NodeSocketInt")
    socket.default_value = 2
    socket = node_group.interface.new_socket("Use Shade Smooth", socket_type="NodeSocketBool")
    socket.default_value = True



    node_in = node_group.nodes.new("NodeGroupInput")
    node_in.location.x = 0

    node_subdivision = node_group.nodes.new("GeometryNodeSubdivisionSurface")
    node_subdivision.location.x = pos_offset * 1


    node_shade_smooth = node_group.nodes.new("GeometryNodeSetShadeSmooth")
    node_shade_smooth.location.x = pos_offset * 2
    node_shade_smooth.location.y = -pos_offset * 1


    node_switch = node_group.nodes.new("GeometryNodeSwitch")
    node_switch.location.x = pos_offset * 3

    node_out = node_group.nodes.new("NodeGroupOutput")
    node_out.location.x = pos_offset * 4
    


    node_group.links.new(node_in.outputs[0], node_subdivision.inputs[0])
    node_group.links.new(node_in.outputs[1], node_subdivision.inputs[1])
    node_group.links.new(node_in.outputs[2], node_switch.inputs[0])
    node_group.links.new(node_subdivision.outputs[0], node_switch.inputs[1])
    node_group.links.new(node_switch.outputs[0], node_out.inputs[0])
    node_group.links.new(node_shade_smooth.outputs[0], node_switch.inputs[2])
    node_group.links.new(node_subdivision.outputs[0], node_shade_smooth.inputs[0])

    return node_group

def update_UI():
    for screen in bpy.data.screens:
        for area in screen.areas:
            area.tag_redraw()

def ensure_geometry_node_modifier(obj, name, node_group):
    mod = obj.modifiers.get(name)
    valid = False

    if mod is not None:
        if mod.type == "NODES":
            if mod.node_group == node_group:
                valid = True
    if not valid:
        mod = obj.modifiers.new("smooth_preview", "NODES")
        mod.node_group = node_group

    return mod

class SmoothPreview_OT_Set_Smooth(bpy.types.Operator):
    """Add Subdivision Modifier & Shade Smooth to Selected Objects"""

    bl_idname = "smooth_preview.set_smooth"
    bl_label = "Set Smooth"

    smooth: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        if context.active_object is not None and context.active_object.mode == "OBJECT":
            return True
        if context.active_object is not None and context.active_object.mode == "EDIT":
            return True
        if context.active_object is not None and context.active_object.mode == "SCULPT":
            return True

    def execute(self, context):

        node_group = ensure_nodegroup("smooth_preview", create_smooth_preview)

        preferences = context.preferences.addons[__package__].preferences

        smooth_preview_check = []

        for obj in context.selected_objects:

            if obj.type == "MESH":
                modifier = ensure_geometry_node_modifier(obj, "smooth_preview", node_group)

                modifier["Socket_2"] = preferences.subdivision_levels
                modifier["Socket_3"] = preferences.use_shade_smooth

                if self.smooth:
                    modifier.show_viewport = True
                    modifier.show_render = True
                    modifier.show_on_cage = True


                    
                else:
                    modifier.show_viewport = False
                    modifier.show_render = False
                    modifier.show_on_cage = False


                            
  
                



        update_UI()
        return {"FINISHED"}




class SmoothPreview_MT_Smooth_Menu(bpy.types.Menu):
    bl_label = "Smooth Menu"
    bl_idname = "SmoothPreview_MT_Smooth_Menu"

    def draw(self, context):
        layout = self.layout

        preferences = context.preferences.addons[__package__].preferences
        layout.prop(preferences, "subdivision_levels", text="Levels")
        layout.prop(preferences, "use_shade_smooth", text="Use Shade Smooth")

        #layout.operator("vh.apply_smooth", text="Apply")



def draw_item(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.prop(context.space_data.overlay, "show_wireframes", text="", icon="FILE_3D")
    preferences = context.preferences.addons[__package__].preferences
    row.operator("smooth_preview.set_smooth", text="Smooth").smooth = True
    row.operator("smooth_preview.set_smooth", text="Normal").smooth = False
    row.menu("SmoothPreview_MT_Smooth_Menu", text="", icon="DOWNARROW_HLT")







classes = [
    SmoothPreview_OT_Set_Smooth,
    SmoothPreview_MT_Smooth_Menu,

]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_HT_header.append(draw_item)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_HT_header.remove(draw_item)



if __name__ == "__main__":
    register()
