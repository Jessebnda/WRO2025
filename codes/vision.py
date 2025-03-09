import cv2
import numpy as np

class Vision:
    def __init__(self, cam_index=0):
        """Inicializa la cámara y define los rangos de colores."""
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reducir resolución para mejor rendimiento
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Definir los rangos de colores en HSV con NumPy
        self.color_ranges = {
            "Red": [(np.array([0, 150, 100]), np.array([10, 255, 255])),
                    (np.array([170, 150, 100]), np.array([180, 255, 255]))],
            "Green": [(np.array([40, 80, 50]), np.array([80, 255, 255]))],
            "Pink": [(np.array([140, 100, 100]), np.array([170, 255, 255]))],
            #"Blue": [(np.array([100, 150, 50]), np.array([130, 255, 255]))],
            #"Orange": [(np.array([10, 150, 100]), np.array([25, 255, 255]))]
        }

        self.kernel = np.ones((3, 3), np.uint8)  # Kernel más pequeño para eficiencia

    def process_color(self, frame, mask, color_name):
        """Encuentra contornos y devuelve posiciones."""
        if np.count_nonzero(mask) < 10000:  # Usar NumPy para contar píxeles activados
            return []

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        objects = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:  # Filtrar ruido
                x, y, w, h = cv2.boundingRect(cnt)
                objects.append((x, y, w, h))

                # Dibujar caja delimitadora
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return objects

    def process_frame(self, frame):
        """Detecta colores optimizado con NumPy."""
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Aplicar máscaras con NumPy en una sola operación
        masks = {color: np.bitwise_or.reduce([cv2.inRange(hsv, lower, upper) for lower, upper in ranges])
                 for color, ranges in self.color_ranges.items()}

        positions = {color: self.process_color(frame, mask, color) for color, mask in masks.items()}

        return frame, positions
