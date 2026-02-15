import bpy

def add_copy_constraints():
    # 1. Seçim kontrolü
    selected_objects = bpy.context.selected_objects
    active_object = bpy.context.active_object

    # En az 2 obje seçili mi ve aktif obje bir armatür mü kontrol et
    if not active_object or active_object.type != 'ARMATURE' or len(selected_objects) < 2:
        print("HATA: Lütfen iki armatür seçin. Constraint eklenecek armatür 'Aktif' (sarı) olmalı.")
        return

    # Hedef armatürü belirle (Seçili olan ama aktif olmayan obje)
    target_armature = None
    for obj in selected_objects:
        if obj != active_object and obj.type == 'ARMATURE':
            target_armature = obj
            break
    
    if not target_armature:
        print("HATA: Hedef olarak uygun bir armatür bulunamadı.")
        return

    # Pose moduna geçiş yap (Constraintler pose kemiklerine eklenir)
    bpy.ops.object.mode_set(mode='POSE')

    print(f"İşlem Başlıyor: {active_object.name} -> {target_armature.name}")

    # 2. Kemikleri Döngüye Al
    for bone in active_object.pose.bones:
        # Hedef armatürde aynı isimde kemik var mı kontrol et
        if bone.name in target_armature.data.bones:
            
            # --- COPY LOCATION ---
            c_loc = bone.constraints.new('COPY_LOCATION')
            c_loc.name = "Auto_Copy_Location"
            c_loc.target = target_armature
            c_loc.subtarget = bone.name # Hedef kemik ismi
            
            # Uzay ayarları (World Space)
            c_loc.target_space = 'WORLD'
            c_loc.owner_space = 'WORLD'
            
            # --- COPY ROTATION ---
            c_rot = bone.constraints.new('COPY_ROTATION')
            c_rot.name = "Auto_Copy_Rotation"
            c_rot.target = target_armature
            c_rot.subtarget = bone.name # Hedef kemik ismi
            
            # Uzay ayarları (World Space)
            c_rot.target_space = 'WORLD'
            c_rot.owner_space = 'WORLD'
            
            print(f"Bağlandı: {bone.name}")
        else:
            print(f"Atlandı (Hedefte yok): {bone.name}")

    print("İşlem Tamamlandı.")

# Fonksiyonu çalıştır
add_copy_constraints()
