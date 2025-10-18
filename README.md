## ABOUT
Web-based application which allows for real-time observation of all the data from SenseHAT sensors in the form of GUI, as well as interaction with RGB matrix and on-board joystick. For detailed information click [here](./report.pdf)
![photo](./images/photo.png)

## Requirements

### Hardware
- Raspberry Pi (any model with GPIO support)
- Sense HAT attached to the Raspberry Pi

### Operating System
- Raspberry Pi OS (formerly Raspbian), Python 3.x installed

### Python Dependencies
Install the required Python packages:

```bash
sudo apt-get update
sudo apt-get install sense-hat
pip3 install Flask Flask-Cors sense-hat
```

### Installation
1. Clone the repository:
```bash
git clone <repo_url>
cd <repo_name>
```
2. Run the server:
```bash
python3 sense_server.py
```
3. Open a web-browser and navigate to:
```bash
http://<raspberry_pi_ip>:5000
```
