import cv2
import threading
from queue import Queue
from control import CarController

def capture_frame(vision, frame_queue):
    """Captura los frames de la cámara en un hilo separado y los coloca en la cola."""
    while True:
        ret, frame = vision.cap.read()
        if not ret:
            print("DEBUG: No frame captured", flush=True)
            break
        
        # Coloca el frame capturado en la cola para que el hilo principal lo procese
        frame_queue.put(frame)

def process_frame_and_control(car, frame_queue):
    """Procesa los frames desde la cola y realiza las acciones correspondientes."""
    frame_skip = 2  # Procesa cada 2 frames
    frame_count = 0

    while True:
        if not frame_queue.empty():  # Solo procesar si hay un frame en la cola
            frame = frame_queue.get()

            if frame_count % frame_skip == 0:  # Procesa solo cada 2 frames
                processed_frame, positions = car.vision.process_frame(frame)
                action = car.decide_action(positions, frame.shape[1])
                car.control_motors(action)
                cv2.imshow("Car Controller Vision", processed_frame)

            frame_count += 1

            # Salir si se presiona 'Esc'
            if cv2.waitKey(1) & 0xFF == 27:
                break

    # Liberar los recursos de la cámara y cerrar las ventanas
    car.vision.cap.release()
    cv2.destroyAllWindows()

def run_car(cam_index=0):
    car = CarController(cam_index)
    frame_queue = Queue()  # Cola para comunicar entre hilos

    # Crear y comenzar el hilo de captura de frames
    capture_thread = threading.Thread(target=capture_frame, args=(car.vision, frame_queue))
    capture_thread.start()

    # Procesar los frames y controlar el carro en el hilo principal
    process_frame_and_control(car, frame_queue)

    # Esperar a que el hilo de captura termine (opcional, dependiendo de cómo manejes el hilo de captura)
    capture_thread.join()

if __name__ == "__main__":
    run_car()
