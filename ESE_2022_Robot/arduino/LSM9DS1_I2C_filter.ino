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
Madgwick filter3;
//LowPassFilter lpf(0.5, 0.01);
//
//int FSR_0 = A2; //analog pin 2
//int FSR_1 = A1; //analog pin 1

//const float cutoff_freq   = 20.0;  //Cutoff frequency in Hz
//const float sampling_time = 0.005; //Sampling time in seconds.
//IIR::ORDER  order  = IIR::ORDER::OD3; // Order (OD1 to OD4)
//Filter hpf(cutoff_freq, sampling_time, IIR::ORDER::OD2, IIR::TYPE::HIGHPASS);
//Filter lpf2(cutoff_freq, sampling_time, order);

//#define PRINT_CALCULATED
//#define PRINT_SPEED 250 // 250 ms between prints
//static unsigned long lastPrint = 0; // Keep track of print time
#define DECLINATION -8.58 // Declination (degrees) in Boulder, CO.

const float sensorRate = 119.00;

//Function definitions
//void printGyro();
//void printAccel();
//void printMag();
void printAttitude(float ax, float ay, float az, float mx, float my, float mz, float roll, float pitch, float yaw);
void printRPY_Arduino(float ax, float ay, float az);

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

  imu_s.settings.device.commInterface = IMU_MODE_I2C;
  imu_s.settings.device.agAddress = LSM9DS1_M;
  imu_s.settings.device.mAddress = LSM9DS1_AG;
  
  imu_s.settings.accel.scale = 4; // Set accel range to +/-16g
  imu_s.settings.gyro.scale = 2000; // Set gyro range to +/-2000dps
  imu_s.settings.mag.scale = 8; // Set mag range to +/-8Gs
}

void loop()
{
    // Arduino
    float xAcc, yAcc, zAcc;
    float xGyro, yGyro, zGyro;
    
    float roll, pitch, yaw;
    float s_roll, s_pitch, s_yaw;
    float relative_roll, relative_pitch;
    float gyroScale=0.001;
    if(IMU.accelerationAvailable()){
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    }
    if(IMU.gyroscopeAvailable()){
    IMU.readGyroscope(xGyro, yGyro, zGyro);
    }
    
//    IMU.readMagneticField(mx, my, mz); 
//    printRPY_Arduino(xAcc, yAcc, zAcc);
  
//    filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);
//    filter.updateIMU(yGyro, xGyro, zGyro, yAcc, xAcc, zAcc);
    filter.updateIMU(xGyro, zGyro, yGyro, xAcc, zAcc, yAcc);
//  
    roll = filter.getRoll();
    pitch = filter.getPitch();
    yaw = filter.getYaw();
//    
//    Serial.print("Arduino: ");
//    Serial.print(roll);
//    Serial.print(" ");
//    Serial.print(pitch);
//    Serial.print(" ");
//    Serial.println(yaw);
//    Serial.print(" ");

//-------------------------------------------------------------------------//
    float s_xAcc, s_yAcc, s_zAcc;
    float s_xGyro, s_yGyro, s_zGyro;
    
//  // Sparkfun
    if ( imu_s.gyroAvailable() )
    {
      imu_s.readGyro();
    }
    if ( imu_s.accelAvailable() )
    {
      imu_s.readAccel();
    }
//    if ( imu_s.magAvailable() )
//    {
//      imu_s.readMag();
//    }
    s_xAcc = imu_s.calcAccel(imu_s.Ax); 
    s_yAcc = imu_s.calcAccel(imu_s.Ay);
    s_zAcc = imu_s.calcAccel(imu_s.Az);
    s_xGyro = imu_s.calcGyro(imu_s.Gx); 
    s_yGyro = imu_s.calcGyro(imu_s.Gy);
    s_zGyro = imu_s.calcGyro(imu_s.Gz);

//  imu_s.Ax = lpf.update(imu_s.Ax);
//  imu_s.Ay = lpf.update(imu_s.Ay);
//  imu_s.Az = lpf.update(imu_s.Az);
//    filter2.updateIMU(s_xGyro, s_yGyro, s_zGyro, s_xAcc, s_yAcc, s_zAcc);
    filter2.updateIMU(s_yGyro, s_zGyro, s_xGyro, s_yAcc, s_zAcc, s_xAcc);

    s_roll = filter2.getRoll();
    s_pitch = filter2.getPitch();
    s_yaw = filter2.getYaw();
//    printGyro();  
//    printAccel(); 
//    printMag();   
//    printAttitude(imu_s.Ax, imu_s.Ay, imu_s.Az, -imu_s.My, -imu_s.Mx, imu_s.Mz, roll, pitch, yaw);
  
//    r = filter.getRoll();
//    p = filter.getPitch();
//    y = filter.getYaw();
//    Serial.print("Sparkfun: ");
//    Serial.print(s_roll);
//    Serial.print(" ");
//    Serial.print(s_pitch);
//    Serial.print(" ");
//    Serial.println(s_yaw);
    relative_roll = roll - s_roll;
    relative_pitch = pitch - s_pitch;
    Serial.print("Relative Angle: ");
    Serial.print(relative_roll);
    Serial.print(" ");
    Serial.println(relative_pitch);
//    Serial.print(" ");
//    Serial.println(yaw - s_yaw);

//  int FSR_00 = analogRead(FSR_0); 
//  int FSR_11 = analogRead(FSR_1);  
//  Serial.print(FSR_00);
//  Serial.print(" ");
//  Serial.println(FSR_11);
//}
}
//-------------------------------------------------------------------------------------//
//void printGyro()
//{
//  // Now we can use the gx, gy, and gz variables as we please.
//  // Either print them as raw ADC values, or calculated in DPS.
//  Serial.print("G: ");
//#ifdef PRINT_CALCULATED
//  // If you want to print calculated values, you can use the
//  // calcGyro helper function to convert a raw ADC value to
//  // DPS. Give the function the value that you want to convert.
//  Serial.print(imu_s.calcGyro(imu_s.Gx), 2);
//  Serial.print(", ");
//  Serial.print(imu_s.calcGyro(imu_s.Gy), 2);
//  Serial.print(", ");
//  Serial.print(imu_s.calcGyro(imu_s.Gz), 2);
//  Serial.println(" deg/s");
//#elif defined PRINT_RAW
//  Serial.print(imu_s.Gx);
//  Serial.print(", ");
//  Serial.print(imu_s.Gy);
//  Serial.print(", ");
//  Serial.println(imu_s.Gz);
//#endif
//}

