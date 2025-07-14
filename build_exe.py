#!/usr/bin/env python3
"""
Build script for OBS Monitor Client executable
"""
import os
import subprocess
import sys
import shutil

def clean_build():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            print(f"Removing {file}...")
            os.remove(file)

def build_gui_exe():
    """Build the GUI configurator executable"""
    print("Building GUI configurator executable...")
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=OBS_Monitor_Configurator',
        '--icon=icon.ico' if os.path.exists('icon.ico') else '',
        '--add-data=config.ini;.',
        'client_gui.py'
    ]
    cmd = [arg for arg in cmd if arg]  # Remove empty strings
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ GUI configurator executable built successfully!")
    else:
        print("✗ Failed to build GUI configurator:")
        print(result.stderr)
        return False
    return True

def build_client_exe():
    """Build the client executable"""
    print("Building client executable...")
    cmd = [
        'pyinstaller',
        '--onefile',
        '--console',
        '--name=OBS_Monitor_Client',
        '--icon=icon.ico' if os.path.exists('icon.ico') else '',
        '--add-data=config.ini;.',
        'client.py'
    ]
    cmd = [arg for arg in cmd if arg]  # Remove empty strings
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Client executable built successfully!")
    else:
        print("✗ Failed to build client executable:")
        print(result.stderr)
        return False
    return True

def create_release_package():
    """Create a release package with both executables and documentation"""
    print("Creating release package...")
    
    # Create release directory
    release_dir = "OBS_Monitor_Client_Release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    # Copy executables
    if os.path.exists('dist/OBS_Monitor_Configurator.exe'):
        shutil.copy2('dist/OBS_Monitor_Configurator.exe', release_dir)
        print("✓ Copied GUI configurator")
    
    if os.path.exists('dist/OBS_Monitor_Client.exe'):
        shutil.copy2('dist/OBS_Monitor_Client.exe', release_dir)
        print("✓ Copied client executable")
    
    # Copy config file
    if os.path.exists('config.ini'):
        shutil.copy2('config.ini', release_dir)
        print("✓ Copied config file")
    
    # Create README for release
    release_readme = f"""# OBS Monitor Client - Release

## Quick Start

1. **Configure the client:**
   - Run `OBS_Monitor_Configurator.exe` to set up your connection settings
   - Enter your server URL, device ID, and OBS WebSocket credentials
   - Click "Save Config"

2. **Start monitoring:**
   - Run `OBS_Monitor_Client.exe` to start monitoring OBS
   - The client will automatically connect to OBS and send status updates

## Requirements
- Windows 10/11
- OBS Studio with WebSocket enabled
- Internet connection to reach your monitoring server

## Files
- `OBS_Monitor_Configurator.exe` - Configuration GUI
- `OBS_Monitor_Client.exe` - OBS monitoring client
- `config.ini` - Configuration file (created by configurator)

## Troubleshooting
- Make sure OBS Studio is running with WebSocket enabled
- Check that your server URL is correct and accessible
- Verify your OBS WebSocket password is correct
- The client will automatically retry connections if OBS is not running

## Support
For issues or questions, please refer to the main project documentation.
"""
    
    with open(os.path.join(release_dir, 'README.txt'), 'w') as f:
        f.write(release_readme)
    
    print(f"✓ Release package created in '{release_dir}' directory")
    return release_dir

def main():
    print("=== OBS Monitor Client Build Script ===")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Clean previous builds
    clean_build()
    
    # Build executables
    if not build_gui_exe():
        return
    
    if not build_client_exe():
        return
    
    # Create release package
    release_dir = create_release_package()
    
    print("\n=== Build Complete ===")
    print(f"Release package created in: {release_dir}")
    print("You can now distribute the contents of this folder to users.")
    print("\nFiles created:")
    print("- OBS_Monitor_Configurator.exe (GUI configurator)")
    print("- OBS_Monitor_Client.exe (monitoring client)")
    print("- README.txt (user instructions)")

if __name__ == "__main__":
    main() 