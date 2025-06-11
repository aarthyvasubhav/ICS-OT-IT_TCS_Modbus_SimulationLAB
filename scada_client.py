import csv
import os
import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient

# Connect to server
client = ModbusTcpClient('localhost', port=5020)
if not client.connect():
    print(f" Could not connect to Modbus server")
    exit(1)

print(f" Connected to Modbus server")
print(" Starting polling every 5 seconds...\n")

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
            		print("Failed to read registers.")

        	time.sleep(5)  # Wait before polling again

    except KeyboardInterrupt:
    	print("\nPolling stopped by user.")

    finally:
    	client.close()
    	print("Connection closed.")

