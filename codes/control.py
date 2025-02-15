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
        self.prev_blue_detected = False  # Track if blue was detected in the last frame

    def get_largest_object(self, objects):
        """Returns the largest detected object by area and its center X position."""
        if objects:
            largest = max(objects, key=lambda obj: obj[2] * obj[3])  # Largest by area (width * height)
            x, y, w, h = largest
            center_x = x + w // 2  # Get the center X position
            return largest, center_x
        return None, None

    def decide_action(self, positions, frame_width):
        """Decides the action based on detected objects and prints object positions."""
        red_obj, red_x = self.get_largest_object(positions["Red"])
        green_obj, green_x = self.get_largest_object(positions["Green"])
        blue_obj, blue_x = self.get_largest_object(positions["Blue"])
        orange_obj, orange_x = self.get_largest_object(positions["Orange"])
        pink_obj, pink_x = self.get_largest_object(positions["Pink"])

        # Print position of the largest detected object
        if red_obj:
            print(f"Red Object Detected at X={red_x}", flush=True)
        if green_obj:
            print(f"Green Object Detected at X={green_x}", flush=True)
        if blue_obj:
            print(f"Blue Object Detected at X={blue_x}", flush=True)
        if orange_obj:
            print(f"Orange Object Detected at X={orange_x}", flush=True)
        if pink_obj:
            print(f"Pink Object Detected at X={pink_x}", flush=True)

        # **Lap Tracking Logic (Trigger on Blue Reappearance)**
        if blue_obj and not self.prev_blue_detected:  
            self.blue_count += 1
            print(f"Iniciar vuelta (Blue detected at X={blue_x}) - Blue Count: {self.blue_count}", flush=True)

        self.prev_blue_detected = bool(blue_obj)  # Update previous blue detection state

        if orange_obj:
            print(f"Terminar vuelta (Orange detected at X={orange_x})", flush=True)

        if self.blue_count >= 4:
            self.lap_count += 1
            self.blue_count = 0
            print(f"Vuelta completada - Total vueltas: {self.lap_count}", flush=True)

        # **If 3 laps are completed and pink is detected, set action to "parking"**
        if self.lap_count >= 3 and pink_obj:
            print(f"Estacionarse (Pink detected at X={pink_x} after 3 laps)", flush=True)
            return "Estacionarse"

        # **Traffic Sign Decision (Red → Right, Green → Left)**
        obj = red_obj if red_obj else green_obj

        if obj:
            action = "turn_right" if obj == red_obj else "turn_left"
            color_detected = "Red" if obj == red_obj else "Green"
        else:
            action = "drive_straight"
            color_detected = "None"

        print(f"Detected: {color_detected} | Action: {action} | Vueltas: {self.lap_count}", flush=True)
        return action

    def control_motors(self, action):
        """Simulates motor control, including stopping for parking."""
        print(f"Motors: {action}", flush=True)

        
        time.sleep(0)
