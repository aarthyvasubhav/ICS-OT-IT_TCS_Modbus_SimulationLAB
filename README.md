# ICS/OT Modbus TCP Simulation and Attack Detection

## Overview

This project simulates a simplified Industrial Control System (ICS) environment using Modbus TCP. It is designed to model both legitimate and malicious behavior within an Operational Technology (OT) setting. The system consists of a Modbus server emulating a PLC, a SCADA client for legitimate polling, attacker scripts to simulate unauthorized access, an intrusion detection system (IDS), passive logging mechanisms, and alerting via log files or Slack notifications. The overall goal is to study ICS cybersecurity threats and implement lightweight detection mechanisms without relying on physical hardware.

## Project Structure

| Component                     | Module/File             | Description                                                                         |
| ----------------------------- | ----------------------- | ----------------------------------------------------------------------------------- |
| Modbus Server (PLC Simulator) | `modbus_server.py`      | Simulates Modbus holding registers for sensor data like temperature and pressure.   |
| SCADA Client                  | `scada_client.py`       | Continuously polls HR\[0] and HR\[1] to emulate a real SCADA/HMI interface.         |
| Unauthorized Write Attack     | `unauthorized_write.py` | Simulates an attack by injecting malicious values (e.g., 9999) into registers.      |
| Anomaly Detector (IDS)        | `ids.py`                | Detects abnormal conditions such as HR\[1] exceeding a threshold and raises alerts. |
| Passive Data Logger           | `logger.py`             | Logs register values to a CSV file for audit, forensics, or post-analysis.          |
| Replay Attack                 | `replay_write.py`       | Replays previously recorded values to simulate stale or delayed data attacks.       |
| Alert Sender                  | `alert_sender.py`       | Sends IDS alerts to log files, terminal output, and optionally to Slack.            |
| Environment Settings          | `.env`                  | Stores sensitive tokens (e.g., Slack) and configuration variables securely.         |
| Network Forensics             | *(Wireshark)*           | External tool used to analyze Modbus TCP traffic on port 5020.                      |

## How to Run the Project

1. **Set up the virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the Modbus server**
   This simulates PLC behavior by periodically updating holding registers.

   ```bash
   python modbus_server.py
   ```

3. **Run the SCADA client**
   This connects to the Modbus server and polls HR\[0] and HR\[1].

   ```bash
   python scada_client.py
   ```

4. **Simulate an attack**
   Inject a malicious value (e.g., `9999`) into HR\[1] using the attacker script.

   ```bash
   python unauthorized_write.py
   ```

5. **Run the IDS**
   Monitors for abnormal values (e.g., pressure spikes) and raises alerts.

   ```bash
   python ids.py
   ```

6. **Enable logging**
   Start the logger script to persist register values in a CSV file.

   ```bash
   python logger.py
   ```

7. **Trigger replay attack** *(optional)*
   Send previously recorded values to the server.

   ```bash
   python replay_write.py
   ```

8. **Check alerts**
   Alerts will appear in the terminal, `alerts.log`, and optionally in Slack if configured.

## Configuring Environment Variables

Create a `.env` file with the following:

```
SLACK_TOKEN=xoxb-...        # Your Slack Bot Token
SLACK_CHANNEL=#ics-alerts   # Slack channel name
SLACK_WEBHOOK=https://...   # Slack webhook URL (optional if using bot API)
```

## Wireshark Usage (Optional)

Wireshark can be used to inspect Modbus TCP traffic:

* Filter by port: `tcp.port == 5020`
* Look for function codes:

  * `0x03` – Read Holding Registers
  * `0x06` or `0x10` – Write operations

This helps verify whether data is tampered with or attacked in transit.

## Learning Outcomes

* Understand how Modbus TCP operates within ICS networks
* Explore vulnerabilities such as unauthorized writes and replay attacks
* Develop lightweight anomaly detection using Python
* Capture forensic data for auditing and analysis
* Integrate basic alerting and incident notification

## License

This project is licensed under the [MIT License](LICENSE)

## Acknowledgements

This work was inspired by industrial cybersecurity practices, open Modbus documentation, and guidance from NIST SP 800-82 on securing Industrial Control Systems.

---


