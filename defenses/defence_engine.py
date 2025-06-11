import logging
from datetime import datetime

# Optional : for restoring safe value

SAFE_VALUES = {

	0 : 21,
	1 : 1000
}

def restore_register(context, register, slave = 0):
	"""
	Reset a given holding register to its predefined safe value
	"""
	try:
		value = SAFE_VALUES.get(register)
		if value is not None:
			context[slave].setValues(3, register, [value])
			logging.warning(f"[RESTORE] HR[{register}] reset to safe value: {value}")
	except Exception as e:
		logging.error(f"[ERROR] Failed to restore HR[{register}]: {e}")

def log_attackers_action(value, register, source_ip=None):
	"""
	Log details about the unauthorized or anomalous action.
	"""
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	log_line = f"{timestamp},HR[{register}],{value},{source_ip or 'N/A'}\n"
	with open("attack_log.csv", "a") as f:
		f.write(log_line)
	logging.info(f"[LOGGED] Anomaly recorded: HR[{register}] = {value}")
    
    
