import bpy

# アドオン情報（名前やバージョンなど）
bl_info = {
    "name": "One Step to Local",
    "author": "Pon Pon Games",
    "version": (0, 1),
    "blender": (3, 4, 0),
    "location": "3D Viewport > View > Sidebar (N key) > GLMR",
    "description": "This adds buttons that switches transform orientation between Global and Loacal.",
    "warning": "Not enough debugging. This addon can cause crashes.",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "3D View"
}

# Log
# 0: Warn and Error
# 1: Debug
# 2: Debug (Noisy)
def print_log(text, level):
    level_max = 0
    if level <= level_max:
        print(text)

# Blender起動後の初回のアドオン有効時だけ呼ばれます。
print_log("One Step to Local is called", 1)

# 制御オペレータ
# 状態をトグルします。UIに追加したボタンから呼ばれます。
class OneStepToLocal_OT_SetGlobal(bpy.types.Operator):
    bl_idname = "onesteptolocal.setglobal"
    bl_label = "Toggle Global"

    @classmethod
    def poll(cls, context):
        return context.scene.transform_orientation_slots[0].type != "GLOBAL"

    def __init__(self):
        print_log("OneStepToLocal_OT_SetGlobal.init is called", 1)

    def __del__(self):
        print_log("OneStepToLocal_OT_SetGlobal.del is called", 1)

    def execute(self, context):
        print_log("OneStepToLocal_OT_SetGlobal.execute is called", 1)
        context.scene.transform_orientation_slots[0].type = "GLOBAL"
        return {'FINISHED'}

    def invoke(self, context, event):
        print_log("OneStepToLocal_OT_SetGlobal.invoke is called", 1)
        return self.execute(context)

class OneStepToLocal_OT_SetLocal(bpy.types.Operator):
    bl_idname = "onesteptolocal.setlocal"
    bl_label = "Toggle Local"

    @classmethod
    def poll(cls, context):
        return context.scene.transform_orientation_slots[0].type != "LOCAL"

    def __init__(self):
        print_log("OneStepToLocal_OT_SetLocal.init is called", 1)

    def __del__(self):
        print_log("OneStepToLocal_OT_SetLocal.del is called", 1)

    def execute(self, context):
        print_log("OneStepToLocal_OT_SetLocal.execute is called", 1)
        context.scene.transform_orientation_slots[0].type = "LOCAL"
        return {'FINISHED'}

    def invoke(self, context, event):
        print_log("OneStepToLocal_OT_SetLocal.invoke is called", 1)
        return self.execute(context)

class OneStepToLocal_OT_SetMove(bpy.types.Operator):
    bl_idname = "onesteptolocal.setmove"
    bl_label = "Toggle Move"

    @classmethod
    def poll(cls, context):
        v_mode = context.workspace.tools.from_space_view3d_mode(bpy.context.mode)
        return v_mode.idname != "builtin.move"

    def __init__(self):
        print_log("OneStepToLocal_OT_SetMove.init is called", 1)

    def __del__(self):
        print_log("OneStepToLocal_OT_SetMove.del is called", 1)

    def execute(self, context):
        print_log("OneStepToLocal_OT_SetMove.execute is called", 1)
        bpy.ops.wm.tool_set_by_id(name = "builtin.move")
        return {'FINISHED'}

    def invoke(self, context, event):
        print_log("OneStepToLocal_OT_SetMove.invoke is called", 1)
        return self.execute(context)

class OneStepToLocal_OT_SetRotation(bpy.types.Operator):
    bl_idname = "onesteptolocal.setrotation"
    bl_label = "Toggle Rot"

    @classmethod
    def poll(cls, context):
        v_mode = context.workspace.tools.from_space_view3d_mode(bpy.context.mode)
        return v_mode.idname != "builtin.rotate"

    def __init__(self):
        print_log("OneStepToLocal_OT_SetRotation.init is called", 1)

    def __del__(self):
        print_log("OneStepToLocal_OT_SetRotation.del is called", 1)

    def execute(self, context):
        print_log("OneStepToLocal_OT_SetRotation.execute is called", 1)
        bpy.ops.wm.tool_set_by_id(name = "builtin.rotate")
        return {'FINISHED'}

    def invoke(self, context, event):
        print_log("OneStepToLocal_OT_SetRotation.invoke is called", 1)
        return self.execute(context)

# UIのクラス
# bpy.types.Panel派生クラスはregister_classするだけでサイドバーに現れます。
class ToggleGLMR_PT_TogglePanel(bpy.types.Panel):
    bl_label = "Toggle GLMR"
    bl_idname = "TOGGLEGLMR_PT_toggle_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GLMR"

    def draw(self, context):
        if context.active_object != None:
            if context.active_object.mode == "OBJECT" or context.active_object.mode == "EDIT" or context.active_object.mode == "POSE":

                layout = self.layout

                label = "Others"
                if context.scene.transform_orientation_slots[0].type == "GLOBAL":
                    label = "Global"
                if context.scene.transform_orientation_slots[0].type == "LOCAL":
                    label = "Local"
                layout.label(text=label)

                row = layout.row(align=True)
                row.active = True
                row.scale_y = 2
                label = "GLO"
                row.operator(OneStepToLocal_OT_SetGlobal.bl_idname, text=label, icon="ORIENTATION_GLOBAL")
                label = "LOC"
                row.operator(OneStepToLocal_OT_SetLocal.bl_idname, text=label, icon="ORIENTATION_LOCAL")

                label = "Others"
                v_mode = context.workspace.tools.from_space_view3d_mode(bpy.context.mode)
                if v_mode.idname == "builtin.move":
                    label = "Move"
                if v_mode.idname == "builtin.rotate":
                    label = "Rotate"
                if v_mode.idname == "builtin.scale":
                    label = "Scale"
                layout.label(text=label)

                row = layout.row(align=True)
                row.active = True
                row.scale_y = 2
                label = "MOV"
                row.operator(OneStepToLocal_OT_SetMove.bl_idname, text=label, icon="DRIVER_DISTANCE")
                label = "ROT"
                row.operator(OneStepToLocal_OT_SetRotation.bl_idname, text=label, icon="DRIVER_ROTATIONAL_DIFFERENCE")

# アドオンを有効にしたときにBlenderから呼ばれます。
# このとき、bpy.dataとbpy.contextにアクセス不可。
def register():
    print_log("register is called.", 1)
    bpy.utils.register_class(OneStepToLocal_OT_SetGlobal)
    bpy.utils.register_class(OneStepToLocal_OT_SetLocal)
    bpy.utils.register_class(OneStepToLocal_OT_SetMove)
    bpy.utils.register_class(OneStepToLocal_OT_SetRotation)
    bpy.utils.register_class(ToggleGLMR_PT_TogglePanel)

# アドオンを無効にしたときにBlenderから呼ばれます。
# このとき、bpy.dataとbpy.contextにアクセス不可。
def unregister():
    print_log("unregister is called", 1)
    bpy.utils.unregister_class(ToggleGLMR_PT_TogglePanel)
    bpy.utils.unregister_class(OneStepToLocal_OT_SetRotation)
    bpy.utils.unregister_class(OneStepToLocal_OT_SetMove)
    bpy.utils.unregister_class(OneStepToLocal_OT_SetLocal)
    bpy.utils.unregister_class(OneStepToLocal_OT_SetGlobal)

# Blenderのテキストエディタで呼んだときの処理（デバッグ用）
if __name__ == "__main__":
    print_log("One Step to Local is called from main", 1)
    register()
    #unregister()

