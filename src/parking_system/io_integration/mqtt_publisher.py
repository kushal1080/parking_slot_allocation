import time
import json
import paho.mqtt.client as mqtt
from parking_system.core import slot_manager

# MQTT configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "parking/slots"

# MQTT client instance
client = mqtt.Client()

def connect_mqtt():
    """
    Connect to the MQTT broker safely.
    """
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        print(f"[MQTT] Connected to broker at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"[MQTT] Connection failed: {e}")

def publish_slot_status(slot_id: int):
    """
    Publish the current slot occupancy via MQTT.
    """
    slot = slot_manager.get_slot_by_id(slot_id)
    if slot:
        payload = json.dumps(slot)
        try:
            client.publish(MQTT_TOPIC, payload)
            print(f"[MQTT] Published slot {slot_id} status")
        except Exception as e:
            print(f"[MQTT] Publish failed for slot {slot_id}: {e}")

def publish_loop():
    """
    Continuously publish all slots every 2 seconds.
    Safe against broker connection issues.
    """
    connect_mqtt()
    while True:
        try:
            slots = slot_manager.list_slots()
            for s in slots:
                publish_slot_status(s["id"])
        except Exception as e:
            print(f"[MQTT] Loop error: {e}")
        time.sleep(2)
