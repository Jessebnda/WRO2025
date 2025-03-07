import cv2
from control import CarController

def run_car(cam_index=0):
    car = CarController(cam_index)

    while True:
        ret, frame = car.vision.cap.read()
        if not ret:
            print("DEBUG: No frame captured", flush=True)
            break

        processed_frame, masks, positions = car.vision.process_frame(frame)
        action = car.decide_action(positions, frame.shape[1])
        car.control_motors(action)
        cv2.imshow("Car Controller Vision", processed_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    car.vision.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_car()