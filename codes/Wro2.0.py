import cv2
import numpy as np

def open_camera(source=0):
    """Opens camara and returns videocapture"""
    return cv2.VideoCapture(source)

def process_frame(frame):
    """Detects colors in the frame and returns masks for red and green."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define colors
    lower_red1, upper_red1 = np.array([0, 120, 70]), np.array([10, 255, 255])
    lower_red2, upper_red2 = np.array([170, 120, 70]), np.array([180, 255, 255])
    lower_green, upper_green = np.array([36, 100, 100]), np.array([86, 255, 255])

    # Create masks
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Filter masks
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

    return mask_red, mask_green

def get_position_value(x, frame_width, color):
    """Calcula el valor basado en la posición horizontal del objeto."""
    normalized_x = x / frame_width  # Normalizar entre 0 y 1

    if color == "red":  # Rojo: Izquierda (2000) → Derecha (0)
        return int((1 - normalized_x) * 2000)
    elif color == "green":  # Verde: Izquierda (0) → Derecha (2000)
        return int(normalized_x * 2000)
    return 0

def detect_and_draw_contours(frame, mask, color):
    """Draws contours and calculates values based on the position of the object."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_width = frame.shape[1]  # Obtener el ancho del frame

    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            value = get_position_value(x + w // 2, frame_width, color)  # Centro del objeto

            # Dibujar rectángulo y mostrar valor
            color_bgr = (0, 0, 255) if color == "red" else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
            cv2.putText(frame, f"{value}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_bgr, 2)
            return value

def turnLeft(positionRED):
    print("Turning left")
    pass

def turnRight(positionGREEN):
    print("Turning right")
    pass
    
    

def main():
    cap = open_camera(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        # Procesar el frame
        mask_red, mask_green = process_frame(frame)

        # Dibujar contornos y calcular valores
        positionRED = detect_and_draw_contours(frame, mask_red, "red")
        positionGREEN = detect_and_draw_contours(frame, mask_green, "green")

        # Mostrar camaras
        cv2.imshow("Frame", frame)
        cv2.imshow("Red Mask", mask_red)
        cv2.imshow("Green Mask", mask_green)
        
        print(positionRED, positionGREEN)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()