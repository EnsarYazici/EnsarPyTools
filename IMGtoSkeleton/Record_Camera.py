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
