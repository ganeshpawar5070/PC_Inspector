import platform
import os
import psutil
import wmi
import uuid
import pythoncom
import socket

def get_system_info():
    return {
        "User Name": os.getlogin(),
        "PC Name": platform.node(),
        "OS": platform.system() + " " + platform.release(),
        "Architecture": platform.machine()
    }

def get_cpu_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()

    for cpu in c.Win32_Processor():
        return {
            "Processor": cpu.Name,
            "Cores": cpu.NumberOfCores,
            "Threads": cpu.NumberOfLogicalProcessors,
            "Usage": str(psutil.cpu_percent(interval=1)) + "%"
        }

def get_ram_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()

    mem = psutil.virtual_memory()
    
    # Default values agar WMI se data na mile
    total_slots = 0
    used_slots = 0

    # 1. Total RAM Slots nikalne ke liye
    try:
        for array in c.Win32_PhysicalMemoryArray():
            total_slots = int(array.MemoryDevices)
    except:
        total_slots = 0

    # 2. Used Slots aur Sticks ki details nikalne ke liye
    sticks = c.Win32_PhysicalMemory()
    used_slots = len(sticks)

    # 3. Empty Slots calculate karne ke liye
    empty_slots = total_slots - used_slots
    if empty_slots < 0:  # Kisi exception se bachne ke liye safety check
        empty_slots = 0

    # Data dictionary prepare karna
    data = {
        "Installed RAM": str(round(mem.total / (1024**3), 2)) + " GB",
        "RAM Slots": str(total_slots) if total_slots > 0 else "N/A",
        "Used Slots": str(used_slots),
        "Empty Slots": str(empty_slots) if total_slots > 0 else "N/A"
    }

    # Har ek RAM stick ki alag se info jodna
    for i, s in enumerate(sticks, 1):
        size = round(int(s.Capacity) / (1024**3), 0)
        speed = s.Speed if s.Speed else "Unknown"
        data[f"RAM Stick {i}"] = f"{size} GB {speed} MHz"

    return data

def get_storage_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()

    data = {}
    i = 1

    for disk in c.Win32_DiskDrive():
        size = round(int(disk.Size) / (1024**3), 0)
        type_ = "SSD" if "SSD" in disk.Model.upper() else "HDD"
        data[f"Drive {i}"] = f"{type_} {size} GB {disk.Model}"
        i += 1

    return data

def get_gpu_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()

    data = {}
    for i, gpu in enumerate(c.Win32_VideoController(), 1):
        data[f"GPU {i}"] = gpu.Name
    return data

def get_motherboard_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()

    for b in c.Win32_BaseBoard():
        return {
            "Manufacturer": b.Manufacturer,
            "Product": b.Product,
            "Serial Number": b.SerialNumber if b.SerialNumber else "N/A"
        }

def get_bios_info():
    pythoncom.CoInitialize()
    c = wmi.WMI()

    for b in c.Win32_BIOS():
        return {"BIOS Version": b.SMBIOSBIOSVersion}

def get_network_info():
    interfaces_data = {}
    interfaces = psutil.net_if_addrs()
    
    for interface_name, addresses in interfaces.items():
        for address in addresses:
            # Sirf IPv4 address uthane ke liye (family == socket.AF_INET)
            if address.family == socket.AF_INET:
                interfaces_data[interface_name] = address.address
                
    if not interfaces_data:
        interfaces_data["Status"] = "No Active IPv4 Network"
        
    return interfaces_data

def get_mac():
    mac = uuid.getnode()
    return ':'.join(f"{(mac >> i) & 0xff:02x}" for i in range(40, -1, -8)).upper()