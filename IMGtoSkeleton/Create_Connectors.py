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
