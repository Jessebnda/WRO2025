import cv2
import matplotlib.pyplot as plt

img = cv2.imread("imagen.jpg")

if img is None:
    print("❌ No se pudo cargar la imagen.")
else:
    print(f"✅ Dimensiones detectadas: {img.shape}")
    
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")  # Quitar ejes
    plt.show()
