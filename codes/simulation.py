import pygame
import math
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 800  # Escalado proporcional a 3000x3000 mm
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación WRO 2025 - Carrito Autónomo")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)

# Configuración de la pista
outer_rect = pygame.Rect(50, 50, 700, 700)  # Pista grande
inner_rect = pygame.Rect(150, 150, 500, 500)  # Área de movimiento

# Generar paredes internas aleatorias
num_internal_walls = 3
walls = []
for _ in range(num_internal_walls):
    x = random.randint(inner_rect.left + 50, inner_rect.right - 100)
    y = random.randint(inner_rect.top + 50, inner_rect.bottom - 100)
    width = random.choice([10, 100])
    height = random.choice([100, 10])
    walls.append(pygame.Rect(x, y, width, height))

# Postes (rojos y verdes en posiciones aleatorias)
posts = []
for _ in range(5):
    x = random.randint(inner_rect.left + 50, inner_rect.right - 50)
    y = random.randint(inner_rect.top + 50, inner_rect.bottom - 50)
    color = RED if random.choice([True, False]) else GREEN
    posts.append((color, pygame.Rect(x, y, 20, 20)))

# Zona de estacionamiento
parking_zone = pygame.Rect(inner_rect.right - 100, inner_rect.bottom - 50, 80, 40)

# Configuración del carrito
car_size = (20, 10)
car_x, car_y = 400, 700
car_speed = 2
car_angle = 0  # Dirección en grados
servo_angle = 0  # Ángulo de las llantas (-30° a 30°)

# Contador de vueltas
laps = 0

# Función para obtener distancias a paredes
def get_distances():
    left_distance = car_x - inner_rect.left
    right_distance = inner_rect.right - (car_x + car_size[0])
    back_distance = car_y - inner_rect.top
    return left_distance, right_distance, back_distance

# Función para actualizar el movimiento del carrito
def update_car():
    global car_x, car_y, car_angle, servo_angle, laps

    left_distance, right_distance, back_distance = get_distances()

    # Algoritmo de navegación básico (evitar paredes)
    if left_distance < 50:
        servo_angle = 30  # Gira a la derecha
    elif right_distance < 50:
        servo_angle = -30  # Gira a la izquierda
    else:
        servo_angle = 0  # Sigue recto

    # Contar vueltas
    if car_y < inner_rect.top + 20 and laps < 3:
        laps += 1
        print(f"Vuelta {laps}/3 completada")

    # Si completó 3 vueltas, ir a la zona de estacionamiento
    if laps >= 3:
        target_x, target_y = parking_zone.center
        if abs(car_x - target_x) > 10:
            servo_angle = 30 if car_x < target_x else -30
        else:
            car_speed = 0  # Detenerse
            print("Carrito estacionado")

    # Aplicar movimiento según el ángulo
    car_angle += servo_angle * 0.1
    rad_angle = math.radians(car_angle)
    car_x += car_speed * math.cos(rad_angle)
    car_y += car_speed * math.sin(rad_angle)

# Bucle principal
running = True
while running:
    win.fill(WHITE)

    # Dibujar la pista
    pygame.draw.rect(win, BLACK, outer_rect, 5)  # Bordes de la pista
    pygame.draw.rect(win, BLACK, inner_rect, 3)  # Área de movimiento

    # Dibujar paredes internas
    for wall in walls:
        pygame.draw.rect(win, BLACK, wall)

    # Dibujar postes
    for color, rect in posts:
        pygame.draw.rect(win, color, rect)

    # Dibujar zona de estacionamiento
    pygame.draw.rect(win, MAGENTA, parking_zone)

    # Dibujar carrito
    car_rect = pygame.Rect(car_x, car_y, *car_size)
    pygame.draw.rect(win, BLUE, car_rect)

    # Obtener datos de sensores
    left_distance, right_distance, back_distance = get_distances()
    print(f"Ángulo: {car_angle}°, Servo: {servo_angle}°, Distancia Izq: {left_distance}, Der: {right_distance}, Atrás: {back_distance}")

    # Actualizar movimiento
    update_car()

    pygame.display.update()

    # Eventos de salida
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()