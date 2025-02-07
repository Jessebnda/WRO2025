import cv2
import numpy as np

class Vision:
    def __init__(self, cam_index=0):
        # Inicializar la cámara
        self.cap = cv2.VideoCapture(cam_index)
        self.kernel = np.ones((5, 5), np.uint8)
        
        # Rangos de color para rojo (se necesitan dos rangos)
        self.lower_red1 = np.array([0, 120, 70])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 120, 70])
        self.upper_red2 = np.array([180, 255, 255])
        
        # Rango de color para verde
        self.lower_green = np.array([36, 100, 100])
        self.upper_green = np.array([86, 255, 255])
        
        # Umbral para determinar si hay presencia significativa del color en la máscara
        self.pixel_threshold = 1000

    def process_color(self, frame, mask, color_name, draw_color, min_area=500):
        positions = []
        if cv2.countNonZero(mask) > self.pixel_threshold:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(cnt)
                    positions.append((x, y, w, h))
                    cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
                    cv2.putText(frame, color_name, (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, draw_color, 2)
        return frame, positions

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask_red1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask_red2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask_red = mask_red1 | mask_red2
        mask_green = cv2.inRange(hsv, self.lower_green, self.upper_green)

        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, self.kernel)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, self.kernel)

        frame, red_positions = self.process_color(frame, mask_red, "Red", (0, 0, 255))
        frame, green_positions = self.process_color(frame, mask_green, "Green", (0, 255, 0))

        positions = {"Red": red_positions, "Green": green_positions}
        return frame, mask_red, mask_green, positions
