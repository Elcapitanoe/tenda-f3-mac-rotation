import requests
import base64
import os
import sys
from datetime import datetime, timedelta, timezone

ROUTER_IP = "192.168.1.1"
ROUTER_PASSWORD = "your_password"
BASE_DIRECTORY = "/www/private/auto_change_mac"
MAC_LIST_FILE_PATH = os.path.join(BASE_DIRECTORY, "list_mac.txt")
LOG_FILE_PATH = os.path.join(BASE_DIRECTORY, "activity.log")

LOGIN_URL = f"http://{ROUTER_IP}/login/Auth"
SETTINGS_URL = f"http://{ROUTER_IP}/goform/setSysTools"

def log_activity(status, message):
    local_timezone = timezone(timedelta(hours=7))
    current_timestamp = datetime.now(local_timezone).strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{current_timestamp}] {status:<8} | {message}"
    
    print(log_entry)
    
    try:
        with open(LOG_FILE_PATH, "a") as file_handle:
            file_handle.write(log_entry + "\n")
    except Exception as error:
        print(f"[ERROR] Could not write to log file: {error}")

def main():
    if not os.path.exists(MAC_LIST_FILE_PATH):
        log_activity("CRITICAL", f"File not found: {MAC_LIST_FILE_PATH}")
        sys.exit(1)
        
    if not os.access(MAC_LIST_FILE_PATH, os.W_OK):
        log_activity("CRITICAL", "Permission denied on list file. Check 'chown/chmod'.")
        sys.exit(1)

    with open(MAC_LIST_FILE_PATH, 'r') as file_handle:
        lines = file_handle.readlines()
    
    mac_address_queue = [line.strip() for line in lines if line.strip()]
    queue_size = len(mac_address_queue)

    if queue_size == 0:
        log_activity("INFO", "Queue empty. No action taken.")
        sys.exit(0)

    target_mac_address = mac_address_queue[0]

    session = requests.Session()
    
    try:
        encoded_password = base64.b64encode(ROUTER_PASSWORD.encode("utf-8")).decode("utf-8")
        login_response = session.post(LOGIN_URL, data={"password": encoded_password}, timeout=10)
        
        if "Tenda Wireless Router" not in login_response.text and "index.js" not in login_response.text:
            log_activity("ERROR", "Login failed. Check password or router status.")
            sys.exit(1)

        configuration_payload = {
            "module1": "loginAuth",
            "newPwd": "",
            "oldPwd": "",
            "module2": "wanAdvCfg",
            "wanServerName": "",
            "wanServiceName": "",
            "wanMTU": "1500",
            "macClone": "manual",
            "wanMAC": target_mac_address,
            "wanSpeed": "100",
            "module3": "lanCfg",
            "lanIP": "192.168.1.1",
            "lanMask": "255.255.255.0",
            "dhcpEn": "true",
            "lanDhcpStartIP": "192.168.1.2",
            "lanDhcpEndIP": "",
            "lanDns1": "8.8.8.8",
            "lanDns2": "",
            "module4": "remoteWeb",
            "remoteWebEn": "false",
            "remoteWebType": "any",
            "remoteWebIP": "",
            "remoteWebPort": "80",
            "module5": "sysTime",
            "sysTimeZone": "56",
            "module6": "softWare",
            "autoMaintenanceEn": "true"
        }

        response = session.post(SETTINGS_URL, data=configuration_payload, timeout=15)

        if response.status_code == 200:
            remaining_mac_addresses = mac_address_queue[1:]
            with open(MAC_LIST_FILE_PATH, 'w') as file_handle:
                for mac_address in remaining_mac_addresses:
                    file_handle.write(mac_address + "\n")
            
            log_activity("SUCCESS", f"MAC updated: {target_mac_address} | Remaining Queue: {len(remaining_mac_addresses)}")
        else:
            log_activity("FAILURE", f"Router rejected config. Status: {response.status_code}")

    except requests.exceptions.ConnectionError:
        log_activity("ERROR", "Unreachable. Router offline or wrong IP.")
    except Exception as error:
        log_activity("ERROR", f"Exception: {str(error)}")

if __name__ == "__main__":
    main()