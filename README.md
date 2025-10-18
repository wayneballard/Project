## ABOUT
Web-based application which allows for real-time observation of all the data from SenseHAT sensors in the form of GUI, as well as interaction with RGB matrix and on-board joystick.

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

```bash
git clone <repo_url>
cd <repo_name>
