import time
import cv2
from vision import Vision

class CarController:
    def __init__(self, cam_index=0):
        """Inicializa el controlador del carrito y la visión."""
        self.vision = Vision(cam_index)
        self.state = "driving"

    def decide_action(self, positions, frame_width):
        """Decide la acción basada en la posición del objeto detectado."""
        def get_largest_object(objects):
            return max(objects, key=lambda obj: obj[2] * obj[3]) if objects else None

        red_obj = get_largest_object(positions["Red"])
        green_obj = get_largest_object(positions["Green"])
        obj = red_obj if red_obj else green_obj

        if obj:
            x, y, w, h, position_value = obj
            if red_obj:
                action = "turn_right"
            else:
                action = "turn_left"
            color_detected = "Red" if red_obj else "Green"
        else:
            action = "drive_straight"
            position_value = 0
            color_detected = "None"

        print(f"Detected: {color_detected} | Position: {position_value} | Action: {action}", flush=True)
        return action

    def control_motors(self, action):
        """Simula el control de los motores y agrega una pausa para evitar spam en la terminal."""
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

        time.sleep(1.5)  # Control de tiempo para evitar impresión rápida
