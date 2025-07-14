# OBS Monitor Client

This client script connects to a local OBS instance and reports status to your central OBS Monitoring Dashboard server.

## Requirements
- Python 3.7+
- OBS Studio with WebSocket enabled

## Installation

```bash
pip install -r requirements.txt
```

## Configuration
Edit `client.py` and set:
- `SERVER_URL` to your dashboard server’s address
- `DEVICE_ID` to a unique name for this machine
- `OBS_PASSWORD` to your OBS WebSocket password

## Usage

```bash
python client.py
```

The script will keep retrying if OBS is not running.

## Metrics Sent
- Streaming/Recording status
- Bitrate
- Dropped frames
- CPU/RAM usage
- Storage remaining 