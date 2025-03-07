import cv2
from control import CarController
from vision import Vision

# Use only one camera, the connected one.
CAMERA_INDEX = 0  

# Parámetros de control
PROCESS_EVERY_N_FRAMES = 5  # Cada cuántos frames se procesa la imagen

def run_car():
    car = CarController(CAMERA_INDEX)
    frame_count = 0

    while True:
        ret, frame = car.vision.cap.read()
        if not ret:
            print("DEBUG: No frame captured", flush=True)
            break

        # Procesar la imagen cada PROCESS_EVERY_N_FRAMES frames
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
