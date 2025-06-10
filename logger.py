import csv
import os
import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("localhost", port=5020)
if not client.connect():
    print("Couldn't connect to Modbus Server")
    exit(1)

filename = "logs.csv"
write_header = not os.path.exists(filename)

with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)

    if write_header:
        writer.writerow(["Timestamp", "Temperature (HR[0])", "Pressure (HR[1])"])

    print(f"Logging to {filename} every 5 seconds…")

    try:
        while True:
            response = client.read_holding_registers(address=0, count=2, slave=1)

            if not response.isError():
                temperature = response.registers[0]
                pressure = response.registers[1]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                writer.writerow([timestamp, temperature, pressure])
                file.flush()

                print(f" {timestamp} | Temperature: {temperature}°C | Pressure: {pressure} hPa")
            else:
                print(" Modbus read failed")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nLogging stopped by user")

    finally:
        client.close()
        print("Client disconnected")
