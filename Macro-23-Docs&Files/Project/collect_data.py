import cv2
import os
import time

def capture_frames(video_source=0, output_folder='c:/Users/LENOVO/Desktop/PBL-AI/pbl/Datasets', frame_interval=0.5, max_frames=2):
    """
    Mengambil frame dari sumber video dan menyimpannya ke folder output.
    
    Args:
        video_source (int or str): Sumber video (0 untuk kamera default atau path ke file video).
        output_folder (str): Folder tujuan untuk menyimpan frame.
        frame_interval (float): Interval waktu (detik) antara pengambilan frame.
        max_frames (int): Jumlah maksimal frame yang akan diambil.
    """
    # Membuat folder output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Membuat objek VideoCapture
    video_capture = cv2.VideoCapture(video_source)

    # Menunggu 5 detik sebelum mulai mengambil frame
    time.sleep(5)

    # Mengambil frame dengan interval waktu dan batasan jumlah frame
    frame_count = 0
    exit_key = ord('q')  # Key code for 'q'
    while frame_count < max_frames:
        # Membaca satu frame dari video capture
        ret, frame = video_capture.read()

        # Keluar dari loop jika mencapai akhir video atau jika 'q' ditekan
        if not ret or cv2.waitKey(1) & 0xFF == exit_key:
            break

        # Menyimpan frame ke folder output
        frame_filename = os.path.join(output_folder, f'Data_{frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        cv2.imshow("frame", frame)

        frame_count += 1

        # Menunggu sebelum mengambil frame berikutnya
        time.sleep(frame_interval)

    # Melepaskan objek video capture dan menutup jendela yang terbuka
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Panggil fungsi capture_frames dengan parameter yang sesuai
    capture_frames()
