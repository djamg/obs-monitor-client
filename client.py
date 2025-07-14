import time
import requests
import obsws_python as obs
import psutil
import shutil
import configparser
import os

CONFIG_FILE = "config.ini"


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    section = config["client"]
    return {
        "server_url": section.get("server_url", "http://0.0.0.0:5500/api/status"),
        "device_id": section.get("device_id", "device_001"),
        "obs_host": section.get("obs_host", "localhost"),
        "obs_port": section.getint("obs_port", 4455),
        "obs_password": section.get("obs_password", ""),
    }


# Helper to get disk space in GB
def get_storage_remaining(path="/"):
    total, used, free = shutil.disk_usage(path)
    return free / (1024**3)  # GB


def get_obs_status(cl, device_id):
    try:
        stream_resp = cl.get_stream_status()
        record_resp = cl.get_record_status()
        stats_resp = cl.get_stats()
        # Bitrate in kbps, dropped frames, cpu, ram, storage
        bitrate = (
            stats_resp.output_bytes_per_sec * 8 / 1000
            if hasattr(stats_resp, "output_bytes_per_sec")
            else None
        )
        dropped_frames = getattr(stream_resp, "num_dropped_frames", None)
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        storage = get_storage_remaining()
        return {
            "device_id": device_id,
            "streaming": getattr(stream_resp, "output_active", False),
            "recording": getattr(record_resp, "output_active", False),
            "bitrate_kbps": bitrate,
            "dropped_frames": dropped_frames,
            "cpu_percent": cpu,
            "ram_percent": ram,
            "storage_gb": storage,
            "timestamp": time.time(),
        }
    except Exception as e:
        print(f"Error fetching OBS status: {e}")
        return {
            "device_id": device_id,
            "streaming": False,
            "recording": False,
            "bitrate_kbps": None,
            "dropped_frames": None,
            "cpu_percent": None,
            "ram_percent": None,
            "storage_gb": None,
            "timestamp": time.time(),
        }


def main():
    if not os.path.exists(CONFIG_FILE):
        print(
            f"Config file '{CONFIG_FILE}' not found. Please run the GUI configurator or create it manually."
        )
        return
    cfg = load_config()
    cl = None
    while True:
        try:
            if cl is None:
                cl = obs.ReqClient(
                    host=cfg["obs_host"],
                    port=cfg["obs_port"],
                    password=cfg["obs_password"],
                    timeout=3,
                )
                print("Attempting to connect to OBS WebSocket...")
            # Try a simple request to check connection
            cl.get_version()
            print("Connected to OBS WebSocket.")
            while True:
                status = get_obs_status(cl, cfg["device_id"])
                try:
                    resp = requests.post(cfg["server_url"], json=status)
                    print(f"Status sent: {status}, Response: {resp.status_code}")
                except Exception as e:
                    print(f"Error sending status: {e}")
                time.sleep(5)
        except Exception as e:
            print(f"Could not connect to OBS WebSocket or lost connection: {e}")
            cl = None
            time.sleep(5)


if __name__ == "__main__":
    main()
