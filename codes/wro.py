import cv2
import RPi.GPIO as GPIO
from control import CarController

# Pines GPIO para la señal a Arduino (opcional)
RED_PIN = 17
GREEN_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

# Lista de índices de cámaras disponibles (ajusta según tu hardware)
CAMERAS = [0, 1]
current_cam = 0  # Cámara inicial

# Parámetros de control
SWITCH_CAMERA_FRAMES = 100  # Cada cuántos frames cambia la cámara
PROCESS_EVERY_N_FRAMES = 5  # Cada cuántos frames se procesan los triángulos

def run_car():
    global current_cam
    car = CarController(CAMERAS[current_cam])
    frame_count = 0

    while True:
        ret, frame = car.vision.cap.read()
        if not ret:
            print("DEBUG: No frame captured", flush=True)
            break

        # Alternar cámara cada SWITCH_CAMERA_FRAMES frames
        if frame_count % SWITCH_CAMERA_FRAMES == 0:
            current_cam = (current_cam + 1) % len(CAMERAS)  # Cambiar cámara
            car.vision.cap.release()
            car.vision.cap = cv2.VideoCapture(CAMERAS[current_cam])
            car.vision.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            car.vision.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            print(f" Cambiando a cámara {current_cam}")

        # Procesar triángulos cada PROCESS_EVERY_N_FRAMES frames
        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            processed_frame, masks, positions = car.vision.process_frame(frame)

            # Detectar rojo y verde para enviar señal a Arduino
            red_detected = len(positions["Red"]) > 0
            green_detected = len(positions["Green"]) > 0
            GPIO.output(RED_PIN, GPIO.HIGH if red_detected else GPIO.LOW)
            GPIO.output(GREEN_PIN, GPIO.HIGH if green_detected else GPIO.LOW)

            cv2.imshow("Car Controller Vision", processed_frame)
        else:
            cv2.imshow("Car Controller Vision", frame)  # Mostrar sin procesar

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == 27:  # Salir con ESC
            break

    GPIO.cleanup()
    car.vision.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_car()
