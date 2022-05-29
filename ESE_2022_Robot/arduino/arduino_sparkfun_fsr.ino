#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <Arduino_LSM9DS1.h>
#include <MahonyAHRS.h>
#include <MadgwickAHRS.h>
#include <ArduinoBLE.h>

//UUID setting
BLEService IMUService("6e400001-b5a3-f393-e0a9-e50e24dcca9e");
// Characteristic setting 
BLEIntCharacteristic IMUxACC("6e400002-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUyACC("6e400003-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUzACC("6e400004-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUxGYro("6e400005-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUyGYro("6e400006-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUzGYro("6e400007-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUxMag("6e400008-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUyMag("6e400009-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUzMag("6e400010-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMURoll("6e400011-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUPitch("6e400012-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUYaw("6e400013-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );

BLEIntCharacteristic IMUxACC("6e400014-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUyACC("6e400015-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUzACC("6e400016-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUxGYro("6e400017-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUyGYro("6e400018-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUzGYro("6e400019-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUxMag("6e400020-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUyMag("6e400021-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUzMag("6e400022-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMURoll("6e400023-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUPitch("6e400024-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUYaw("6e400025-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );

BLEIntCharacteristic FSR1("6e400026-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic FSR2("6e400027-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );


LSM9DS1 imu_s;
Mahony filter;
Madgwick filter2;

int FSR_0 = A2; //analog pin 2
int FSR_1 = A1; //analog pin 1

#define PRINT_CALCULATED
#define PRINT_SPEED 250 // 250 ms between prints
static unsigned long lastPrint = 0; // Keep track of print time
#define DECLINATION -8.58 // Declination (degrees) in Boulder, CO.

const float sensorRate = 119.00;
int FSR_00, FSR_11;

// Arduino
float xAcc, yAcc, zAcc;
float xGyro, yGyro, zGyro, bef_xGyro, bef_zAcc;

float roll, pitch, yaw;
float r, p, y;

void printAttitude(float ax, float ay, float az, float mx, float my, float mz, float roll, float pitch, float yaw);

BLEDevice central = BLE.central();

void setup()
{
  Serial.begin(115200);

  Wire.begin();
  
  //Arduino
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    while (true);
  }
  filter.begin(sensorRate);

  //Sparkfun
  if (imu_s.begin() == false) // with no arguments, this uses default addresses (AG:0x6B, M:0x1E) and i2c port (Wire).
  {
    Serial.println("Failed to communicate with LSM9DS1.");
    Serial.println("Double-check wiring.");
    Serial.println("Default settings in this sketch will " \
                   "work for an out of the box LSM9DS1 " \
                   "Breakout, but may need to be modified " \
                   "if the board jumpers are.");
    while (1);
  }

  BLE.setLocalName("Thanos_Glove");
  BLE.setAdvertisedService(IMUService); 
  IMUService.addCharacteristic(IMUxACC);
  IMUService.addCharacteristic(IMUyACC);
  IMUService.addCharacteristic(IMUzACC);
  IMUService.addCharacteristic(IMUxGYro);
  IMUService.addCharacteristic(IMUyGYro);
  IMUService.addCharacteristic(IMUzGYro);
  IMUService.addCharacteristic(IMUxMag);
  IMUService.addCharacteristic(IMUyMag);
  IMUService.addCharacteristic(IMUzMag);
  IMUService.addCharacteristic(IMURoll);
  IMUService.addCharacteristic(IMUPitch);
  IMUService.addCharacteristic(IMUYaw);
  
  IMUService.addCharacteristic(IMU2xACC);
  IMUService.addCharacteristic(IMU2yACC);
  IMUService.addCharacteristic(IMU2zACC);
  IMUService.addCharacteristic(IMU2xGYro);
  IMUService.addCharacteristic(IMU2yGYro);
  IMUService.addCharacteristic(IMU2zGYro);
  IMUService.addCharacteristic(IMU2xMag);
  IMUService.addCharacteristic(IMU2yMag);
  IMUService.addCharacteristic(IMU2zMag);
  IMUService.addCharacteristic(IMU2Roll);
  IMUService.addCharacteristic(IMU2Pitch);
  IMUService.addCharacteristic(IMU2Yaw);
  
  IMUService.addCharacteristic(FSR1);
  IMUService.addCharacteristic(FSR2);
 
  BLE.addService(IMUService);

  BLE.advertise();
}

void loop()
{
  //imu1 
  IMU.readAcceleration(xAcc, yAcc, zAcc);
  IMU.readGyroscope(xGyro, yGyro, zGyro);
  //IMU.readMagneticField(mx, my, mz); 

  //filter.update(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc, mx, my, mz);
  filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);

  roll = filter.getRoll();
  pitch = filter.getPitch();
  yaw = filter.getYaw();

  //imu2
  r = atan2(ay, az);
  p = atan2(-ax, sqrt(ay * ay + az * az));
  if (my == 0)
      y = (mx < 0) ? PI : 0;
    else
      y = atan2(mx, my);
  
    y -= DECLINATION * PI / 180;
  
    if (y > PI) y -= (2 * PI);
    else if (y < -PI) y += (2 * PI);
  
    // Convert everything from radians to degrees:
    r *= 180.0 / PI;
    p *= 180.0 / PI;
    y  *= 180.0 / PI;

//-------------------------------------------------------------------------//
  // Sparkfun
  if ( imu_s.gyroAvailable() )
  {
    imu_s.readGyro();
  }
  if ( imu_s.accelAvailable() )
  {
    imu_s.readAccel();
  }
  if ( imu_s.magAvailable() )
  {
    imu_s.readMag();
  }

  //Sparkfun
 
  //printAttitude(imu_s.Ax, imu_s.Ay, imu_s.Az, -imu_s.My, -imu_s.Mx, imu_s.Mz, roll, pitch, yaw);
  FSR_00 = analogRead(FSR_0); 
  FSR_11 = analogRead(FSR_1);  

//-------------------------------------------------------------------------//
/*쓰기*/
        IMUxACC.writeValue((int)100 * xAcc);
        IMUyACC.writeValue((int)100 * yAcc);
        IMUzACC.writeValue((int)100 * zAcc);
        IMUxGYro.writeValue((int)100 * xGyro);
        IMUyGYro.writeValue((int)100 * yGyro);
        IMUzGYro.writeValue((int)100 * zGyro);
        IMUxMag.writeValue((int)100 * mx);
        IMUyMag.writeValue((int)100 * my);
        IMUzMag.writeValue((int)100 * mz);
        IMURoll.writeValue((int)100 * roll);
        IMUPitch.writeValue((int)100 * pitch);
        IMUYaw.writeValue((int)100 * yaw);

        IMU2xACC.writeValue((int)100 * imu_s.Ax);
        IMU2yACC.writeValue((int)100 * imu_s.Ay);
        IMU2zACC.writeValue((int)100 * imu_s.Az);
        IMU2xGYro.writeValue((int)100 * imu_s.Gx);
        IMU2yGYro.writeValue((int)100 * imu_s.Gy);
        IMU2zGYro.writeValue((int)100 * imu_s.Gz);
        IMU2xMag.writeValue((int)100 * -imu_s.My);
        IMU2yMag.writeValue((int)100 * imu_s.Mx);
        IMU2zMag.writeValue((int)100 * imu_s.Mx);
        IMU2Roll.writeValue((int)100 * r);
        IMU2Pitch.writeValue((int)100 * p);
        IMU2Yaw.writeValue((int)100 * y);

        FSR1.writeValue(FSR_00)
        FSR2.writeValue(FSR_11)
        

//monitoring
//  Serial.print("A0: ");
  Serial.print(FSR_00);
  Serial.print(" ");
  Serial.println(FSR_11);
}

//-------------------------------------------------------------------------------------//
////
//void printAttitude(float ax, float ay, float az, float mx, float my, float mz, float roll, float pitch, float yaw)
//{
//  float r = atan2(ay, az);
//  float p = atan2(-ax, sqrt(ay * ay + az * az));
//  float y;
//  if (my == 0)
//    y = (mx < 0) ? PI : 0;
//  else
//    y = atan2(mx, my);
//
//  y -= DECLINATION * PI / 180;
//
//  if (y > PI) y -= (2 * PI);
//  else if (y < -PI) y += (2 * PI);
//
//  // Convert everything from radians to degrees:
//  r *= 180.0 / PI;
//  p *= 180.0 / PI;
//  y  *= 180.0 / PI;
//
//
//  Serial.print(roll-r);
//  Serial.print(" ");
//  Serial.print(pitch-p);
//  Serial.print(" ");
//  Serial.print(yaw-y);
//
  
}
