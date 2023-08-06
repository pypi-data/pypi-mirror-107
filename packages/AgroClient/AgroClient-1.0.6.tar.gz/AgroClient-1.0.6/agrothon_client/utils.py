from gpiozero import MotionSensor, OutputDevice
from cv2 import VideoCapture, imencode
from .request_helper import *
import io
import logging
from serial import Serial
from agrothon_client import (
    USB_PORT,
    USB_BAUD_RATE,
    RELAY_GPIO,
    PIR1_GPIO,
    PIR2_GPIO,
    PIR3_GPIO,
    PIR4_GPIO
    )

serial_in = Serial(USB_PORT, USB_BAUD_RATE)

pump = OutputDevice(RELAY_GPIO, active_high=True, initial_value=True)

pir1 = MotionSensor(PIR1_GPIO)
pir2 = MotionSensor(PIR2_GPIO)
pir3 = MotionSensor(PIR3_GPIO)
pir4 = MotionSensor(PIR4_GPIO)

LOGGER = logging.getLogger(__name__)


def motion_intruder_detect():
    LOGGER.info("Starting Intruder Module")
    while True:
        if pir1.motion_detected or pir2.motion_detected or pir3.motion_detected or pir4.motion_detected:
            LOGGER.info(f"PIR1 : {pir1.value}, PIR2 : {pir2.value}, PIR3 : {pir3.value}. PIR4 : {pir4.value}")
            LOGGER.info("Launching camera")
            img_cap = VideoCapture(0)
            check, frame = img_cap.read()
            is_success, cv2_img = imencode(".jpg", frame)
            img_cap.release()
            if is_success:
                data = io.BytesIO(cv2_img)
                resp = image_poster(data)
                if resp:
                    LOGGER.info(f"Intruder Detected:{str(resp)}")
                else:
                    LOGGER.error("maybe nothing found")


def serial_sensor_in():
    """
    This Module just get the Serial lines from Arduino nano and decode them
    """
    LOGGER.info("Starting Sensor module")
    while True:
        if serial_in.in_waiting:
            serial_line = serial_in.readline().decode('utf-8').strip()
            list_of_values = serial_line.split(",")
            try:
                no_of_moist_sens = len(list_of_values)-2
                moist_list = [] * no_of_moist_sens
                for i in range(no_of_moist_sens):
                    moist_list.append(float(list_of_values[i]))
                sensor_dict = {"no_of_sensors": no_of_moist_sens, "moisture": moist_list, "humidity": float(list_of_values[len(list_of_values)-1]), "temperature":float(list_of_values[len(list_of_values)-2])}
                sensor_data_post(json=sensor_dict)
            except ValueError:
                LOGGER.error(serial_line)
                LOGGER.error("DHT Data read failed")
                pass

def pump_status():
    LOGGER.info("Starting Pump status Check")
    while True:
        resp = pump_status_check()
        if resp:
            pump.off()

            LOGGER.info(f"Pump is {pump.value}")
        elif not resp:
            pump.on()
            LOGGER.info(f"Pump is {pump.value}")
        else:
            LOGGER.error("Bruhhhh....")
            pass

