import cv2
from control import CarController

def run_car(cam_index=0, process_every_n_frames=5):
    car = CarController(cam_index)
    frame_count = 0  # Contador de frames

    while True:
        ret, frame = car.vision.cap.read()
        if not ret:
            print("DEBUG: No frame captured", flush=True)
            break

        # Procesar solo cada 'n' frames
        if frame_count % process_every_n_frames == 0:
            processed_frame, masks, positions = car.vision.process_frame(frame)
            action = car.decide_action(positions, frame.shape[1])
            car.control_motors(action)
            cv2.imshow("Car Controller Vision", processed_frame)
        else:
            # Si no es un frame de procesamiento, solo mostrar el frame sin procesar
            cv2.imshow("Car Controller Vision", frame)

        frame_count += 1  # Incrementar contador de frames

        if cv2.waitKey(1) & 0xFF == 27:  # Salir con ESC
            break

    car.vision.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_car()
