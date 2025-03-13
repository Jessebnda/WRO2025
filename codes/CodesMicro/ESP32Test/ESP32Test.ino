#include <Wire.h>
#include <VL53L0X.h>
#include <MPU6050_tockn.h>

// Pines XSHUT (Usamos GPIOs seguros en ESP32)
#define XSHUT_1 25  
#define XSHUT_2 26  
#define XSHUT_3 27  

// Pines de entrada y salida
#define SENSOR_PIN 34  // GPIO 34 es solo entrada en ESP32
#define V 13  // LED en GPIO 13

MPU6050 gyro(Wire);
VL53L0X sensor1, sensor2, sensor3;

int valor = 0;  // Posición del objeto otorgado por la Raspberry Pi

void setup() {
    Serial.begin(115200);
    Wire.begin(21, 22);  // ESP32 usa SDA 21 y SCL 22 por defecto

    inicializarMPU();
    configurarVL53L0X();
    
    pinMode(SENSOR_PIN, INPUT);
    pinMode(V, OUTPUT);
}

void loop() {
    int posicion;
    leerMPU();
    leerSensoresVL53L0X();
    posicion = ColorPosicion();
    delay(100);
}

void inicializarMPU() {
    gyro.begin();
    gyro.calcGyroOffsets(true);
}

void configurarVL53L0X() {
    const int xshut_pins[] = {XSHUT_1, XSHUT_2, XSHUT_3};
    VL53L0X* sensores[] = {&sensor1, &sensor2, &sensor3};
    const uint8_t direcciones[] = {0x30, 0x31, 0x32};

    for (int i = 0; i < 3; i++) {
        pinMode(xshut_pins[i], OUTPUT);
        digitalWrite(xshut_pins[i], LOW);
    }
    delay(10);

    for (int i = 0; i < 3; i++) {
        digitalWrite(xshut_pins[i], HIGH);
        delay(10);
        sensores[i]->init();
        sensores[i]->setAddress(direcciones[i]);
        sensores[i]->startContinuous();
    }
}

int ColorPosicion() {
    int estado = digitalRead(SENSOR_PIN);  // Leer el estado del pin de entrada

    if (estado == HIGH) {
        Serial.println("¡Señal recibida! La Raspberry detectó verde.");
        digitalWrite(V, HIGH);
    } else {
        Serial.println("No hay nada.");
        digitalWrite(V, LOW);
    }

    if (Serial.available() > 0) {  // Si hay datos disponibles en el puerto serial
        String posicion = Serial.readStringUntil('\n');  
        valor = posicion.toInt();  
        digitalWrite(V, LOW);
        Serial.print("Valor recibido: ");
        Serial.println(valor);
    } else {
        digitalWrite(V, HIGH);
    }
    return valor;
}

void leerMPU() {
    gyro.update();
    float angleZ = gyro.getAngleZ();
    Serial.print("Grados: "); 
    Serial.print(angleZ);
}

void leerSensoresVL53L0X() {
    Serial.print(" | VL53L0X #1: "); Serial.print(sensor1.readRangeContinuousMillimeters());
    Serial.print(" mm | VL53L0X #2: "); Serial.print(sensor2.readRangeContinuousMillimeters());
    Serial.print(" mm | VL53L0X #3: "); Serial.print(sensor3.readRangeContinuousMillimeters());
    Serial.println(" mm");
}
