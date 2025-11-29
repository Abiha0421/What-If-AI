from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import paramiko

app = Flask(__name__)
CORS(app)

# 🔹 Step 1: Start Kali Linux VM using VirtualBox (GUI Mode)
def start_kali_vm():
    try:
        # Absolute path to VBoxManage.exe
        vboxmanage = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

        # Replace with your VM name
        vm_name = "kali-linux-2025.2-virtualbox-amd64"

        # Start Kali with GUI mode
        cmd = [vboxmanage, "startvm", vm_name, "--type", "gui"]
        subprocess.run(cmd, check=True)

        return "Kali Linux VM booting... GUI window should open!"
    except Exception as e:
        return f"Error starting Kali VM: {str(e)}"

# 🔹 Step 2: Connect to Kali VM via SSH (Port Forwarding: Host 127.0.0.1:2222 → Guest 22)
def run_in_kali(ip, mode):
    kali_ip = "127.0.0.1"        # Host machine IP
    kali_port = 2222             # Forwarded port (VirtualBox NAT Port Forwarding)
    username = "kali"            # apna Kali username
    password = "kali"            # apna Kali password

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(kali_ip, port=kali_port, username=username, password=password)

        if mode == "offensive":
            command = f"bash ~/offensive.sh {ip}"
        elif mode == "defensive":
            command = f"bash ~/defensive.sh {ip}"
        else:
            command = f"echo 'Invalid mode selected for {ip}'"

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode() + stderr.read().decode()
        client.close()

        return output if output else "No output from script."

    except Exception as e:
        return f"SSH error: {str(e)}"

# 🔹 API endpoint
@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    ip = data.get("ip")
    feature = data.get("feature")

    if feature == "kali":
        return jsonify({"output": start_kali_vm()})

    elif feature in ["offensive", "defensive"]:
        result = run_in_kali(ip, feature)
        return jsonify({"output": result})

    else:
        return jsonify({"output": "Feature not implemented yet."})


if __name__ == '__main__':
    app.run(debug=True)


