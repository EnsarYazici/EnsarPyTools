import bpy

# Armature'ı seçin
armature = bpy.data.objects['PoseArmature']
bpy.context.view_layer.objects.active = armature

# Pose moduna geçin
bpy.ops.object.mode_set(mode='POSE')

# Tüm kemikler için "Empty" nesneleri oluşturun ve "Child Of" constraint ekleyin
for bone in armature.pose.bones:
    # Empty nesnesi oluşturun
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=armature.matrix_world @ bone.head)
    empty = bpy.context.object
    empty.name = f'empty_{bone.name}'
    
    # Empty nesnesini kemiğe bağlayın
    constraint = empty.constraints.new(type='CHILD_OF')
    constraint.target = armature
    constraint.subtarget = bone.name
    
    # Constraint'i uygulayın
    bpy.context.view_layer.objects.active = empty
    bpy.ops.object.visual_transform_apply()
    bpy.ops.object.constraints_clear()
    
    # Constraint'i tekrar ekleyin
    constraint = empty.constraints.new(type='CHILD_OF')
    constraint.target = armature
    constraint.subtarget = bone.name
    
    # Armature'ı tekrar aktif yapın
    bpy.context.view_layer.objects.active = armature
    bpy.ops.object.mode_set(mode='POSE')

# Pose modundan çıkın
bpy.ops.object.mode_set(mode='OBJECT')
