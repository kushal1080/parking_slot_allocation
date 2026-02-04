# Expose all IoT modules for Phase 4
from .sensor_reader import update_slots_from_sensors
from .camera_plate_recognition import simulate_camera_checkins
from .mqtt_publisher import publish_loop
