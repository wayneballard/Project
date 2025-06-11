import json

object = {"temeprature_sensor": {"temperature": 23.6,"Units": "degrees"},
          "humidity_sensor": {"humidity": 42, "Units": "%"},
          "pressure_sensor": {"pressure": 1012.8, "Units": "hPa"},
          "accelerometer":
                [{"x": 0.1, "Units": "g"},
                 {"y":0.02, "Units": "g"},
                 {"z":0.98, "Units": "g"}],
          "gyroscope":
            [{"x": 50, "Units": "degrees/s"},
             {"y":40, "Units": "degrees/s"},
             {"z":10, "Units": "degrees/s"}],
          "magnetometer":
               [{"x": 12.3, "Units": "\u03BCT"},
                {"x": -5.6, "Units": "\u03BCT"},
                {"x": 42.1, "Units": "\u03BCT"}] }

object_encoded = json.dumps(object, ensure_ascii=False, indent=1)


print(f"Temperature Sensor: \n{object_encoded}")


with open('output.json', 'w', encoding='utf-8') as j:
    json.dump(object_encoded, j, indent=1)

#Testing purposes
f = open('output.json')
data = json.load(f)
print(data)

