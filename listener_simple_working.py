import socket
import time
import json
import os
from datetime import datetime

# تحميل الإعدادات من settings.json
with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

PBX_HOST = settings["pbx"]["ip"]
PBX_PORT = int(settings["pbx"]["port"])
PBX_USER = settings["pbx"]["username"]
PBX_PASS = settings["pbx"]["password"]
TARGET_EXTENSION = settings["agent"]["extension"]

# المسار الوحيد
callstatus_file = r"C:\OMEGASYS\CaCallstatus.dat"
os.makedirs(r"C:\OMEGASYS", exist_ok=True)

def connect_ami():
    """الاتصال بالـ PBX"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((PBX_HOST, PBX_PORT))
    s.sendall(f"Action: Login\r\nUsername: {PBX_USER}\r\nSecret: {PBX_PASS}\r\nEvents: on\r\n\r\n".encode())
    return s

def write_callstatus(caller, ddi):
    """يكتب بيانات المكالمة أثناء الرنين"""
    try:
        content = f"""<CRM>
    <callRecord>
        <CallerID>{caller}</CallerID>
        <DDI>{ddi}</DDI>
        <Date>{datetime.now().strftime('%d-%m-%Y')}</Date>
        <Time>{datetime.now().strftime('%H:%M:%S')}</Time>
    </callRecord>
</CRM>"""
        with open(callstatus_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ CaCallstatus.dat updated for {caller}")
    except Exception as e:
        print(f"⚠️ Error writing file: {e}")

def clear_after_delay(delay=3):
    """يمسح الملف بعد التأخير المحدد"""
    time.sleep(delay)
    try:
        with open(callstatus_file, "w", encoding="utf-8") as f:
            f.write("")
        print("🧹 Cleared CaCallstatus.dat after 3 seconds.")
    except Exception as e:
        print(f"⚠️ Error clearing file: {e}")

def handle_event(event):
    """تحليل أحداث AMI"""
    lines = event.strip().split("\n")
    data = {}
    for line in lines:
        if ": " in line:
            k, v = line.split(": ", 1)
            data[k.strip()] = v.strip()

    event_type = data.get("Event", "")
    caller = data.get("CallerIDNum", "")
    dest_ext = data.get("DestCallerIDNum", "")
    dial_status = data.get("DialStatus", "")
    connected_line = data.get("ConnectedLineNum", "")

    # رنين المكالمة
    if event_type == "DialBegin" and dest_ext == TARGET_EXTENSION:
        print(f"📞 Incoming call: {caller} → {TARGET_EXTENSION}")
        write_callstatus(caller, TARGET_EXTENSION)
        return

    # عند الإجابة (بعض الإصدارات ترسل DialEnd أو BridgeEnter)
    if (event_type == "DialEnd" and dial_status == "ANSWER" and dest_ext == TARGET_EXTENSION) \
        or (event_type == "BridgeEnter" and (connected_line == TARGET_EXTENSION or dest_ext == TARGET_EXTENSION)):
        print(f"✅ Call answered by {TARGET_EXTENSION}, will clear after 3s.")
        clear_after_delay(3)
        return

def listen():
    """الاستماع للأحداث"""
    print(f"🚀 Listener started for extension {TARGET_EXTENSION}")
    sock = connect_ami()
    buffer = ""

    while True:
        try:
            data = sock.recv(4096).decode(errors="ignore")
            if not data:
                time.sleep(1)
                continue
            buffer += data
            while "\r\n\r\n" in buffer:
                event, buffer = buffer.split("\r\n\r\n", 1)
                handle_event(event)
        except Exception as e:
            print(f"⚠️ Connection error: {e}")
            time.sleep(5)
            sock = connect_ami()

if __name__ == "__main__":
    listen()
