from sense_hat import SenseHat
import json

sense = SenseHat()

def get_pressure():
	atmospheric_pressure = sense.get_pressure()

	json_pressure = {"value": atmospheric_pressure,
		 "units": "hPa"}


	print(json.dumps(json_pressure, indent=4, ensure_ascii=False))

def main():
	if __name__ == "__main__":
		get_pressure()

main()
