import os
import socket
import subprocess

# Auto-detect local IP address
ip = socket.gethostbyname(socket.gethostname())

print(f"Starting Django server at: http://{ip}:8000")

# Run Django server with the IP
subprocess.run(["python", "manage.py", "runserver", f"{ip}:8000"])
