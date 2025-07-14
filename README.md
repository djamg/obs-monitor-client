# OBS Monitor Client

This client script connects to a local OBS instance and reports status to your central OBS Monitoring Dashboard server.

## Features

- **GUI Configuration**: Easy-to-use interface for setting up connection parameters
- **Real-time Monitoring**: Tracks streaming/recording status, bitrate, dropped frames, CPU/RAM usage, and storage
- **Automatic Reconnection**: Handles OBS connection drops gracefully
- **Standalone Executables**: Can be built into Windows executables for easy distribution

## Requirements
- Python 3.7+
- OBS Studio with WebSocket enabled

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Development Mode
```bash
# Run the GUI configurator
python client_gui.py

# Run the monitoring client
python client.py
```

### Building Executables
To create standalone Windows executables:

```bash
# Install build dependencies
pip install -r requirements.txt

# Run the automated build script
python build_exe.py
```

This creates:
- `OBS_Monitor_Configurator.exe` - GUI configuration tool
- `OBS_Monitor_Client.exe` - OBS monitoring client

See `RELEASE_GUIDE.md` for detailed build instructions.

## Configuration

The application uses `config.ini` for settings:

```ini
[client]
server_url = http://your-server:5500/api/status
device_id = your_device_name
obs_host = localhost
obs_port = 4455
obs_password = your_obs_websocket_password
```

## Metrics Sent
- Streaming/Recording status
- Bitrate (kbps)
- Dropped frames
- CPU usage (%)
- RAM usage (%)
- Storage remaining (GB)

## Project Structure

```
obs-monitor-client/
├── client_gui.py          # GUI configuration interface
├── client.py              # OBS monitoring client
├── config.ini             # Configuration file
├── requirements.txt       # Python dependencies
├── build_exe.py          # Automated build script
├── create_icon.py        # Icon generation script
├── RELEASE_GUIDE.md      # Build and release instructions
└── README.md             # This file
```

## Development

### Adding New Metrics
To add new monitoring metrics, modify the `get_obs_status()` function in `client.py`.

### Customizing the GUI
The GUI is built with tkinter and styled with a dark theme. Modify `client_gui.py` to change the appearance.

## Troubleshooting

- **Connection Issues**: Ensure OBS WebSocket is enabled and password is correct
- **Missing Dependencies**: Run `pip install -r requirements.txt`
- **Build Issues**: See `RELEASE_GUIDE.md` for detailed troubleshooting

## License

[Add your license here]

## Contributing

[Add contribution guidelines here] 