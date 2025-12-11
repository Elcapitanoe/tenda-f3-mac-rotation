import random
import os

TOTAL_MAC_ADDRESSES = 48
OUTPUT_FILE_PATH = "/www/private/auto_change_mac/list_mac.txt"

def generate_unicast_mac_address():
    hex_digits = "0123456789ABCDEF"
    even_digits = "02468ACE"

    first_digit = random.choice(hex_digits)
    second_digit = random.choice(even_digits)
    
    mac_address_parts = [f"{first_digit}{second_digit}"]

    for _ in range(5):
        byte_value = random.randint(0, 255)
        mac_address_parts.append(f"{byte_value:02X}")

    return ":".join(mac_address_parts)

def main():
    print(f"--- Starting generation of {TOTAL_MAC_ADDRESSES} MAC Addresses ---")
    
    directory_path = os.path.dirname(OUTPUT_FILE_PATH)
    if directory_path and not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"[INFO] Directory created: {directory_path}")
        except OSError as error:
            print(f"[ERROR] Failed to create directory. Check permissions. {error}")
            return

    try:
        with open(OUTPUT_FILE_PATH, "w") as file_handle:
            for _ in range(TOTAL_MAC_ADDRESSES):
                mac_address = generate_unicast_mac_address()
                file_handle.write(mac_address + "\n")
        
        print(f"[SUCCESS] Successfully saved {TOTAL_MAC_ADDRESSES} MAC Addresses.")
        print(f"[PATH] File location: {OUTPUT_FILE_PATH}")
        
    except IOError as error:
        print("[ERROR] Failed to write to file. Ensure correct access permissions.")
        print(f"Error details: {error}")

if __name__ == "__main__":
    main()