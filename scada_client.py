import time
from pymodbus.client import ModbusTcpClient

# Connect to server
client = ModbusTcpClient('localhost', port=5020)
if not client.connect():
    print(f"❌ Could not connect to Modbus server at {server_ip}")
    exit(1)

print(f" Connected to Modbus server")
print(" Starting polling every 5 seconds...\n")

try:
    while True:
        response = client.read_holding_registers(address=0, count=2, slave=1)
        if not response.isError():
            temp = response.registers[0]
            pressure = response.registers[1]
            print(f" Temperature (HR[0]): {temp} °C; Pressure (HR[1]): {pressure} hPa")
        else:
            print("Failed to read registers.")

        time.sleep(5)  # Wait before polling again

except KeyboardInterrupt:
    print("\nPolling stopped by user.")

finally:
    client.close()
    print("Connection closed.")

