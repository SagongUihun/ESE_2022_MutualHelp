#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <Arduino_LSM9DS1.h>
#include <MahonyAHRS.h>
#include <MadgwickAHRS.h>


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

void printAttitude(float ax, float ay, float az, float mx, float my, float mz, float roll, float pitch, float yaw);

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
}

void loop()
{
  // Arduino
  float xAcc, yAcc, zAcc;
  float xGyro, yGyro, zGyro, bef_xGyro, bef_zAcc;
  
  float roll, pitch, yaw;
  float r, p, y;
  
  IMU.readAcceleration(xAcc, yAcc, zAcc);
  IMU.readGyroscope(xGyro, yGyro, zGyro);
  //IMU.readMagneticField(mx, my, mz); 

  //filter.update(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc, mx, my, mz);
  filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);

  roll = filter.getRoll();
  pitch = filter.getPitch();
  yaw = filter.getYaw();


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
 
  printAttitude(imu_s.Ax, imu_s.Ay, imu_s.Az, -imu_s.My, -imu_s.Mx, imu_s.Mz, roll, pitch, yaw);
  int FSR_00 = analogRead(FSR_0); 
  int FSR_11 = analogRead(FSR_1);  
//  Serial.print("A0: ");
  Serial.print(FSR_00);
  Serial.print(" ");
  Serial.println(FSR_11);
}

//-------------------------------------------------------------------------------------//
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
  y  *= 180.0 / PI;


  Serial.print(roll-r);
  Serial.print(" ");
  Serial.print(pitch-p);
  Serial.print(" ");
  Serial.print(yaw-y);
  
}
