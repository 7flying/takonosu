#define RATE 115200

// Holds the command
char buffer[10];
// Buffer index
uint8_t buffInd = 0;

void setup(void) {
  Serial.begin(RATE);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);

  pinMode(8, INPUT);
  pinMode(9, INPUT);
  pinMode(10, INPUT);
  pinMode(11, INPUT);
  pinMode(12, INPUT);
  pinMode(13, OUTPUT);
}

// {R|W}{A|D}{NN}{X|valueX}
void process(void) {
  int reading;
  uint8_t err = 0;
  switch (buffer[0]) {
    case 'R':
      // Read an A|D sensor, {A|D}00 - {A|D}13
      if (buffer[1] == 'A') {
        reading = analogRead((buffer[2] - 48) * 10 + (buffer[3] - 48));
      } else {
        reading = digitalRead((buffer[2] - 48) * 10 + (buffer[3] - 48));
      }
      break;
    case 'W':
      // write some data to pin.
      if (buffer[1] == 'A') {
        uint8_t i = 4;
        uint8_t value = 0;
        while(buffer[i] != 'X') {
          value = value * 10 + (buffer[i] - 48);
        }
        analogWrite((buffer[2] - 48) * 10 + (buffer[3] - 48), value);
      } else {
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
  if (buffer[0] == 'R' && !err && !isnan(reading))
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