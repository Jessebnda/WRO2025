import cv2
import time
import signal
import sys
from control import CarController

# Declarar globalmente para acceder desde el handler
car = None
out = None

def signal_handler(sig, frame):
    print("Interrupción detectada, liberando recursos y guardando video...")
    if car and car.vision.cap.isOpened():
        car.vision.cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()
    print("Video guardado en 'output.avi'")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def run_car(cam_index=0):
    global car, out
    car = CarController(cam_index)
    frame_skip = 2  # Procesa cada 2 frames para reducir carga
    frame_count = 0

    # Configurar VideoWriter con codec MJPEG (puedes probar otros)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    frame_width = int(car.vision.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(car.vision.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (frame_width, frame_height))

    try:
        while True:
            ret, frame = car.vision.cap.read()
            if not ret:
                break

            if frame_count % frame_skip == 0:
                processed_frame, positions = car.vision.process_frame(frame)
                action, color, x_position = car.decide_action(positions, frame.shape[1])
                car.control_motors(action, color, x_position)

                # Escribir el frame procesado en el video
                out.write(processed_frame)
                cv2.imshow("Car Controller Vision", processed_frame)

            frame_count += 1

            # Salir si se presiona ESC
            if cv2.waitKey(1) & 0xFF == 27:
                print("Tecla ESC detectada, finalizando...")
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if car and car.vision.cap.isOpened():
            car.vision.cap.release()
        if out is not None:
            out.release()
        cv2.destroyAllWindows()
        print("Video guardado en 'output.avi'")

if __name__ == "__main__":
    run_car()
