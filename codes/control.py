import time
import cv2
from vision import Vision

class CarController:
    def __init__(self, cam_index=0):
        """Inicializa el controlador del carro y la visión."""
        self.vision = Vision(cam_index)
        self.state = "driving"
        self.blue_count = 0
        self.lap_count = 0
        self.prev_blue_detected = False

    def get_largest_object(self, objects):
        """Devuelve el objeto más grande basado en el área."""
        if objects:
            largest = max(objects, key=lambda obj: obj[2] * obj[3])
            x, y, w, h = largest
            center_x = x + w // 2
            return largest, center_x
        return None, None

    def decide_action(self, positions, frame_width):
        """Decide qué acción tomar basado en la detección de colores."""
        red_obj, red_x = self.get_largest_object(positions.get("Red", []))
        green_obj, green_x = self.get_largest_object(positions.get("Green", []))
        blue_obj, blue_x = self.get_largest_object(positions.get("Blue", []))
        orange_obj, orange_x = self.get_largest_object(positions.get("Orange", []))
        pink_obj, pink_x = self.get_largest_object(positions.get("Pink", []))

        if blue_obj and not self.prev_blue_detected:  
            self.blue_count += 1
            print(f"Iniciar vuelta (Blue detected at X={blue_x}) - Blue Count: {self.blue_count}", flush=True)

        self.prev_blue_detected = bool(blue_obj)

        if orange_obj:
            print(f"Terminar vuelta (Orange detected at X={orange_x})", flush=True)

        if self.blue_count >= 4:
            self.lap_count += 1
            self.blue_count = 0
            print(f"Vuelta completada - Total vueltas: {self.lap_count}", flush=True)

        if self.lap_count >= 3 and pink_obj:
            print(f"Estacionarse (Pink detected at X={pink_x} after 3 laps)", flush=True)
            return "Estacionarse"

        action = "turn_right" if red_obj else "turn_left" if green_obj else "drive_straight"
        return action

    def control_motors(self, action):
        """Simula el control de los motores."""
        print(f"Motors: {action}", flush=True)
