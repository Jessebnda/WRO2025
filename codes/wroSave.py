import cv2
import os
import sys
import signal
from controlPI import CarController

OUTPUT_PATH = "output.avi"
FPS = 5.0         # Ajusta según tu frame_skip y velocidad real de captura
FRAME_SKIP = 2    # Procesar 1 de cada 2 frames

car = None
out = None
write_count = 0

def signal_handler(sig, frame):
    """Maneja CTRL+C"""
    print("\nInterrupción detectada → cerrando cámara y guardando video…")
    cleanup_and_report()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def cleanup_and_report():
    global car, out, write_count
    if car and car.vision.cap.isOpened():
        car.vision.cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

    if write_count > 0 and os.path.exists(OUTPUT_PATH):
        size = os.path.getsize(OUTPUT_PATH)
        print(f"✅ Video guardado correctamente → '{OUTPUT_PATH}'")
        print(f"   • Frames escritos: {write_count}")
        print(f"   • Tamaño del archivo: {size:,} bytes")
    else:
        print(f"❌ No se grabó ningún frame. El archivo '{OUTPUT_PATH}' está vacío o no existe.")

def run_car(cam_index=0):
    global car, out, write_count

    # Avisar si existe el archivo previo
    if os.path.exists(OUTPUT_PATH):
        print(f"⚠️  '{OUTPUT_PATH}' ya existe — será sobrescrito")

    car = CarController(cam_index)
    width  = int(car.vision.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(car.vision.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(OUTPUT_PATH, fourcc, FPS, (width, height))
    if not out.isOpened():
        print("❌ Error: no se pudo abrir VideoWriter (codec no soportado?)")
        sys.exit(1)

    frame_count = 0

    try:
        while True:
            ret, frame = car.vision.cap.read()
            if not ret:
                break

            if frame_count % FRAME_SKIP == 0:
                processed_frame, positions = car.vision.process_frame(frame)
                action, color, x_pos = car.decide_action(positions, frame.shape[1])
                car.control_motors(action, color, x_pos)

                out.write(processed_frame)
                write_count += 1
                cv2.imshow("Vision", processed_frame)

            frame_count += 1

            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                print("ESC presionado → terminando captura")
                break

    except Exception as e:
        print(f"❌ Excepción: {e}")
    finally:
        cleanup_and_report()

if __name__ == "__main__":
    run_car()
