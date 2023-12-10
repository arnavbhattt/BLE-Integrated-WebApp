import time
import paho.mqtt.client as mqtt
import asyncio
from bleak import BleakScanner, BleakClient

# BLE device information
device_name = 'BLE Device'  # Replace with your BLE device's address
characteristic_uuid1 = 'd395c564-68a8-4174-bd9f-f95a6ffde52f'  # Replace with the desired characteristic UUID
characteristic_uuid_2 = 'ee2e9261-698b-43d4-b328-f39b0fe5761e'  # Replace with the second characteristic UUID

# MQTT Client
mqttc = mqtt.Client()
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)


async def connect_to_ble_device(device_name):
    print("Scanning for BLE devices...")

    devices = await BleakScanner.discover()
    target_device = next((device for device in devices if device.name == device_name), None)

    if not target_device:
        print(f"Device with name '{device_name}' not found.")
        return None

    print(f"Connecting to BLE device '{device_name}'...")

    try:
        client = BleakClient(target_device.address)
        await client.connect()
        return client

    except Exception as e:
        print(f"Error: {e}")
        return None


async def read_ble_and_publish_mqtt(client, characteristic_uuid, mqtt_topic):

    try:
        # Read the value of the specified characteristic
        value = await client.read_gatt_char(characteristic_uuid)
        converted_val = float(value.decode('utf-8'))

        # Publish the value using MQTT
        mqttc.publish(mqtt_topic, converted_val)
        #  await asyncio.sleep(2)

    except Exception as e:
        print(f"Error: {e}")

async def main():
    ble_client = await connect_to_ble_device(device_name)

    if ble_client:
        while True:
            await read_ble_and_publish_mqtt(ble_client, characteristic_uuid1, "sensor/emg1")
            await read_ble_and_publish_mqtt(ble_client, characteristic_uuid_2, "sensor/emg2")

# Main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
