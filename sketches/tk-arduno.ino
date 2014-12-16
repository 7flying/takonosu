#define RATE 115200

// Holds the command
char buffer[10];
// Buffer index
uint8_t buffInd = 0;

void setup(void) {
  Serial.begin(RATE);
  pinMode(7, OUTPUT);
}

// {R|W}{A|D}{NN}{X|valueX}
void process(void) {
  float reading;
  uint8_t err = 0;
  switch (buffer[0]) {
    case 'R':
      // Read an A|D sensor, {A|D}00 - {A|D}13
      if (buffer[2] == 'A') {
        reading = analogRead(buffer[3] - 48);
      } else {
        reading = digitalRead((buffer[2] - 48) * 10 + (buffer[3] - 48));
      }
      break;
    case 'W':
      // write some data to pin.
      if (buffer[4] == 'A') {
        uint8_t i = 0;
        uint8_t value = 0;
        while(buffer[i] != 'X') {
          value = value * 10 + (buffer[i] - 48);
        }
        reading = value;
        analogWrite(buffer[3] - 48, value);
      } else {
        reading = buffer[4] - 48;
        digitalWrite((buffer[2] - 48) * 10 + (buffer[3] - 48), buffer[4] - 48);
      }
      break;
    default:
      err = 1;
  }
  // Echo the command  
  for (uint8_t i = 0; i<10; i++)
    Serial.print(buffer[i]);
  // Data
  if (!err && !isnan(reading))
    Serial.print(reading);
  Serial.println();
}

void loop(void) {
  if(Serial.available()) {
    char command = Serial.read();
    if(command == 'X') {
      buffer[buffInd] = 'X';
      buffInd = 0;
      process();
    } else {
      buffer[buffInd] = command;
      buffInd++;
    }
  }
}