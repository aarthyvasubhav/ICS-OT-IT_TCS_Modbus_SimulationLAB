import time
from pymodbus.client import ModbusTcpClient
from alert_sender import log_to_file, print_alert, send_email_alert, send_slack_alert

PRESSURE_THRESHOLD = 2000

client = ModbusTcpClient('localhost', port = 5020)

if not client.connect():
	print("couldn't able to connect with server")
	exit(1)
	
print("IDS monitoring for any anomalies")

try:

	while True:
		response = client.read_holding_registers(address = 1, count = 1, slave =1)
		if not response.isError():
			pressure = response.registers[0]
			print(f"Pressure (HR[1] = {pressure}")
			if pressure > PRESSURE_THRESHOLD:
				print(f" ALERT: Aanamolous pressure detected: {pressure} hpa")
				
				alert_msg = f"Anomaly Detected: HR[1] = {pressure} exceeds {PRESSURE_THRESHOLD}"
				# Send alerts
				print_alert(alert_msg)
				log_to_file(alert_msg)
				#if SEND_EMAIL:
					#send_email_alert("Modbus IDS Alert", alert_msg)
				#if SEND_SLACK:
					#send_slack_alert(alert_msg, webhook_url=SLACK_WEBHOOK_URL)
		else:
			print("Failed to read register")
		time.sleep(2)

except KeyboardInterrupt:
	print("\n IDS stopped by user")

finally:
	client.close()
	print("connection closed")
	
