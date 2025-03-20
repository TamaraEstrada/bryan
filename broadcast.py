import socket
import json
import time
import hmac
import hashlib
import json
import base64

SECRET_KEY = b'Idontwanttofail'

class Broadcast:
    def __init__(self):
        # List of target IP addresses
        self.TARGET_IPS = [
            "10.170.9.14",
            "10.170.10.166", 
            "10.170.8.255",
            "10.170.10.165",
            "10.170.9.15"
        ]
        
        self.UDP_PORT = 5005  # Ensure receivers listen on this port
    
    def generate_hmac(self, payload: dict) -> str:
        # Generate an HMAC signature for the given payload.
        message = json.dumps(payload, separators=(',', ':')).encode('utf-8')
        signature = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()
        return base64.b64encode(signature).decode()
        
    def Broadcast_Info(self, timestamp, location, sensors):
        # Create the payload structure with the passed information
        payload = {
            "botId": 3,
            "timestamp": timestamp,
            "location": location,
            "sensors": sensors
        }
        
        hmac_signature = self.generate_hmac(payload) 

        secure_message = {
            "payload": payload,
            "hmac": hmac_signature
        }

        # Convert JSON payload to bytes
        MESSAGE = json.dumps(secure_message).encode('utf-8')
        
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Send the message to each IP address
        for ip in self.TARGET_IPS:
            try:
                sock.sendto(MESSAGE, (ip, self.UDP_PORT))
                print(f"JSON payload sent to {ip}")
            except Exception as e:
                print(f"Failed to send to {ip}: {e}")
        
        sock.close()