from flask import Flask, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

mqtt_broker = "test.mosquitto.org"
mqtt_topic = "pot/voltage"
mqtt_topic2 = "pot/voltage2"

sensor_data1 = "No hay datos"
sensor_data2 = "No hay datos"

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT")
    client.subscribe([(mqtt_topic, 0), (mqtt_topic2, 0)])

def on_message(client, userdata, msg):
    global sensor_data1, sensor_data2
    if msg.topic == mqtt_topic:
        sensor_data1 = msg.payload.decode()
    elif msg.topic == mqtt_topic2:
        sensor_data2 = msg.payload.decode()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, 1883, 60)

@app.route('/')
def index():
    return render_template('index.html', sensor_data1=sensor_data1, sensor_data2=sensor_data2)

@app.route('/get_sensor_value1', methods=['GET'])
def get_sensor_value1():
    global sensor_data1
    return sensor_data1

@app.route('/get_sensor_value2', methods=['GET'])
def get_sensor_value2():
    global sensor_data2
    return sensor_data2

if __name__ == '__main__':
    client.loop_start()
    app.run(debug=True)
