# AgroNexon GPIO & Wiring Map

## Main ESP32 DevKit V1

| Function | ESP32 GPIO | Connection |
|---|---:|---|
| Left driver IN1 | 16 | L298N #1 IN1 |
| Left driver IN2 | 17 | L298N #1 IN2 |
| Left driver IN3 | 18 | L298N #1 IN3 |
| Left driver IN4 | 19 | L298N #1 IN4 |
| Left driver EN | 21 | Tie ENA+ENB (remove both jumpers) |
| Right driver IN1 | 22 | L298N #2 IN1 |
| Right driver IN2 | 23 | L298N #2 IN2 |
| Right driver IN3 | 25 | L298N #2 IN3 |
| Right driver IN4 | 26 | L298N #2 IN4 |
| Right driver EN | 27 | Tie ENA+ENB (remove both jumpers) |
| HC-SR04 TRIG | 13 | TRIG |
| HC-SR04 ECHO | 34 | ECHO through 5V-to-3.3V divider |
| Capacitive soil sensor AO | 35 | Analog output |
| Relay IN | 32 | Pump relay input |

GPIO34 and GPIO35 are input-only, which is suitable for ECHO and analog input.
Avoid using boot-strapping pins and UART pins for motor control.

## L298N motor wiring

Each L298N runs the two motors on one side:
- Driver #1 OUT1/OUT2: left-front motor; OUT3/OUT4: left-rear motor.
- Driver #2 OUT1/OUT2: right-front motor; OUT3/OUT4: right-rear motor.
- Tie IN1 and IN3 together; tie IN2 and IN4 together only if both channels
  are intended to receive the same direction signal. This firmware instead
  drives IN1..IN4 individually, so connect each GPIO exactly as in the table.
- Tie ENA and ENB together per driver to the listed PWM GPIO. Remove ENA/ENB jumpers.
- If one motor turns opposite to its partner, reverse that motor's two output wires.
- Check the actual L298N module terminal labels; board layouts vary.

## Power and safety

- Motor supply: suitable 12V battery sized for the motors and stall current.
- ESP32: clean regulated 5V supply to 5V/VIN pin, sized for Wi-Fi current peaks.
- ESP32-CAM: separate stable regulated 5V supply (recommend 1A or more).
- Relay/pump: pump supply must match pump voltage/current; relay contacts switch pump supply.
- Join grounds: battery negative, motor driver GND, ESP32 GND, relay GND and sensor GND.
- Do NOT feed motor or pump current through ESP32 pins or its 5V regulator.
- Fit a fuse near the battery and add suitable flyback suppression if the pump/relay
  module does not provide it.
- Use a resistor divider on HC-SR04 ECHO. Example: ECHO -> 1k -> GPIO34;
  GPIO34 -> 2k -> GND (about 3.3V from a 5V ECHO).
- Confirm relay active level before connecting pump. Firmware defaults active LOW.
- Keep electronics protected from water; route pump tubing away from boards.

## Camera

The ESP32-CAM is a separate board. Power it from regulated 5V and GND.
This sketch assumes the common AI-Thinker ESP32-CAM pin map. Verify your module
pinout before upload. The OV3660 sensor must be supported by the installed
esp32-camera driver.
