import threading
import time
import json
from mCastReceiver import Reciever
from broadcast import Broadcast    

def broadcast_info_continuously(interval=15):
    broadcaster = Broadcast("488_FAIL")

    print("Starting broadcast...")

    while True:
        try:
            # Simulate data generation (timestamp, location, sensors)
            timestamp = time.time()
            location = {"x": 10.5, "y": 20.3, "orientation": 180}
            sensors = {
                "sonar": [1.2, 2.3, 3.4],
                "lidar": [0.5, 1.0, 1.5, 2.0],
                "camera": "base64EncodedStringHere"
            }
            
            broadcaster.Broadcast_Info(timestamp, location, sensors)
            print("Broadcast message sent")

            # Wait before sending the next broadcast
            time.sleep(interval)

        except KeyboardInterrupt:
            print("Broadcasting stopped.")
            break
        except Exception as e:
            print(f"Error in broadcast thread: {e}")
            time.sleep(2)  # Shorter retry delay for improved resilience

def main():
    with open("key.json", "r") as config_file:
        config = json.load(config_file)
        SECRET_KEY = config["secret_key"].encode()

    recieverObj = Reciever(SECRET_KEY)
    receiver_thread = threading.Thread(target=recieverObj.receive(), daemon=True)
    broadcaster_thread = threading.Thread(target=broadcast_info_continuously, daemon=True)

    # Start threads
    receiver_thread.start()
    broadcaster_thread.start()

    # Main thread loop with error handling
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting gracefully...")

if __name__ == "__main__":
    main()
