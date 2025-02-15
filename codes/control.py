import time
import cv2
from vision import Vision

class CarController:
    def __init__(self, cam_index=0):
        """Initializes the CarController and connects to the Vision system."""
        self.vision = Vision(cam_index)
        self.state = "driving"
        self.blue_count = 0
        self.lap_count = 0

    def decide_action(self, positions, frame_width):
        """Decides the action based on detected objects."""
        def get_largest_object(objects):
            return max(objects, key=lambda obj: obj[2] * obj[3]) if objects else None

        # Get detected objects
        red_obj = get_largest_object(positions["Red"])
        green_obj = get_largest_object(positions["Green"])
        blue_obj = get_largest_object(positions["Blue"])
        orange_obj = get_largest_object(positions["Orange"])
        pink_obj = get_largest_object(positions["Pink"])

        # **Lap Tracking Logic**
        if blue_obj:
            self.blue_count += 1
            print(f"Iniciar vuelta (Blue detected) - Blue Count: {self.blue_count}", flush=True)

        if orange_obj:
            print("Terminar vuelta (Orange detected)", flush=True)

        if self.blue_count >= 4:
            self.lap_count += 1
            self.blue_count = 0
            print(f"Vuelta completada - Total vueltas: {self.lap_count}", flush=True)

        if self.lap_count >= 3 and pink_obj:
            print("Estacionarse (Pink detected after 3 laps)", flush=True)

        # **Traffic Sign Decision**
        obj = red_obj if red_obj else green_obj  # Prioritize the first detected object

        if obj:
            x, y, w, h = obj
            action = "turn_right" if obj == red_obj else "turn_left"
            color_detected = "Red" if obj == red_obj else "Green"
        else:
            action = "drive_straight"
            color_detected = "None"

        print(f"Detected: {color_detected} | Action: {action} | Vueltas: {self.lap_count}", flush=True)
        return action

    def control_motors(self, action):
        """Simulates motor control with a delay to prevent excessive printing."""
        print(f"Motors: {action}", flush=True)
        time.sleep(0)
