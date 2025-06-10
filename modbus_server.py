import asyncio
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from threading import Thread
import time
import random

# Simulated values for HR[0]=TEMPERATURE, HR[1] = pressure

initial_values = [25, 1000] #Temperature in Cel, pressure in hpa

hr_blocks = ModbusSequentialDataBlock(0, initial_values)
store = ModbusSlaveContext(hr = hr_blocks)
context = ModbusServerContext(slaves = store, single = True)

#Fucntion to simulate sensor value changes

def simulate_sensors():
	while True:
		temp =  random.randint(20,30)
		pressure = random.randint(950, 1050)
		context[0].setValues(3, 0, [temp, pressure]) # 3 - Holding Register
		print(f"[Sensor Update] Temp = {temp} Celcious Pressure = {pressure} hpa")
		time.sleep(5) # wait before next update

# Start the sensor simulation thread

sensor_thread = Thread(target = simulate_sensors)
sensor_thread.daemon = True
sensor_thread.start()

#start THe Modbus TCP server
if __name__ == "__main__":
    print(" Modbus server running on port 5020...")
    asyncio.run(StartTcpServer(context, address=("0.0.0.0", 5020)))

