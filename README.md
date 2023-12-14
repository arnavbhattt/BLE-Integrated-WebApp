# BLE Integrated Web App (Health Monitoring System)
This project is a Python-based MQTT (Message Queuing Telemetry Transport) system for health monitoring. It leverages the Paho MQTT library for communication, Dash for creating a web-based dashboard, and Bleak for Bluetooth Low Energy (BLE) communication with a health monitoring device.

## **Prerequisites**
1. Python 3.x is required to run the script.
2. Install the required Python packages by running the command below.
3. Have a Bluetooth low-energy device or peripheral available for connection. "BLE Scanner" is an IOS app that allows the iPhone to act as a BLE peripheral.

**Getting Started**
1. Clone or download the project to your local machine.
2, Install the required Python packages by running pip install -r requirements.txt.
3. Modify the characteristic UUIDs in the publish.py script as needed. If using the BLE Scanner app, set up the device by adding "Advertiser," navigating to "BLE Device," and modifying the "Custom Services." Each service has a specific UUID, which is represented in the publish.py script. Change the service property of each to "Read/Write" for testing.

**Project Structure**
* subscribe.py: MQTT subscriber script that listens for EMG (Electromyography) data from the health monitoring device.
* publish.py: BLE (Bluetooth Low Energy) script that continuously reads data from the health monitoring device and publishes it via MQTT.
* app.js: JavaScript file for handling the web application.
* style.css: Cascading Style Sheets for styling the web application.
* package.json: Configuration file for managing Node.js dependencies.
* requirements.txt: List of Python dependencies.

**How to Use Locally**
1. Open a terminal or command prompt and navigate to the project directory.
2. Run `pip install -r requirements.txt` to install Python dependencies, if not already.
3. Run `npm install` to install Node.js dependencies.
5. Run `node app.js` to start the web application.
6. Before running the application, make sure that the device is turned on and ready to connect. Additionally, make sure the Device Name and all UUIDs in the publish.py script match the device's.
7. While the application is running, it will display values from those certain UUIDs in real-time. To send data values from the "BLE Scanner" app, navigate the to specific service UUID, tap on "SetValue?", select "Text", and enter any decimal value (ideally from 0.00 to 5.00).

**Functionality**
* The application initially connects to the Bluetooth low-energy device using the Bleak Python library. This allows it to work with all BLE characteristics from that device.
* BleakScanner then reads the value sent to the specific UUID.
* Such data is then sent to the Eclipse Mosquitto (MQTT) Broker, which continuously publishes to the stream of data requests.
* This is a subprocess (which runs in the background) to the subscribe.py script.
* subscribe.py subscribes from the MQTT Broker and sends that data to the respective callback function of the Dash graph.
* This process is repeated until the user/device stops sending data.

**Important Notes**
* Ensure that the BLE device is ready for connection when running subscribe.py.
* Check the specified BLE device information and adjust it in the code if needed.
* The package.json file manages the Node.js dependencies for running the web application.
