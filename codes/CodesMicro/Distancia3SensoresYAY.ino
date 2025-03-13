#include <Wire.h>
#include <VL53L0X.h>
#include <MPU6050.h>

MPU6050 mpu;
VL53L0X sensor1;
VL53L0X sensor2;
VL53L0X sensor3;

#define XSHUT_1 2  // Pin para XSHUT del sensor 1
#define XSHUT_2 3  // Pin para XSHUT del sensor 2
#define XSHUT_3 4  // Pin para XSHUT del sensor 3

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // Inicializar MPU-6050
  /*
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("Error en el MPU-6050");
    while (1);
  }
*/
  // Configurar VL53L0X con direcciones únicas
  pinMode(XSHUT_1, OUTPUT);
  pinMode(XSHUT_2, OUTPUT);
  pinMode(XSHUT_3, OUTPUT);

  digitalWrite(XSHUT_1, LOW);
  digitalWrite(XSHUT_2, LOW);
  digitalWrite(XSHUT_3, LOW);
  delay(10);

  digitalWrite(XSHUT_1, HIGH);
  delay(10);
  sensor1.init();
  sensor1.setAddress(0x30);  // Nueva dirección para sensor 1

  digitalWrite(XSHUT_2, HIGH);
  delay(10);
  sensor2.init();
  sensor2.setAddress(0x31);  // Nueva dirección para sensor 2

  digitalWrite(XSHUT_3, HIGH);
  delay(10);
  sensor3.init();
  sensor3.setAddress(0x32);  // Nueva dirección para sensor 3

  sensor1.startContinuous();
  sensor2.startContinuous();
  sensor3.startContinuous();
}

void loop() {
  // Leer datos del MPU-6050
 /* int16_t gx, gy, gz;
  mpu.getRotation(&gx, &gy, &gz);

  Serial.print("Giro: X=");
  Serial.print(gx);
  Serial.print(" | Y=");
  Serial.print(gy);
  Serial.print(" | Z=");
  Serial.println(gz);
*/
  // Leer distancias de los 3 VL53L0X
  Serial.print("VL53L0X #1: ");
  Serial.print(sensor1.readRangeContinuousMillimeters());
  Serial.print(" mm | VL53L0X #2: ");
  Serial.print(sensor2.readRangeContinuousMillimeters());
  Serial.print(" mm | VL53L0X #3: ");
  Serial.print(sensor3.readRangeContinuousMillimeters());
  Serial.println(" mm");

  delay(100);
}

