import socket
import struct
import json
import hashlib
import base64
import hmac

class Reciever():
    def __init__(self, key):
        SECRET_KEY = key
    

    def verify_hmac(self, received_payload: dict, received_hmac: str) -> bool:
        """Verify the HMAC signature."""
        message = json.dumps(received_payload, separators=(',', ':')).encode('utf-8')
        expected_signature = hmac.new(self.SECRET_KEY, message, hashlib.sha256).digest()
        expected_hmac = base64.b64encode(expected_signature).decode()

        return hmac.compare_digest(received_hmac, expected_hmac)

    def receive(self):
        MULTICAST_GROUP = "239.1.1.1"
        UDP_PORT = 5005

        # Create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", UDP_PORT))

        # Join the multicast group
        mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print("Listening for JSON multicast messages...")

        while True:
            try:
                data, addr = sock.recvfrom(4096)  # Increase buffer size for larger JSON payloads
                decoded_data = data.decode("utf-8")  # Decode bytes to string

                try:
                    json_data = json.loads(decoded_data)  # Convert string to dictionary
                    
                    # Extract values safely
                    received_payload = json_data.get("payload")
                    received_hmac = json_data.get("hmac")

                    if received_payload is not None and received_hmac is not None:
                        if self.verify_hmac(received_payload, received_hmac):
                            print(f"Received valid JSON from {addr}: {json.dumps(json_data, indent=4)}")
                        else:
                            print(f"Received JSON from {addr}, but HMAC verification failed!")
                    else:
                        print(f"Malformed JSON from {addr}: {json_data}")

                except json.JSONDecodeError:
                    print(f"Received non-JSON message from {addr}: {decoded_data}")

            except Exception as e:
                print(f"Error receiving data: {e}")

