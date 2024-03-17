#define HallSensorU_pin 19  //PD2
#define HallSensorV_pin 20  //PD1
#define HallSensorW_pin 21  //PD0

#define CW 1
#define CCW -1

#define en 12   //PE3
#define sped 7  //PH4

int motor_steps = 48;
int reduction = 1;

double Kp = 0.7;
double Kd = 1.0;

double step_to_deg = (double) (motor_steps * reduction) / 360; //[paso/grado] -> 0.2 [paso/grados] o 5 [grados/paso]

int direct = 1;
int pulseCount = 0;

double desired_angle = 0.0;

double angle = 0.0;

int desired_step = 0.0;

double error = 0;
double prev_error = 0;

bool HSU_Val = digitalRead(HallSensorU_pin);
bool HSV_Val = digitalRead(HallSensorV_pin);
bool HSW_Val = digitalRead(HallSensorW_pin);

char buffer[20];

String data;

int debug_mode = 0;
int status1 = 0;

// Declaración de variables
//unsigned long tiempoAnterior = 0;
//const int intervalo = 5000;  // Intervalo de tiempo en milisegundos (2 segundos)

// Declaración de variables
unsigned long tiempoAnterior = 0;
const int intervalo = 2000;  // Intervalo de tiempo en milisegundos (2 segundos)
bool cambio = true;

void setup() {
  pinMode(HallSensorU_pin, INPUT);
  pinMode(HallSensorV_pin, INPUT);
  pinMode(HallSensorW_pin, INPUT);


  pinMode(en, OUTPUT);
  pinMode(sped, OUTPUT);

  digitalWrite(en, LOW);

  attachInterrupt(digitalPinToInterrupt(HallSensorU_pin), HallSensorU, CHANGE);
  attachInterrupt(digitalPinToInterrupt(HallSensorV_pin), HallSensorV, CHANGE);
  attachInterrupt(digitalPinToInterrupt(HallSensorW_pin), HallSensorW, CHANGE);

  Serial.begin(115200);
}

void loop() {

  // Obtener el tiempo actual en milisegundos
  unsigned long tiempoActual = millis();

  // Imprimir "Hola" o "Mundo" cada 2 segundos alternativamente
  if (tiempoActual - tiempoAnterior >= intervalo) {
    if (cambio) {
      Serial.println("520°");
      desired_angle = 520;
    } else {
      Serial.println("720°");
      desired_angle = 720;
    }

    cambio = !cambio;  // Alternar entre imprimir "Hola" y "Mundo"
    tiempoAnterior = tiempoActual;  // Actualizar el tiempo anterior
  }

  angle = pulseCount / step_to_deg;  // paso * grado/paso
  control();

  if (debug_mode == 1) {
    Serial.print("Step : ");
    Serial.print(pulseCount);
    Serial.print("   |   desired step : ");
    Serial.print(desired_step);
    Serial.print("   |   Angle : ");
    Serial.print(angle, 5);
    Serial.print("   |   Kp : ");
    Serial.print(Kp, 5);
    Serial.print("   |   Kd : ");
    Serial.print(Kd, 5);
    Serial.print("   |   Status : ");
    Serial.println(status1);
  }

  else
    Serial.println(angle);
}


void control() {
  desired_step = (int)(desired_angle * step_to_deg);

  error = desired_step - pulseCount;

  double pid_out = error * Kp + Kd * (error - prev_error);
  prev_error = error;
  //Serial.print("PID : ");
  //Serial.println(pid_out);

  if (pid_out > 0) {
    if (pid_out > 100)
      pid_out = 100;
    else if (pid_out < 10)
      pid_out = 10;
  }

  else {
    if (pid_out < -100)
      pid_out = -100;
    else if (pid_out > -10)
      pid_out = -10;
  }

  motor_start(pid_out);
}

void motor_start(double spd) {
  if (spd != 0 && status1 == 1) {
    digitalWrite(en, HIGH);

    double out = map(spd, 100, -100, 255, 0);
    analogWrite(sped, out);
  } else {
    digitalWrite(en, LOW);
  }
}

void HallSensorW() {
  HSW_Val = digitalRead(HallSensorW_pin);
  HSV_Val = digitalRead(HallSensorV_pin);
  direct = (HSW_Val == HSV_Val) ? CW : CCW;
  pulseCount = pulseCount + (1 * direct);
}

void HallSensorV() {
  HSV_Val = digitalRead(HallSensorV_pin);
  HSU_Val = digitalRead(HallSensorU_pin);
  direct = (HSV_Val == HSU_Val) ? CW : CCW;
  pulseCount = pulseCount + (1 * direct);
}

void HallSensorU() {
  HSU_Val = digitalRead(HallSensorU_pin);
  HSW_Val = digitalRead(HallSensorW_pin);
  direct = (HSU_Val == HSW_Val) ? CW : CCW;
  pulseCount = pulseCount + (1 * direct);
}

void serialEvent() {
  if (Serial.available() > 0) {
    data = Serial.readString();
    data.toCharArray(buffer, data.length());
    Serial.print("Data : ");
    Serial.println(buffer);
    desired_angle = parseNumber('a', 'A', desired_angle);
    Kp = parseNumber('P', 'p', Kp);
    Kd = parseNumber('d', 'D', Kd);
    debug_mode = parseNumber('m', 'M', debug_mode);
    status1 = parseNumber('s', 'S', status1);
  }
}

float parseNumber(char code, char code2, double val) {
  char *ptr = buffer;  // start at the beginning of buffer
  for (int i = 0; i < sizeof(buffer); i++) {
    if (*ptr == code || *ptr == code2)  // if you find code on your walk,
      return atof(ptr + 1);             // convert the digits that follow into a float and return it
    ptr++;
  }
  return val;
}
