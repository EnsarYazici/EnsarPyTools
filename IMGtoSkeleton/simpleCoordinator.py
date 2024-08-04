import bpy
import mathutils

# Objeleri sahneden al
obj_A = bpy.data.objects.get("A")
obj_B = bpy.data.objects.get("B")
obj_C = bpy.data.objects.get("C")

# 'mode' değişkeni, 'center' veya 'A' değerlerini alabilir
# 'center' ise C'yi A ve B'nin ortasına, 'A' ise A'nın olduğu yere yerleştirir
mode = 'center'  # Bu değeri 'A' olarak da değiştirebilirsiniz

if obj_A and obj_B and obj_C:
    # A ve B objelerinin dünya koordinatlarını al
    A = obj_A.location
    B = obj_B.location
    
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
else:
    print("Objelerden biri veya daha fazlası bulunamadı")
