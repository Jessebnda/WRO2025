import cv2
from control import CarController
from vision import Vision

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
            # Recreate the Vision object to ensure proper initialization of the new camera
            car.vision.cap.release()
            car.vision = Vision(CAMERAS[current_cam])
            print(f"Cambiando a cámara {current_cam}")

        # Procesar triángulos cada PROCESS_EVERY_N_FRAMES frames
        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            processed_frame, masks, positions = car.vision.process_frame(frame)
            cv2.imshow("Car Controller Vision", processed_frame)
        else:
            cv2.imshow("Car Controller Vision", frame)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == 27:  # Salir con ESC
            break

    car.vision.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_car()
