#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>

LSM9DS1 imu_s;
Madgwick filter;

#define PRINT_CALCULATED
#define PRINT_SPEED 250 // 250 ms between prints
static unsigned long lastPrint = 0; // Keep track of print time
#define DECLINATION -8.58 // Declination (degrees) in Boulder, CO.

const float sensorRate = 119.00;

//Function definitions
void printGyro();
void printAccel();
void printMag();
void printAttitude(float ax, float ay, float az, float mx, float my, float mz);

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

  // Arduino
  float xAcc, yAcc, zAcc;
  float xGyro, yGyro, zGyro;
  
  float roll, pitch, yaw;
  
  if ((lastPrint + PRINT_SPEED) < millis())
  {
    //Arduino
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    IMU.readGyroscope(xGyro, yGyro, zGyro);
    //IMU.readMagneticField(mx, my, mz); 

    //filter.update(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc, mx, my, mz);
    filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);

    roll = filter.getRoll();
    pitch = filter.getPitch();
    yaw = filter.getYaw();
    
    Serial.println("-----------------");
    Serial.print("Roll: ");
    Serial.println(roll);
    Serial.print("Pitch: ");
    Serial.println(pitch);
    Serial.print("Yaw: ");
    Serial.println(yaw);

    //Sparkfun
    printGyro();  
    printAccel(); 
    printMag();   
    printAttitude(imu_s.ax, imu_s.ay, imu_s.az,
                  -imu_s.my, -imu_s.mx, imu_s.mz);
    Serial.println();

    lastPrint = millis(); // Update lastPrint time
  }
  
}

void printGyro()
{
  // Now we can use the gx, gy, and gz variables as we please.
  // Either print them as raw ADC values, or calculated in DPS.
  Serial.print("G: ");
#ifdef PRINT_CALCULATED
  // If you want to print calculated values, you can use the
  // calcGyro helper function to convert a raw ADC value to
  // DPS. Give the function the value that you want to convert.
  Serial.print(imu_s.calcGyro(imu_s.gx), 2);
  Serial.print(", ");
  Serial.print(imu_s.calcGyro(imu_s.gy), 2);
  Serial.print(", ");
  Serial.print(imu_s.calcGyro(imu_s.gz), 2);
  Serial.println(" deg/s");
#elif defined PRINT_RAW
  Serial.print(imu_s.gx);
  Serial.print(", ");
  Serial.print(imu_s.gy);
  Serial.print(", ");
  Serial.println(imu_s.gz);
#endif
}

void printAccel()
{
  // Now we can use the ax, ay, and az variables as we please.
  // Either print them as raw ADC values, or calculated in g's.
  Serial.print("A: ");
#ifdef PRINT_CALCULATED
  // If you want to print calculated values, you can use the
  // calcAccel helper function to convert a raw ADC value to
  // g's. Give the function the value that you want to convert.
  Serial.print(imu_s.calcAccel(imu_s.ax), 2);
  Serial.print(", ");
  Serial.print(imu_s.calcAccel(imu_s.ay), 2);
  Serial.print(", ");
  Serial.print(imu_s.calcAccel(imu_s.az), 2);
  Serial.println(" g");
#elif defined PRINT_RAW
  Serial.print(imu_s.ax);
  Serial.print(", ");
  Serial.print(imu_s.ay);
  Serial.print(", ");
  Serial.println(imu_s.az);
#endif

}

void printMag()
{
  // Now we can use the mx, my, and mz variables as we please.
  // Either print them as raw ADC values, or calculated in Gauss.
  Serial.print("M: ");
#ifdef PRINT_CALCULATED
  // If you want to print calculated values, you can use the
  // calcMag helper function to convert a raw ADC value to
  // Gauss. Give the function the value that you want to convert.
  Serial.print(imu_s.calcMag(imu_s.mx), 2);
  Serial.print(", ");
  Serial.print(imu_s.calcMag(imu_s.my), 2);
  Serial.print(", ");
  Serial.print(imu_s.calcMag(imu_s.mz), 2);
  Serial.println(" gauss");
#elif defined PRINT_RAW
  Serial.print(imu_s.mx);
  Serial.print(", ");
  Serial.print(imu_s.my);
  Serial.print(", ");
  Serial.println(imu_s.mz);
#endif
}

// Calculate pitch, roll, and y.
// Pitch/roll calculations take from this app note:
// https://web.archive.org/web/20190824101042/http://cache.freescale.com/files/sensors/doc/app_note/AN3461.pdf
// Heading calculations taken from this app note:
// https://web.archive.org/web/20150513214706/http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/Magnetic__Literature_Application_notes-documents/AN203_Compass_Heading_Using_Magnetometers.pdf
void printAttitude(float ax, float ay, float az, float mx, float my, float mz)
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

  Serial.print("R: ");
  Serial.println(r, 2);
  Serial.print("P: ");
  Serial.println(p, 2);
  Serial.print("Y: ");
  Serial.println(y, 2);
}
