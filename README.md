# Tenda F3 WAN MAC Rotation Automation

## Overview

This repository contains a set of Python scripts designed to automate the rotation of WAN MAC addresses on **Tenda F3 V3** routers. It is specifically engineered to interact with the router's web interface to clone/update the WAN MAC address, facilitating automated network identity rotation.

The project consists of two core components:
1.  **Generator:** Creates valid, unicast MAC addresses.
2.  **Rotator:** Authenticates with the router and applies the configuration via HTTP requests.

## Compatibility

* **Hardware:** Tenda F3 (Version 3.0)
* **Firmware:** V12.01.01.46_multi
* **Host OS:** Linux (Ubuntu, Debian, CentOS, etc.)
* **Python Version:** 3.6+

## Prerequisites

Ensure your host machine has Python 3 installed. You will also need the `requests` library.

```bash
pip install requests
```

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Elcapitanoe/tenda-f3-mac-rotation.git
cd tenda-f3-mac-rotation
```

### 2. Directory Structure

The scripts are currently configured to use specific absolute paths. Ensure the following directory exists to match the script configuration:

```bash
sudo mkdir -p /www/private/auto_change_mac
sudo chown -R $USER:$USER /www/private/auto_change_mac
```

### 3. Configuration

Open `auto_mac.py` and update the router credentials and network settings to match your environment:

```python
ROUTER_IP = "192.168.1.1"       # Your Gateway IP
ROUTER_PASSWORD = "your_password" # Your Router Login Password
```

*Note: The script applies a full configuration payload (DHCP settings, DNS, etc.). Review the `configuration_payload` dictionary in `auto_mac.py` to ensure it matches your network requirements.*

## Usage

### 1. Generate MAC Addresses

Run the generator script to create a batch of 48 valid unicast MAC addresses. This creates the `list_mac.txt` file in the configured directory.

```bash
python3 mac_generator.py
```

*Output:* `[SUCCESS] Successfully saved 48 MAC Addresses.`

### 2. Rotate MAC Address

Run the rotator script to pick the next address from the list and apply it to the router.

```bash
python3 auto_mac.py
```

* **On Success:** The script logs the change, updates the router, and removes the used address from the queue.
* **On Failure:** Errors are logged to `activity.log` and printed to standard output.

## Automation (Cron Job)

To automate the rotation (e.g., every 30 minutes), add an entry to your crontab.

1.  Open crontab:
    ```bash
    crontab -e
    ```

2.  Add the following line:
    ```bash
    */30 * * * * /usr/bin/python3 /path/to/your/auto_mac.py >> /www/private/auto_change_mac/cron_output.log 2>&1
    ```

## Logging

The system maintains an activity log at `/www/private/auto_change_mac/activity.log`.

**Sample Log Output:**
```text
[2025-12-10 08:00:01] SUCCESS  | MAC updated: 12:A4:B6:C8:D9:E0 | Remaining Queue: 47
[2025-12-11 08:30:01] SUCCESS  | MAC updated: 46:32:11:AB:CD:EF | Remaining Queue: 46
```

## Disclaimer

This tool is intended for educational purposes and network administration in authorized environments. The author is not responsible for any misuse or network instability caused by improper configuration.
