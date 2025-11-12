// L9110S Motor Driver with Arduino
// Motor A connections
const int motorA_IA = 9;  // Speed control (PWM pin)
const int motorA_IB = 10; // Direction control (PWM pin)

// Motor run duration in milliseconds
const unsigned long RUN_DURATION = 300; // 2 seconds - adjust as needed

// Motor speed (0-255)
const int MOTOR_SPEED = 250; // Adjust speed here (0-255)

unsigned long motorStartTime = 0;
bool motorRunning = false;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set motor control pins as outputs
  pinMode(motorA_IA, OUTPUT);
  pinMode(motorA_IB, OUTPUT);
  
  // Make sure motor is stopped initially
  stopMotor();
  
  Serial.println("Arduino Ready!");
  Serial.println("Waiting for keyboard input...");
}

void loop() {
  // Check if data is available from serial
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    
    // Any character received will trigger the motor
    Serial.print("Key pressed: ");
    Serial.println(incomingByte);
    
    // Start the motor
    startMotor();
  }
  
  // Check if motor should stop
  if (motorRunning && (millis() - motorStartTime >= RUN_DURATION)) {
    stopMotor();
    Serial.println("Motor stopped");
  }
}

void startMotor() {
  // Run motor forward
  analogWrite(motorA_IA, MOTOR_SPEED);
  analogWrite(motorA_IB, 0);
  
  motorStartTime = millis();
  motorRunning = true;
  
  Serial.println("Motor started");
}

void stopMotor() {
  // Stop the motor
  analogWrite(motorA_IA, 0);
  analogWrite(motorA_IB, 0);
  
  motorRunning = false;
}

// Alternative: To run motor in reverse, use this in startMotor():
// analogWrite(motorA_IA, 0);
// analogWrite(motorA_IB, MOTOR_SPEED);