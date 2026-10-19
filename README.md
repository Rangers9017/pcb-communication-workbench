# PCB & Communication Workbench

A Turkish-language desktop learning app for electronics fundamentals, PCB calculations, and digital communication protocols. It uses Tkinter and the Python standard library.

## What is inside

The app opens as a desktop window with nine tabs:

1. **PCB basics** — IPC-2221 trace-width estimates and a microstrip impedance calculator.
2. **Power and circuits** — Ohm's law, voltage-divider and RC calculations, and nearby E24 resistor values.
3. **UART** — baud-rate and frame timing calculations, plus byte/parity examples.
4. **I2C** — pull-up resistor and rise-time estimates, with a bus transaction simulator.
5. **SPI** — a basic transfer simulator for clock mode and bit order.
6. **CAN** — bit-timing estimates for a selected oscillator and target baud rate.
7. **Modbus** — CRC-16 and RTU frame examples.
8. **Protocol comparison** — a quick reference for the supported buses.
9. **Mini applications** — LED resistor, frequency conversion, number-base conversion, and capacitor charging helpers.

## Requirements

- Python 3.9 or newer
- Tkinter (included with many Python distributions; on some Linux systems it is provided by a separate `python3-tk` package)

Run the app:

```bash
python pcb_haberlesme_rehberi.py
```

## Türkçe

Bu uygulama; PCB iz genişliği ve mikroşerit empedansı hesapları, temel devre araçları, UART/I2C/SPI/CAN simülatörleri, Modbus örnekleri ve mini elektronik araçları sunan sekmeli bir masaüstü rehberidir.

## Accuracy note

The calculators are educational estimates. PCB trace impedance and current capacity depend on the full stack-up, copper finish, board fabrication, temperature, and design rules. Check the relevant standards, manufacturer data, and board-house constraints before using any result in a real design.
