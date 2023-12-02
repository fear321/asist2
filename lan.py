import cv2
import cvlib as cv
from tkinter import *
import time
import threading
import webbrowser
import os
import sys

def start_face_detection():
    global face_detected, face_not_detected_start_time, mode, detection_thread
    video_capture = cv2.VideoCapture(0)
    face_not_detected_start_time = None
    face_detected = False
    timeout_duration = 3  # Timeout duration in seconds

    while video_capture.isOpened() and mode != "Kapalı":
        ret, frame = video_capture.read()

        # Yüz tespiti
        faces, confidences = cv.detect_face(frame)

        # Yüz tespiti başarılı mı değil mi kontrolü ve yazdırma
        if faces:
            print("Yüz tespiti başarılı!")
            face_detected = True
            face_not_detected_start_time = None  # Reset timer if face is detected
        else:
            if face_detected:
                print(f"Yüz tespiti başarısız ({timeout_duration})")
                face_detected = False

            # If face is not detected, start or update the timer
            if face_not_detected_start_time is None:
                face_not_detected_start_time = time.time()
            else:
                elapsed_time = time.time() - face_not_detected_start_time
                remaining_time = max(0, round(timeout_duration - elapsed_time))
                print(f"Yüz tespiti başarısız ({remaining_time})")

                if mode == "Normal" and elapsed_time >= timeout_duration:
                    print(f"Yüz tespiti {timeout_duration} saniye boyunca başarısız oldu. Program kapatılıyor.")
                    break
                elif mode == "Katı" and elapsed_time >= timeout_duration:
                    print(f"Yüz tespiti {timeout_duration} saniye boyunca başarısız oldu. Youtube.com açılıyor.")
                    webbrowser.open("https://www.youtube.com")
                    break

    video_capture.release()
    cv2.destroyAllWindows()

def switch_mode():
    global mode, mode_label, detection_thread
    if mode == "Kapalı":
        mode = "Normal"
        mode_label.config(text="Mod: Normal")
        print("Normal moda geçildi")
        detection_thread = threading.Thread(target=start_face_detection)
        detection_thread.start()
    elif mode == "Normal":
        mode = "Katı"
        mode_label.config(text="Mod: Katı")
        print("Katı moda geçildi")
        detection_thread = threading.Thread(target=start_face_detection)
        detection_thread.start()
    else:
        mode = "Kapalı"
        mode_label.config(text="Mod: Kapalı")
        print("Kapalı moda geçildi")

def stop_detection():
    global detection_thread
    if detection_thread and detection_thread.is_alive():
        detection_thread.join()

mode = "Kapalı"
detection_thread = None
mode_file = "mod.txt"  # Dosya adı

def save_mode():
    with open(mode_file, 'w') as file:
        file.write(mode)

def load_saved_mode():
    global mode
    if os.path.exists(mode_file):
        with open(mode_file, 'r') as file:
            mode = file.read().strip()

load_saved_mode()  # Kaydedilen modu yükle

def save_and_exit():
    save_mode()  # Modu kaydet
    os._exit(0)  # Tüm programı kapat

root = Tk()
root.title("Yüz Tanıma Uygulaması")

if mode == "Kapalı":
    mode_label_text = "Mod: Kapalı"
    print("Kapalı moda geçildi")
elif mode == "Normal":
    mode_label_text = "Mod: Normal"
    print("Normal moda geçildi")
    detection_thread = threading.Thread(target=start_face_detection)
    detection_thread.start()
elif mode == "Katı":
    mode_label_text = "Mod: Katı"
    print("Katı moda geçildi")
    detection_thread = threading.Thread(target=start_face_detection)
    detection_thread.start()

mode_label = Label(root, text=mode_label_text)
mode_label.pack()

switch_button = Button(root, text="Mod Değiştir", command=switch_mode)
switch_button.pack()

exit_button = Button(root, text="Kapat", command=save_and_exit)
exit_button.pack()


root.mainloop()
    