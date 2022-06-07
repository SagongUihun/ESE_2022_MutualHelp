#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <Arduino_LSM9DS1.h>
#include <MahonyAHRS.h>
#include <MadgwickAHRS.h>
//#include "LowPassFilter.h"
//#include "filters.h"
#define LSM9DS1_M  0x1C // Would be 0x1C if SDO_M is LOW
#define LSM9DS1_AG 0x6A // Would be 0x6A if SDO_AG is LOW

LSM9DS1 imu_s;
Mahony filter;
Madgwick filter2;
int FSR_1 = A1; //analog pin 1
int FSR_11;

#define DECLINATION -8.58 // Declination (degrees) in Boulder, CO.
const float sensorRate = 119.00;

//setup
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
  filter2.begin(sensorRate);

  //Sparkfun
//  if (imu_s.begin() == false) // with no arguments, this uses default addresses (AG:0x6B, M:0x1E) and i2c port (Wire).
//  {
//    Serial.println("Failed to communicate with LSM9DS1.");
//    Serial.println("Double-check wiring.");
//    Serial.println("Default settings in this sketch will " \
//                   "work for an out of the box LSM9DS1 " \
//                   "Breakout, but may need to be modified " \
//                   "if the board jumpers are.");
//    while (1);
//  }
//
//  imu_s.settings.device.commInterface = IMU_MODE_I2C;
//  imu_s.settings.device.agAddress = LSM9DS1_M;
//  imu_s.settings.device.mAddress = LSM9DS1_AG;
//  
//  imu_s.settings.accel.scale = 4; // Set accel range to +/-16g
//  imu_s.settings.gyro.scale = 2000; // Set gyro range to +/-2000dps
//  imu_s.settings.mag.scale = 8; // Set mag range to +/-8Gs
}

void loop()
{
    // Arduino
    float xAcc, yAcc, zAcc;
    float xGyro, yGyro, zGyro;
    
    float roll, pitch, yaw;
    float s_roll, s_pitch, s_yaw;
    float relative_roll, relative_pitch;

//    t_past_a = millis();
    if(IMU.accelerationAvailable()){
      IMU.readAcceleration(xAcc, yAcc, zAcc);
      
    }
    if(IMU.gyroscopeAvailable()){
      IMU.readGyroscope(xGyro, yGyro, zGyro);
    }
//    IMU.readMagneticField(mx, my, mz); 

//    filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);
//    filter.updateIMU(yGyro, xGyro, zGyro, yAcc, xAcc, zAcc);
    filter.updateIMU(xGyro, zGyro, yGyro, xAcc, zAcc, yAcc);
//  
    roll = filter.getRoll();
    pitch = filter.getPitch();
    yaw = filter.getYaw();
//    
    Serial.print("Arduino: ");
    Serial.print(roll);
    Serial.print(" ");
//    Serial.print(pitch);
//    Serial.print(" ");
//    Serial.println(yaw);


////-------------------------------------------------------------------------//
//    // Sparkfun
    float s_xAcc, s_yAcc, s_zAcc;
    float s_xGyro, s_yGyro, s_zGyro;
    float Acc_total;
    
    if ( imu_s.gyroAvailable() )
    {
      imu_s.readGyro();
    }
    
    if ( imu_s.accelAvailable() )
    {
      imu_s.readAccel();
    }


    s_xAcc = imu_s.calcAccel(imu_s.Ax); 
    s_yAcc = imu_s.calcAccel(imu_s.Ay);
    s_zAcc = imu_s.calcAccel(imu_s.Az);
    s_xGyro = imu_s.calcGyro(imu_s.Gx); 
    s_yGyro = imu_s.calcGyro(imu_s.Gy);
    s_zGyro = imu_s.calcGyro(imu_s.Gz);

    filter2.updateIMU(s_yGyro, s_zGyro, s_xGyro, s_yAcc, s_zAcc, s_xAcc);

    s_roll = filter2.getRoll();
    s_pitch = filter2.getPitch();
    s_yaw = filter2.getYaw();

    Serial.print(s_roll);
    Serial.print(" ");
    // FSR
    FSR_11 = analogRead(FSR_1);
    Serial.println(FSR_11);
}
