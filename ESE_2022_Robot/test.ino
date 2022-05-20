#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>


//UUID setting
BLEService IMUService("6e400001-b5a3-f393-e0a9-e50e24dcca9e");
// Characteristic setting 
BLEIntCharacteristic IMUxACC("6e400002-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUyACC("6e400003-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );
BLEIntCharacteristic IMUzACC("6e400004-b5a3-f393-e0a9-e50e24dcca9e", BLEWrite | BLERead |BLENotify );

//BLEStringCharacteristic PitchChar("6e400003-b5a3-f393-e0a9-e50e24dcca9e",BLEWrite ,10);
//BLEStringCharacteristic YawChar("6e400004-b5a3-f393-e0a9-e50e24dcca9e",BLEWrite ,10);

// initialize a Madgwick filter:
Madgwick filter;
// sensor's sample rate is fixed at 104 Hz:
const float sensorRate = 119.00;
  // values for acceleration and rotation:
  float xAcc, yAcc, zAcc;
  float xGyro, yGyro, zGyro;
  float mx, my, mz; // Magnometer #########
  float xAcc_now, xAcc_past;
  float xVel_now, xVel_past;
  float xPos;
String imu_msg;
unsigned long before_t , after_t;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
Serial.print("start communication");

if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    // stop here if you can't access the IMU:
    while (true);
  }
  // start the filter to run at the sample rate:
  filter.begin(sensorRate);

if (!BLE.begin()) {
    Serial.println("starting BLE failed!");

    while (1);
  }

  BLE.setLocalName("QuitSmocking");
  BLE.setAdvertisedService(IMUService); 
  IMUService.addCharacteristic(IMUxACC);
  IMUService.addCharacteristic(IMUyACC);
  IMUService.addCharacteristic(IMUzACC);

  
  BLE.addService(IMUService);

  BLE.advertise();
  
Serial.println("Bluetooth device active, waiting for connections...");
}

void loop() {
  // put your main code here, to run repeatedly:
BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());
       

      while(central.connected()){

       //before_t = millis();
       
       if (IMU.accelerationAvailable() &&
           IMU.gyroscopeAvailable()&& IMU.magneticFieldAvailable()) {
          // read accelerometer &and gyrometer:
          IMU.readAcceleration(xAcc, yAcc, zAcc);
          IMU.readGyroscope(xGyro, yGyro, zGyro);
          IMU.readMagneticField(mx, my, mz); // ##############
      
          // update the filter, which computes orientation:
          
          // print the heading, pitch and roll
          //imu_msg = (String)xAcc +" " + (String)yAcc +" " +(String)zAcc + " " + (String)xGyro + " " + (String)yGyro + " " + (String)zGyro + " " + (String)mx +" " + (String)my +" " + (String)mz;
        } 
        //Serial.println( millis() - before_t);

        
      /*쓰기*/
        IMUxACC.writeValue((int)100 * xAcc);
        IMUyACC.writeValue((int)100 * yAcc);
        IMUzACC.writeValue((int)100 * zAcc);

  //    /*읽기*/
//        if(IMUxACC.written()) {
//            if (IMUxACC.value()) {
//                
//                int val = IMUxACC.value();
//                Serial.print("Counting: ");
//                Serial.println(val);
//                
//                
//            }//value
//        }//written
    }//connected
  }//central
}
