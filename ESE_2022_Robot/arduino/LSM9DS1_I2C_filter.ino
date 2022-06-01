#include <Wire.h>
#include <SPI.h>
#include <SparkFunLSM9DS1.h>
#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>
#include <ArduinoBLE.h>

#define LSM9DS1_M  0x1C // Would be 0x1C if SDO_M is LOW
#define LSM9DS1_AG 0x6A // Would be 0x6A if SDO_AG is LOW

//UUID setting
BLEService DataSendService("6e400001-b5a3-f393-e0a9-e50e24dcca9e");

BLEStringCharacteristic IMU1Acc("6e400002-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify ,20);
BLEStringCharacteristic IMU1Gyro("6e400003-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify ,20);
BLEStringCharacteristic IMU1Pose("6e400004-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify ,20);
BLEStringCharacteristic IMU2Acc("6e400005-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify ,20);
BLEStringCharacteristic IMU2Gyro("6e400006-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify ,20);
BLEStringCharacteristic IMU2Pose("6e400007-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify ,20);


//BLEStringCharacteristic FSR("6e400008-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify ,20);

LSM9DS1 imu_s;
Madgwick filter,filter2;

int FSR_2 = A2; //analog pin 2
int FSR_1 = A1; //analog pin 1

#define DECLINATION -8.58 // Declination (degrees) in Boulder, CO.

const float sensorRate = 119.00;

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
  
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  //imu2 address setting
  imu_s.settings.device.commInterface = IMU_MODE_I2C;
  imu_s.settings.device.agAddress = LSM9DS1_M;
  imu_s.settings.device.mAddress = LSM9DS1_AG;
  
  imu_s.settings.accel.scale = 4; // Set accel range to +/-16g
  imu_s.settings.gyro.scale = 2000; // Set gyro range to +/-2000dps
  imu_s.settings.mag.scale = 8; // Set mag range to +/-8Gs

  //ble setting 
  BLE.setLocalName("Thanos_Glove");
  BLE.setAdvertisedService(DataSendService); 
  DataSendService.addCharacteristic(IMU1Acc);
  DataSendService.addCharacteristic(IMU1Gyro);
  DataSendService.addCharacteristic(IMU1Pose);

  DataSendService.addCharacteristic(IMU2Acc);
  DataSendService.addCharacteristic(IMU2Gyro);
  DataSendService.addCharacteristic(IMU2Pose);

//  DataSendService.addCharacteristic(FSR);
 
  BLE.addService(DataSendService);

  BLE.advertise();
}

void loop()
{
    // Arduino
    float xAcc, yAcc, zAcc;
    float xGyro, yGyro, zGyro;
    float roll, pitch, yaw;
    float s_roll, s_pitch, s_yaw;
    float relative_roll, relative_pitch;
    float s_xAcc, s_yAcc, s_zAcc;
    float s_xGyro, s_yGyro, s_zGyro;
    float gyroScale=0.001;
    String IMU1_data_acc ,IMU1_data_gyro ,IMU1_data_pose ,IMU2_data_acc,IMU2_data_gyro,IMU2_data_pose, FSR_data;
    
    BLEDevice central = BLE.central();
    
    if (central) {
      while(central.connected()){
            
        //-------------------------IMU1------------------------------------------------//
      
        if(IMU.accelerationAvailable()){
        IMU.readAcceleration(xAcc, yAcc, zAcc);
        }
        if(IMU.gyroscopeAvailable()){
        IMU.readGyroscope(xGyro, yGyro, zGyro);
        }
    //    IMU.readMagneticField(mx, my, mz); 
    
     
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
   IMU1_data_acc =  String(xAcc) + " " + String(yAcc) + " " +String(zAcc); 
   IMU1_data_gyro = String(xGyro) + " " + String(yGyro) + " " + String(zGyro);
   IMU1_data_pose = String(roll) + " " + String(pitch) + " " + String(yaw);
    //-----------------------------IMU2--------------------------------------------//
        
        
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
    
        filter2.updateIMU(s_yGyro, s_zGyro, s_xGyro, s_yAcc, s_zAcc, s_xAcc);
    
        s_roll = filter2.getRoll();
        s_pitch = filter2.getPitch();
        s_yaw = filter2.getYaw();
        
        IMU2_data_acc = String(s_xAcc) + " " + String(s_yAcc) + " " +String(s_zAcc);
        IMU2_data_gyro = String(s_xGyro) + " " + String(s_yGyro) + " " + String(s_zGyro);
        IMU2_data_pose = String(s_roll) + " " + String(s_pitch) + " " + String(s_yaw);
    //------------------------------FSR-------------------------------------------//

    //    printAttitude(imu_s.Ax, imu_s.Ay, imu_s.Az, -imu_s.My, -imu_s.Mx, imu_s.Mz, roll, pitch, yaw);
      
    //    Serial.print("Sparkfun: ");
    //    Serial.print(s_roll);
    //    Serial.print(" ");
    //    Serial.print(s_pitch);
    //    Serial.print(" ");
    //    Serial.println(s_yaw);
        relative_roll = roll - s_roll;
        relative_pitch = pitch - s_pitch;
//        Serial.print("Relative Angle: ");
//        Serial.print(relative_roll);
//        Serial.print(" ");
//        Serial.println(relative_pitch);
    //    Serial.print(" ");
    //    Serial.println(yaw - s_yaw);
//    
//        FSR_22 = analogRead(FSR_2); 
//        FSR_11 = analogRead(FSR_1);  
    //  Serial.print(FSR_00);
    //  Serial.print(" ");
    //  Serial.println(FSR_11);
//        FSR_data = String(FSR_22) + " " + String(FSR_11);
        
        IMU1Acc.writeValue(IMU1_data_acc);
        IMU1Gyro.writeValue(IMU1_data_gyro);
        IMU1Pose.writeValue(IMU1_data_pose);

        IMU2Acc.writeValue(IMU2_data_acc);
        IMU2Gyro.writeValue(IMU2_data_gyro);
        IMU2Pose.writeValue(IMU2_data_pose);
//        FSR.writeValue(FSR_data);
  
      }
  }
}