//
//void printAccel()
//{
//  // Now we can use the ax, ay, and az variables as we please.
//  // Either print them as raw ADC values, or calculated in g's.
//  Serial.print("A: ");
//#ifdef PRINT_CALCULATED
//  // If you want to print calculated values, you can use the
//  // calcAccel helper function to convert a raw ADC value to
//  // g's. Give the function the value that you want to convert.
//  Serial.print(imu_s.calcAccel(imu_s.Ax), 2);
//  Serial.print(" ");
//  Serial.print(imu_s.calcAccel(imu_s.Ay), 2);
//  Serial.print(" ");
//  Serial.println(imu_s.calcAccel(imu_s.Az), 2);
//
//#elif defined PRINT_RAW
//  Serial.print(imu_s.Ax);
//  Serial.print(" ");
//  Serial.print(imu_s.Ay);
//  Serial.print(" ");
//  Serial.println(imu_s.Az);
//#endif

//}
//
//void printMag()
//{
//  // Now we can use the mx, my, and mz variables as we please.
//  // Either print them as raw ADC values, or calculated in Gauss.
//  Serial.print("M: ");
//#ifdef PRINT_CALCULATED
//  // If you want to print calculated values, you can use the
//  // calcMag helper function to convert a raw ADC value to
//  // Gauss. Give the function the value that you want to convert.
//  Serial.print(imu_s.calcMag(imu_s.mx), 2);
//  Serial.print(", ");
//  Serial.print(imu_s.calcMag(imu_s.my), 2);
//  Serial.print(", ");
//  Serial.print(imu_s.calcMag(imu_s.mz), 2);
//  Serial.println(" gauss");
//#elif defined PRINT_RAW
//  Serial.print(imu_s.mx);
//  Serial.print(", ");
//  Serial.print(imu_s.my);
//  Serial.print(", ");
//  Serial.println(imu_s.mz);
//#endif
//}

//
void printAttitude(float ax, float ay, float az, float mx, float my, float mz, float roll, float pitch, float yaw)
{
  float r = atan2(ay, az);
  float p = atan2(-ax, sqrt(ay * ay + az * az));
  float y;
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
  y *= 180.0 / PI;

//  r = lpf2.filterIn(r);
//  p = lpf2.filterIn(p);
//  y = lpf2.filterIn(y);

  Serial.print(r);
  Serial.print(" ");
  Serial.print(p);
  Serial.print(" ");
  Serial.println(y);
  
}
