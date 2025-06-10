from dotenv import load_dotenv
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import requests

load_dotenv()
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")


# - - - - 1. File Logger - - - - -

def log_to_file(message, filename="alert.log"):
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	with open(filename, "a") as file:
		file.write(f"[{timestamp} {message}\n")

# - - - - 2. Console Print - - - - 

def print_alert(message):
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print(f"[{timestamp}]  ALERT: {message}")
	
	
# - - - - #. EMail ALert  - - - -

def send_email_alert(subject, body,
		     smtp_server = "smtp.gmail.com", port=587,
		     sender_email="email_user", sender_password="email_pass",
		     receipient_email="receipient email"):
		  
	try:
		msg = MIMEText(body)
		msg["Subject"] = subject
		msg["From"] = sender_email
		msg["To"] = recipient_email
		
		with smtplib.SMTP(smtp_server, port) as server:
			server.starttls()
			server.login(sender_email, sender_password)
			server.send_message(msg)
			
		print("EMAIL ALERT SENT!!")
	
	except Exception as e:
		print("Failed to send email")
		

# - - - - 4. Slack Alert - - - - 

def send_slack_alert(message, webhook_url):
	try:
		payload = { "text" : f" [MODBUS ALERT] {message}" }
		response = requested.post(webhook_url, json=payload)
		if response.status_code == 200:
			print("SLack alert sent!")
		else:
			print("SLack alert failed:", response.status_code)
	except Exception as e:
		print("Slack alert exceptiom:" , e)
	
