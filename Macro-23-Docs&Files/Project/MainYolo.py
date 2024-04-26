from ultralytics import YOLO # Library Paling Utama YOLO dalam Ultralytics
import cv2 #Library Utama ke-2 untuk menampilkan output
import cvzone # Library Utama ke-3 untuk bounding-box
import pyttsx3 # Library Utama ke-4 untuk menghasilkan Feedback Suara

# Library tambahan 
import math # Untuk perhitungan math, bisa juga menggunakan numpy
import time # Untuk waktu dan timestamp
import os # Untuk mengatur direktori

def set_working_directory(directory):
    """Mengubah direktori kerja ke lokasi yang sesuai."""
    os.chdir(directory)

def initialize_yolo_model(model_path):
    """Inisialisasi model YOLO."""
    return YOLO(model_path)

def initialize_camera(width=1280, height=720):
    """Inisialisasi kamera."""
    cam = cv2.VideoCapture(0)
    cam.set(3, width)
    cam.set(4, height)
    if not cam.isOpened():
        raise Exception("Kamera tidak terdeteksi")
    return cam

def initialize_text_to_speech_engine():
    """Inisialisasi engine text-to-speech."""
    return pyttsx3.init()

def reset_feedback_count(feedback_dict):
    """Mereset dictionary feedback_count."""
    feedback_dict.clear()

def main():
    # Mengatur direktori kerja
    set_working_directory("c:/Users/LENOVO/Desktop/PBL-AI/pbl")

    # Inisialisasi model YOLO
    model = initialize_yolo_model("TrainedModel.pt")

    # Daftar nama kelas yang dikenali
    classNames = ["Marco", "Unknown Face"]

    # Inisialisasi kamera
    cam = initialize_camera(1280, 720)

    # Inisialisasi engine text-to-speech
    engine = initialize_text_to_speech_engine()

    # Konfigurasi reset feedback
    reset_time = time.time()
    reset_duration = 600  # 10 menit (600 detik)
    feedback_count = {}
    exit_key = 27  # Key code for 'q'

    while True:
        current = time.time()

        # Membaca frame dari kamera
        success, img = cam.read()

        # Keluar dari loop jika tidak berhasil atau tombol 'q' ditekan
        if not success or cv2.waitKey(1) & 0xFF == exit_key:
            break

        # Periksa apakah sudah waktunya untuk mereset feedback_count
        if current - reset_time >= reset_duration:
            reset_feedback_count(feedback_count)
            reset_time = current  # Perbarui waktu reset

        # Deteksi objek menggunakan model YOLO
        results = model(img, stream=True)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Mendapatkan koordinat bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Menghitung kepercayaan deteksi
                conf = math.ceil((box.conf[0] * 100)) / 100

                # Mendapatkan nama kelas
                cls = int(box.cls[0])

                if conf < 0.70:
                    cls = len(classNames) - 1  # Set class to "Unknown" yang merupakan kelas terakhir

                    # Menambahkan kotak bounding-box dan teks peringatan untuk kelas yang tidak dikenali
                    w, h = x2 - x1, y2 - y1
                    cvzone.cornerRect(img,
                                      (x1, y1, w, h),
                                      l=32, t=7, rt=3,
                                      colorR=(0, 0, 0), colorC=(0, 0, 255)
                                      )
                    cvzone.putTextRect(img,
                                       f'{classNames[cls]} {conf}',
                                       (max(0, x1), max(35, y1)),
                                       scale=3, thickness=2,
                                       colorT=(255, 255, 255), colorR=(139, 0, 0)
                                       )
                    if classNames[cls] not in feedback_count or feedback_count[classNames[cls]] < 2:
                        engine.say("Unknown")
                        engine.runAndWait()
                        # Memperbarui jumlah feedback untuk kelas ini
                        feedback_count[classNames[cls]] = feedback_count.get(classNames[cls], 0) + 1

                else:
                    # Menambahkan kotak bounding-box dan teks untuk kelas yang dikenali
                    w, h = x2 - x1, y2 - y1
                    cvzone.cornerRect(img,
                                      (x1, y1, w, h),
                                      l=32, t=7, rt=3,
                                      colorR=(255, 0, 0), colorC=(0, 255, 0)
                                      )
                    cvzone.putTextRect(img,
                                       f'{classNames[cls]} {conf}',
                                       (max(0, x1), max(35, y1)),
                                       scale=3, thickness=2,
                                       colorT=(255, 255, 255), colorR=(0, 0, 139)
                                       )
                    if classNames[cls] not in feedback_count or feedback_count[classNames[cls]] < 2:
                        engine.say(f"Hello, {classNames[cls]}")
                        engine.runAndWait()
                        # Memperbarui jumlah feedback untuk kelas ini
                        feedback_count[classNames[cls]] = feedback_count.get(classNames[cls], 0) + 1

        # Menampilkan frame dengan hasil deteksi
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    # Menutup kamera dan jendela tampilan
    cam.release()
    cv2.destroyAllWindows()

# Run the program
if __name__ == "__main__":
    main()
