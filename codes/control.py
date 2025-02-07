import time
import cv2
from vision import Vision

class CarController:
    def __init__(self, cam_index=0):
        """Initializes the CarController and connects to the Vision system."""
        self.vision = Vision(cam_index)
        self.state = "driving"

    def decide_action(self, positions, frame_width):
        """Decides the action based on the detected object's size and position."""
        def get_largest_object(objects):
            """Returns the object with the largest area (width * height)."""
            return max(objects, key=lambda obj: obj[2] * obj[3]) if objects else None

        # Get the largest red and green objects
        red_obj = get_largest_object(positions["Red"])
        green_obj = get_largest_object(positions["Green"])

        # If both colors are detected, prioritize the largest object
        if red_obj and green_obj:
            red_area = red_obj[2] * red_obj[3]  # Width * Height
            green_area = green_obj[2] * green_obj[3]
            obj = red_obj if red_area > green_area else green_obj
        else:
            obj = red_obj if red_obj else green_obj  # If only one color is detected

        # Decision based on the largest detected object
        if obj:
            x, y, w, h, position_value = obj
            if obj in positions["Red"]:
                action = "turn_right"
                color_detected = "Red"
            else:
                action = "turn_left"
                color_detected = "Green"
        else:
            action = "drive_straight"
            position_value = 0
            color_detected = "None"

        print(f"Detected: {color_detected} | Position: {position_value} | Action: {action}", flush=True)
        return action

    def control_motors(self, action):
        """Simulates motor control and slows down terminal printing."""
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

        time.sleep(0.3)  # Delay to avoid excessive printing
