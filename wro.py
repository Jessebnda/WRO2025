import cv2
import numpy as np

def main():
    # Open the webcam (use 0 for default camera, or replace with a video file path)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        # Convert the frame from BGR to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # ----------- Define color ranges for red -----------
        # Red often requires splitting into two ranges in HSV
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        # Create masks for the two red ranges
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = mask_red1 | mask_red2  # Combine both masks

        # ----------- Define color range for green -----------
        lower_green = np.array([36, 100, 100])
        upper_green = np.array([86, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # Apply morphological operations to remove noise (optional but often helpful)
        kernel = np.ones((5, 5), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

        # ----------- Find contours for red -----------
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours_red:
            area = cv2.contourArea(cnt)
            # Filter out small objects by area
            if area > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw red bounding box

        # ----------- Find contours for green -----------
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours_green:
            area = cv2.contourArea(cnt)
            if area > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw green bounding box

        # Display the result
        cv2.imshow("Frame", frame)
        cv2.imshow("Red Mask", mask_red)
        cv2.imshow("Green Mask", mask_green)

        # Exit on pressing the 'ESC' key
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
