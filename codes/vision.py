import cv2
import numpy as np

class Vision:
    def __init__(self, cam_index=0):
        """Inicializa la cámara y define los rangos de colores."""
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Mejor resolución para Raspberry Pi
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.kernel = np.ones((3, 3), np.uint8)  # Se reduce de (5,5) a (3,3) para eficiencia

        # Rango de colores HSV
        self.lower_red1, self.upper_red1 = np.array([0, 150, 100]), np.array([10, 255, 255])
        self.lower_red2, self.upper_red2 = np.array([170, 150, 100]), np.array([180, 255, 255])
        self.lower_green,self.upper_green = np.array([40, 80, 50]), np.array([80, 255, 255])
        self.lower_pink, self.upper_pink = np.array([140, 100, 100]), np.array([170, 255, 255])
        self.lower_blue, self.upper_blue = np.array([100, 150, 50]), np.array([130, 255, 255])
        self.lower_orange, self.upper_orange = np.array([10, 150, 100]), np.array([25, 255, 255])

        self.color_map = {  
            "Red": (0, 0, 255),
            "Green": (0, 255, 0),
            "Pink": (255, 0, 255),
            "Blue": (255, 0, 0),
            "Orange": (0, 165, 255)
        }

    def process_color(self, frame, mask, color_name):
        """Encuentra contornos y devuelve posiciones solo si hay suficientes píxeles activados."""
        if np.sum(mask) < 10000:  # Si hay pocos píxeles, omitir procesamiento
            return []

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        gray = cv2.GaussianBlur(mask, (3, 3), 0)  # Suavizar antes de Canny
        edges = cv2.Canny(gray, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        objects = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:  # Se aumentó el umbral para evitar ruido
                x, y, w, h = cv2.boundingRect(cnt)
                objects.append((x, y, w, h))

                # Dibujar caja delimitadora
                cv2.rectangle(frame, (x, y), (x + w, y + h), self.color_map[color_name], 2)
                cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color_map[color_name], 2)

        return objects

    def process_frame(self, frame):
        """Detecta colores y devuelve las posiciones sin procesar toda la imagen después."""
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Máscaras de color
        masks = {
            "Red": cv2.inRange(hsv, self.lower_red1, self.upper_red1) | cv2.inRange(hsv, self.lower_red2, self.upper_red2),
            "Green": cv2.inRange(hsv, self.lower_green, self.upper_green),
            "Pink": cv2.inRange(hsv, self.lower_pink, self.upper_pink),
            "Blue": cv2.inRange(hsv, self.lower_blue, self.upper_blue),
            "Orange": cv2.inRange(hsv, self.lower_orange, self.upper_orange)
        }

        positions = {}
        for color in masks.keys():
            positions[color] = self.process_color(frame, masks[color], color)

        return frame, positions  # Eliminamos las máscaras si ya no son necesarias
