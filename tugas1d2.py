import cv2
from ultralytics import YOLO

# Panggil Model YOLOv8
model = YOLO("yolov8n.pt")

# Menyalakan Kamera Webcam 
cap = cv2.VideoCapture(0)

# Menentukan ID 3 objek target (Orang=0, Gelas=41, HP=67)
target_objek = [0, 41, 67]

# Perulangan untuk membaca video frame demi frame
while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera tidak terdeteksi!")
        break

    # Command YOLO mendeteksi gambar dan batasi hanya untuk 3 kelas target
    hasil_deteksi = model(frame, classes=target_objek, conf=0.5)

    # YOLO menggambar otomatis Bounding Box, Nama, dan Confidence ke atas frame
    frame_bergaris = hasil_deteksi[0].plot()

    # tampilin ke layar
    cv2.imshow("Tugas 1 - Deteksi 3 Objek", frame_bergaris)

    # tombol stop
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()