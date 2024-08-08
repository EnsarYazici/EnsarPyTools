```py
# Record_Video.py

import cv2
import mediapipe as mp
import csv

# MediaPipe Pose modelini başlatma
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# MediaPipe çizim yardımcı işlevleri
mp_drawing = mp.solutions.drawing_utils

# Video dosyasını açma
video_path = 'video.mp4'  # İşlemek istediğiniz video dosyasının yolu
cap = cv2.VideoCapture(video_path)

# Kemik isimlerini alma
landmark_names = [landmark.name for landmark in mp_pose.PoseLandmark]

# CSV dosyasını hazırlama
with open('pose_coordinates.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['frame', 'landmark', 'x', 'y', 'z', 'visibility'])

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Renk alanını BGR'den RGB'ye dönüştürme
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # İşlemeyi uygulama
        results = pose.process(image)

        # Görüntüyü tekrar BGR'ye dönüştürme
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Anahtar noktaları çizme ve kaydetme
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Anahtar noktaların koordinatlarını CSV'ye yazma
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                writer.writerow([frame_count, landmark_names[idx], landmark.x, landmark.y, landmark.z, landmark.visibility])

        # Görüntüyü gösterme
        cv2.imshow('Pose Estimation', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        frame_count += 1

cap.release()
cv2.destroyAllWindows()
```
```py
# Record_Camera.py

import cv2
import mediapipe as mp
import csv

# MediaPipe Pose modelini başlatma
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# MediaPipe çizim yardımcı işlevleri
mp_drawing = mp.solutions.drawing_utils

# Video akışını başlatma
cap = cv2.VideoCapture(0)

# CSV dosyasını hazırlama
with open('pose_coordinates.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['frame', 'landmark', 'x', 'y', 'z', 'visibility'])

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Renk alanını BGR'den RGB'ye dönüştürme
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # İşlemeyi uygulama
        results = pose.process(image)

        # Görüntüyü tekrar BGR'ye dönüştürme
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Anahtar noktaları çizme ve kaydetme
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Anahtar noktaların koordinatlarını CSV'ye yazma
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                writer.writerow([frame_count, idx, landmark.x, landmark.y, landmark.z, landmark.visibility])

        # Görüntüyü gösterme
        cv2.imshow('Pose Estimation', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        frame_count += 1

cap.release()
cv2.destroyAllWindows()
```
```py
# CSVtoBlender.py

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
csv_path = 'C:/Users/yzcen/Desktop/IMGSkeletonCoordinate/mp/pose_coordinates.csv'  # CSV dosyasının yolu
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    frames = {}
    
    # Her frame ve landmark için koordinatları kaydedin
    for row in reader:
        frame = int(row['frame'])
        landmark = row['landmark']
        x = float(row['x']) -0.5
        y = float(row['z'])
        z = -float(row['y']) + 1.0

        if frame not in frames:
            frames[frame] = {}
        frames[frame][landmark] = (x, y, z)

# İstediğiniz organları belirleyin
selected_landmarks = ['NOSE', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', "LEFT_ELBOW", 'RIGHT_ELBOW', 'LEFT_WRIST', "RIGHT_WRIST", 'LEFT_HIP', 'RIGHT_HIP', "LEFT_KNEE", 'RIGHT_KNEE', 'LEFT_ANKLE', "RIGHT_ANKLE"]
# Tüm organları seçmek için bu listeyi boş bırakın veya None yapın
# selected_landmarks = None

# Kemikleri oluşturun
landmarks = next(iter(frames.values())).keys()
for landmark in landmarks:
    if selected_landmarks is None or landmark in selected_landmarks:
        bone = armature_data.edit_bones.new(landmark)
        bone.head = (0, 0, 0)
        bone.tail = (0, 0.1, 0)  # Kemiklerin bir boyutu olması gerektiği için küçük bir uzunluk veriyoruz
if "Bone" in armature_data.edit_bones:
    armature_data.edit_bones.remove(armature_data.edit_bones["Bone"])
# Pose moduna geçin
bpy.ops.object.mode_set(mode='POSE')

# Animasyon oluşturun
for frame in frames:
    bpy.context.scene.frame_set(frame)
    for landmark, (x, y, z) in frames[frame].items():
        if selected_landmarks is None or landmark in selected_landmarks:
            bone = armature.pose.bones[landmark]
            bone.location = (x, y, z)
            bone.keyframe_insert(data_path="location", frame=frame)

# Animasyonu tekrar oynatmaya başladığınızda sahneyi başa alın
bpy.context.scene.frame_set(0)
```
```py
# SetValidEmptys.py

import bpy

# Armature'ı seçin
armature = bpy.data.objects['PoseArmature']
bpy.context.view_layer.objects.active = armature

# Pose moduna geçin
bpy.ops.object.mode_set(mode='POSE')

# Tüm kemikler için mevcut "Empty" nesneleri bulun, lokasyonlarını eşitleyin ve "Child Of" constraint ekleyin
for bone in armature.pose.bones:
    # Empty nesnesini isme göre bulun
    empty_name = f'empty_{bone.name}'
    empty = bpy.data.objects.get(empty_name)
    
    if empty is not None:
        # Empty nesnesinin lokasyonunu kemiğin lokasyonuna eşitleyin
        empty.location = armature.matrix_world @ bone.head
        
        # Mevcut empty nesnesine child of constraint ekleyin
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

print("Constraints have been added and empty objects have been positioned.")
```
```py
# CreatingEmptys.py

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
```
```py
# Create_Connectors.py

import bpy
import mathutils

def create_connector_cubes(cube_name,empty1_name, empty2_name,originStyle = "center"):
    # Empty nesnelerini alın
    empty1 = bpy.data.objects[empty1_name]
    empty2 = bpy.data.objects[empty2_name]

    # İki empty arasındaki mesafeyi hesaplayın
    distance = (empty2.location - empty1.location).length
    
    # Küpü oluşturun
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.object
    cube.name = cube_name
    
    # Küpün boyutlarını ayarlayın
    cube.scale = (distance / 2, 0.0125, 0.0125)  # x boyutu mesafenin yarısı, y ve z boyutları 0.025 / 2
    
    # Küpü iki empty'nin ortasına yerleştirin
    cube.location = (empty1.location + empty2.location) / 2
    
    # setting origin
    
    cube = bpy.data.objects[cube_name]
    
    # Edit moduna geçin
    bpy.context.view_layer.objects.active = cube
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Tüm vertexleri seçin
    bpy.ops.mesh.select_all(action='SELECT')
    
    if originStyle == "left":   
        bpy.ops.transform.translate(value=(distance / 2, 0, 0))
    elif originStyle == "right":
        bpy.ops.transform.translate(value=(-distance / 2, 0, 0))
        
    
    # Ön yüzü (-Y yönünde) seçin
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    for face in cube.data.polygons:
        if face.normal.y < 0:
            face.select = True
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Yarıya kadar inset yapın
    bpy.ops.mesh.inset(thickness=0.5)
    
    # Biraz extrude edin
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, -0.015, 0)})
    
    # Object moduna geri dönün
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
    

# Örnek kullanım
def track_between_objects(a, b, c, mode='center'):
    # Objeleri sahneden al
    obj_A = bpy.data.objects.get(a)
    obj_B = bpy.data.objects.get(b)
    obj_C = bpy.data.objects.get(c)

    if obj_A and obj_B and obj_C:
        # Animasyonun adını belirleyin
        action_name = f"{obj_C.name}_track"
        action = bpy.data.actions.new(name=action_name)
        obj_C.animation_data_create()
        obj_C.animation_data.action = action
        
        # Sahnedeki toplam frame sayısını alın
        scene = bpy.context.scene
        start_frame = scene.frame_start
        end_frame = scene.frame_end
        
        for frame in range(start_frame, end_frame + 1):
            # Geçerli frame'i ayarlayın
            scene.frame_set(frame)
            
            # A ve B objelerinin dünya koordinatlarını al
            A = obj_A.matrix_world.translation
            B = obj_B.matrix_world.translation
            
            # İki nokta arasındaki yönü hesapla
            direction = (B - A).normalized()
            
            # C objesinin konumunu ayarlama
            if mode == 'center':
                obj_C.location = (A + B) / 2
            elif mode == 'A':
                obj_C.location = A
            
            # Hesaplanan yönü C objesine aktar
            # C'nin rotasını direction'a göre ayarla
            obj_C.rotation_mode = 'QUATERNION'
            obj_C.rotation_quaternion = direction.to_track_quat('X', 'Z')  # X eksenini yönlendirici olarak kullanma
            
            # Konum ve rotasyonu keyframe olarak ekleyin
            obj_C.keyframe_insert(data_path="location", frame=frame)
            obj_C.keyframe_insert(data_path="rotation_quaternion", frame=frame)
    else:
        print("Objelerden biri veya daha fazlası bulunamadı")
        
        
      
create_connector_cubes("ConnectorCube_Hip",'empty_RIGHT_HIP', 'empty_LEFT_HIP',"center")
create_connector_cubes("ConnectorCube_Shoulder",'empty_RIGHT_SHOULDER', 'empty_LEFT_SHOULDER',"center")
create_connector_cubes("ConnectorCube_UpperArm_L",'empty_LEFT_SHOULDER', 'empty_LEFT_ELBOW',"left")
create_connector_cubes("ConnectorCube_UpperArm_R",'empty_RIGHT_SHOULDER', 'empty_RIGHT_ELBOW',"left")
create_connector_cubes("ConnectorCube_LowerArm_L",'empty_LEFT_ELBOW', 'empty_LEFT_WRIST',"left")
create_connector_cubes("ConnectorCube_LowerArm_R",'empty_RIGHT_ELBOW', 'empty_RIGHT_WRIST',"left")
create_connector_cubes("ConnectorCube_UpperLeg_L",'empty_LEFT_HIP', 'empty_LEFT_KNEE',"left")
create_connector_cubes("ConnectorCube_UpperLeg_R",'empty_RIGHT_HIP', 'empty_RIGHT_KNEE',"left")
create_connector_cubes("ConnectorCube_LowerLeg_L",'empty_LEFT_KNEE', 'empty_LEFT_ANKLE',"left")
create_connector_cubes("ConnectorCube_LowerLeg_R",'empty_RIGHT_KNEE', 'empty_RIGHT_ANKLE',"left")

# Örnek kullanım
track_between_objects('empty_RIGHT_HIP', 'empty_LEFT_HIP', 'ConnectorCube_Hip', 'center')
track_between_objects('empty_RIGHT_SHOULDER', 'empty_LEFT_SHOULDER', 'ConnectorCube_Shoulder', 'center')
track_between_objects('empty_LEFT_SHOULDER', 'empty_LEFT_ELBOW', 'ConnectorCube_UpperArm_L', 'A')
track_between_objects('empty_RIGHT_SHOULDER', 'empty_RIGHT_ELBOW', 'ConnectorCube_UpperArm_R', 'A')
track_between_objects('empty_LEFT_ELBOW', 'empty_LEFT_WRIST', 'ConnectorCube_LowerArm_L', 'A')
track_between_objects('empty_RIGHT_ELBOW', 'empty_RIGHT_WRIST', 'ConnectorCube_LowerArm_R', 'A')
track_between_objects('empty_LEFT_HIP', 'empty_LEFT_KNEE', 'ConnectorCube_UpperLeg_L', 'A')
track_between_objects('empty_RIGHT_HIP', 'empty_RIGHT_KNEE', 'ConnectorCube_UpperLeg_R', 'A')
track_between_objects('empty_LEFT_KNEE', 'empty_LEFT_ANKLE', 'ConnectorCube_LowerLeg_L', 'A')
track_between_objects('empty_RIGHT_KNEE', 'empty_RIGHT_ANKLE', 'ConnectorCube_LowerLeg_R', 'A')
```
