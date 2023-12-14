# BLE Integrated Web App (Health Monitoring System)
This project is a Python-based MQTT (Message Queuing Telemetry Transport) system for health monitoring. It leverages the Paho MQTT library for communication, Dash for creating a web-based dashboard, and Bleak for Bluetooth Low Energy (BLE) communication with a health monitoring device.
**Prerequisites**
1. Python 3.x is required to run the script.
2. Install the required Python packages by running the command below.
3. Have a Bluetooth low-energy device or peripheral available for connection. "BLE Scanner" is an IOS app that allows iPhone to act as such a BLE peripheral.

**Getting Started**
1. Clone or download the project to your local machine.
2, Install the required Python packages by running pip install -r requirements.txt.
3. Modify the characteristic uuids in the publish.py script as needed. If using the BLE Scanner app, set up device by adding "Advertiser," navigating to "BLE Device," and modifying the "Custom Services." Each service has a specific uuid, which is represented in the publish.py script.

**Project Structure**
* subscribe.py: MQTT subscriber script that listens for EMG (Electromyography) data from the health monitoring device.
* publish.py: BLE (Bluetooth Low Energy) script that continuously reads data from the health monitoring device and publishes it via MQTT.
* app.js: JavaScript file for handling the web application.
* style.css: Cascading Style Sheets for styling the web application.
* package.json: Configuration file for managing Node.js dependencies.
* requirements.txt: List of Python dependencies.

**How to Use**
1. Open a terminal or command prompt and navigate to the directory containing the script.
2. Run the script using python Automate.py.

3. 

**Functionality**
1. Login: The script will prompt you to enter your LinkedIn email or phone number and password. It will then log in to your LinkedIn account.
2. Filter Company Links: The script will ask you to enter the name of a company you are interested in. It will search for the company on Google and navigate to its LinkedIn page. Currently, it searches for people related to the "recruitment" keyword on the company page.
3. Retrieve People Links: The script will extract the links to the profiles of people related to the recruitment keyword and store them in a list. This list is stored in a SQL database, that can then be exported into an Excel file as per the user's command.
4. Detect Closed Window: The script continuously checks if the browser window is closed by the user, and if so, it terminates the script.

**SQL Database Schema**   

employees(    
&ensp; &nbsp; &nbsp;first_name TEXT,  
&ensp; &nbsp; &nbsp;last_name TEXT,  
&ensp; &nbsp; &nbsp;job_title TEXT,  
&ensp; &nbsp; &nbsp;profile_url TEXT);  
