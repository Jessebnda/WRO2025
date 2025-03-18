import cv2
import time
from controlPI import CarController

def run_car(cam_index=0):
    car = CarController(cam_index)
    frame_skip = 2  # Ajusta según tus necesidades
    frame_count = 0

    # Configurar VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Puedes probar también 'XVID'
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

                # Escribir el frame procesado al video
                out.write(processed_frame)
                # Opcional: muestra el frame si lo deseas para debug
                cv2.imshow("Car Controller Vision", processed_frame)

            frame_count += 1

            if cv2.waitKey(1) & 0xFF == 27:
                break

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        car.vision.cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_car()
