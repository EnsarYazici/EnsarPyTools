import bpy
import csv

# Blender'daki mevcut tüm nesneleri temizleyin
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Yeni bir armature oluşturun
bpy.ops.object.armature_add()
armature = bpy.context.object
armature.name = 'PoseArmature'

# Edit moduna geçin
bpy.ops.object.mode_set(mode='EDIT')
armature_data = armature.data

# CSV dosyasını okuyun
csv_path = 'pose_coordinates.csv'  # CSV dosyasının yolu
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    frames = {}
    
    # Her frame ve landmark için koordinatları kaydedin
    for row in reader:
        frame = int(row['frame'])
        landmark = row['landmark']
        x = float(row['x'])
        y = float(row['y'])
        z = float(row['z'])

        if frame not in frames:
            frames[frame] = {}
        frames[frame][landmark] = (x, y, z)

# Kemikleri oluşturun
landmarks = next(iter(frames.values())).keys()
for landmark in landmarks:
    bone = armature_data.edit_bones.new(landmark)
    bone.head = (0, 0, 0)
    bone.tail = (0, 0.1, 0)  # Kemiklerin bir boyutu olması gerektiği için küçük bir uzunluk veriyoruz

# Pose moduna geçin
bpy.ops.object.mode_set(mode='POSE')

# Animasyon oluşturun
for frame in frames:
    bpy.context.scene.frame_set(frame)
    for landmark, (x, y, z) in frames[frame].items():
        bone = armature.pose.bones[landmark]
        bone.location = (x, y, z)
        bone.keyframe_insert(data_path="location", frame=frame)

# Animasyonu tekrar oynatmaya başladığınızda sahneyi başa alın
bpy.context.scene.frame_set(0)
