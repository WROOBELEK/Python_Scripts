from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

def get_fake_data():
    try:
        tempDS18B20 = round(random.uniform(20.0, 30.0), 1)
        tempBME280 = round(random.uniform(20.0, 30.0), 1)

        humidity = random.randint(50, 60)

        pressure = random.randint(980, 1020)

        lightState = random.choice([0, 1])
        
        soilState = random.choice([0, 1])

        data = {
            "dstemperature": tempDS18B20,
            "bmetemperature": tempBME280,
            "humidity": humidity,
            "pressure": pressure,
            "illumination": "0" if lightState == 1 else "1",
            "soil": "0" if soilState == 1 else "1"
        }
        return data
    except Exception as e:
        print(e)
        return None


@app.route('/fake1', methods=['GET'])
def fake1():
    return jsonify(get_fake_data())

@app.route('/fake2', methods=['GET'])
def fake2():
    return jsonify(get_fake_data())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
