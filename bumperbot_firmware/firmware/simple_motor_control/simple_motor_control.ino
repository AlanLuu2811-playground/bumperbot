// L298N H-Bridge Connection PINs
#define L298N_enA 9  // PWM
#define L298N_in1 12  // Dir Motor A
#define L298N_in2 13  // Dir Motor A

float cmd = 0;

void setup() {
  // Set pin modes
  pinMode(L298N_enA, OUTPUT);
  pinMode(L298N_in1, OUTPUT);
  pinMode(L298N_in2, OUTPUT);

  Serial.begin(115200);
}

void loop() {
  if (Serial.available())
  {
    cmd = Serial.readString().toFloat();

    analogWrite(L298N_enA, cmd*100);

    if (cmd > 0.0) {
      // Set Motor Rotation Direction
      digitalWrite(L298N_in1, LOW);
      digitalWrite(L298N_in2, HIGH);
    }


  }
}
