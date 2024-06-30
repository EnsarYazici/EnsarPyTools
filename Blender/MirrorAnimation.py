import bpy

calculateUnicBones = True
# Pick selected object
selected_object = bpy.context.active_object

# Switch the selected object to pose mode
bpy.ops.object.mode_set(mode='POSE')
scene = bpy.context.scene

# Go round all the bones
for f in range(scene.frame_start, scene.frame_end + 1):
    # Adjust frame
    scene.frame_set(f)
    for bone in selected_object.pose.bones:
        # If the bone name contains ".R"
        if ".R" in bone.name:
            # Karşılık gelen ".L" kemik adını oluştur
            left_bone_name = bone.name.replace(".R", ".L")
            
            # Generate the corresponding ".L" bone name
            right_bone = selected_object.pose.bones.get(bone.name)
            left_bone = selected_object.pose.bones.get(left_bone_name)
            
            if right_bone and left_bone:
                # Copy locations
                leftTemp = left_bone.location.copy()

                left_bone.location.x = -right_bone.location.copy().x
                left_bone.location.y = right_bone.location.copy().y
                left_bone.location.z = right_bone.location.copy().z
                left_bone.keyframe_insert(data_path="location")

                right_bone.location.x = -leftTemp.x
                right_bone.location.y = leftTemp.y
                right_bone.location.z = leftTemp.z
                right_bone.keyframe_insert(data_path="location")
                
                # Copy rotations
                leftTemp = left_bone.rotation_quaternion.copy()

            
                left_bone.rotation_quaternion.x = right_bone.rotation_quaternion.copy().x
                left_bone.rotation_quaternion.y = -right_bone.rotation_quaternion.copy().y
                left_bone.rotation_quaternion.z = -right_bone.rotation_quaternion.copy().z
                left_bone.keyframe_insert(data_path="rotation_quaternion")

                right_bone.rotation_quaternion.x = leftTemp.x
                right_bone.rotation_quaternion.y = -leftTemp.y
                right_bone.rotation_quaternion.z = -leftTemp.z
                right_bone.keyframe_insert(data_path="rotation_quaternion")
                
                # Copy scales
                leftTemp = left_bone.scale.copy()
                left_bone.scale = right_bone.scale.copy()
                left_bone.keyframe_insert(data_path="scale")
                right_bone.scale = leftTemp
                right_bone.keyframe_insert(data_path="scale")
        elif ".L" in bone.name:
            continue
        else:
            if calculateUnicBones == True:
                unic_Bone = selected_object.pose.bones.get(bone.name)

                unic_BoneTemp = unic_Bone.location.copy()
                unic_Bone.location.x = -unic_BoneTemp.x
                unic_Bone.location.y = unic_BoneTemp.y
                unic_Bone.location.z = unic_BoneTemp.z
                unic_Bone.keyframe_insert(data_path="location")

                unic_BoneTemp = unic_Bone.rotation_quaternion.copy()
                unic_Bone.rotation_quaternion.x = unic_BoneTemp.x
                unic_Bone.rotation_quaternion.y = -unic_BoneTemp.y
                unic_Bone.rotation_quaternion.z = -unic_BoneTemp.z
                unic_Bone.keyframe_insert(data_path="rotation_quaternion")
# Exit Pose mode
bpy.ops.object.mode_set(mode='OBJECT')
