import cv2
import signal
import sys
import os
from control import CarController

def signal_handler(sig, frame):
    """Maneja la interrupción con CTRL + C para cerrar correctamente la cámara y el video."""
    if 'car' in globals():
        car.vision.cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def run_car(cam_index=0):
    global car
    car = CarController(cam_index)
    frame_skip = 2
    frame_count = 0

    try:
        # Crear directorio para frames
        save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recorded_frames")
        os.makedirs(save_dir, exist_ok=True)

        while True:
            ret, frame = car.vision.cap.read()
            if not ret:
                break

            if frame_count % frame_skip == 0:
                # Procesar frame y obtener decisiones
                processed_frame, positions = car.vision.process_frame(frame)
                action, color, x_position = car.decide_action(positions, frame.shape[1])
                car.control_motors(action, color, x_position)

                # Guardar frame procesado
                frame_path = os.path.join(save_dir, f'frame_{frame_count:06d}.jpg')
                cv2.imwrite(frame_path, processed_frame)

            frame_count += 1

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if car.vision.cap.isOpened():
            car.vision.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_car()