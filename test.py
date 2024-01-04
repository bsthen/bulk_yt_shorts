import subprocess
import hashlib

def get_mac_address():
    # This function retrieves the MAC address of the first network interface card (NIC)
    try:
        result = subprocess.check_output(['wmic', 'nic', 'get', 'MACAddress']).decode().split('\n')[1].strip()
        return result
    except Exception as e:
        print(f"Error retrieving MAC address: {e}")
        return None

def get_cpu_serial_number():
    # This function retrieves the CPU serial number
    try:
        result = subprocess.check_output(['wmic', 'cpu', 'get', 'ProcessorId']).decode().split('\n')[1].strip()
        return result
    except Exception as e:
        print(f"Error retrieving CPU serial number: {e}")
        return None

def generate_device_key():
    mac_address = get_mac_address()
    cpu_serial_number = get_cpu_serial_number()

    if mac_address and cpu_serial_number:
        # Combine MAC address and CPU serial number to create a unique device key
        device_key = hashlib.md5((mac_address + cpu_serial_number).encode()).hexdigest()
        return device_key
    else:
        return None

device_key = generate_device_key()
if device_key:
    print(f"Generated Device Key: {device_key}")
else:
    print("Failed to generate Device Key.")
