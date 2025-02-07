import time
import cv2
from vision import Vision  # Importamos la clase Vision

class CarController:
    def __init__(self, cam_index=0):
        """
        Inicializa la clase CarController, conectándose a Vision y estableciendo el estado inicial.
        """
        self.vision = Vision(cam_index)
        self.state = "driving"

    def decide_action(self, positions, frame_width):
        """
        Decide la acción del carro en función de la posición del obstáculo más cercano.
        - Prioriza los objetos más grandes (suponiendo que están más cerca).
        """
        print("DEBUG: Positions received ->", positions, flush=True)  # Depuración

        def get_largest_object(objects):
            return max(objects, key=lambda obj: obj[2] * obj[3]) if objects else None

        red_obj = get_largest_object(positions["Red"])
        green_obj = get_largest_object(positions["Green"])
        obj = red_obj if red_obj else green_obj

        if obj:
            x, y, w, h = obj
            obstacle_center = x + w / 2
            if obstacle_center < frame_width / 2:
                action = "turn_right"
            else:
                action = "turn_left"
            color_detected = "Red" if obj == red_obj else "Green"
        else:
            action = "drive_straight"
            color_detected = "None"

        print(f"Detected: {color_detected} | Action: {action}", flush=True)
        return action

    def control_motors(self, action):
        """
        Simula el control de los motores con `time.sleep()` para ralentizar las impresiones.
        """
        print("DEBUG: control_motors called with action ->", action, flush=True)
        if action == "drive_straight":
            print("Motors: driving straight", flush=True)
        elif action == "turn_left":
            print("Motors: turning left", flush=True)
        elif action == "turn_right":
            print("Motors: turning right", flush=True)
        elif action == "parking":
            print("Motors: parking the car", flush=True)
        else:
            print("Motors: unknown action", flush=True)

        time.sleep(1.5)  # Ajusta este tiempo según lo que necesites
