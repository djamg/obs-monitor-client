# OBS Monitor Client - Release Guide

This guide will help you build and release the OBS Monitor Client as standalone executables.

## Prerequisites

1. **Python 3.7+** installed on Windows
2. **All dependencies** installed: `pip install -r requirements.txt`

## Quick Build

Run the automated build script:

```bash
python build_exe.py
```

This will:
- Install PyInstaller if needed
- Create an icon for the executables
- Build both GUI configurator and client executables
- Package everything into a release folder

## Manual Build Process

If you prefer to build manually:

### 1. Create Icon (Optional)
```bash
python create_icon.py
```

### 2. Build GUI Configurator
```bash
pyinstaller --onefile --windowed --name=OBS_Monitor_Configurator --icon=icon.ico --add-data=config.ini;. client_gui.py
```

### 3. Build Client
```bash
pyinstaller --onefile --console --name=OBS_Monitor_Client --icon=icon.ico --add-data=config.ini;. client.py
```

### 4. Create Release Package
Copy the executables from `dist/` folder and create a release package with:
- `OBS_Monitor_Configurator.exe`
- `OBS_Monitor_Client.exe`
- `config.ini` (if exists)
- `README.txt` (user instructions)

## Release Package Contents

Your release package should contain:

```
OBS_Monitor_Client_Release/
├── OBS_Monitor_Configurator.exe    # GUI configuration tool
├── OBS_Monitor_Client.exe          # OBS monitoring client
├── config.ini                      # Default configuration (optional)
└── README.txt                      # User instructions
```

## Distribution Options

### 1. Direct Distribution
- Zip the release folder
- Share via email, cloud storage, or direct download

### 2. GitHub Releases
1. Create a new release on GitHub
2. Upload the zipped release folder
3. Add release notes with version and changes

### 3. Installer Creation (Advanced)
For a more professional release, consider using:
- **Inno Setup** - Create Windows installers
- **NSIS** - Nullsoft Scriptable Install System
- **WiX Toolset** - Microsoft's installer framework

## Testing Your Release

Before distributing:

1. **Test on a clean machine** (without Python installed)
2. **Verify all functionality**:
   - GUI configurator opens and saves settings
   - Client connects to OBS and sends data
   - No missing dependencies
3. **Check file sizes** (should be reasonable, typically 10-50MB each)

## Troubleshooting Build Issues

### Common Problems:

1. **Missing dependencies**
   - Ensure all requirements are installed
   - Check for hidden imports in your code

2. **Large executable size**
   - Use `--exclude-module` to remove unused modules
   - Consider using `--onedir` instead of `--onefile` for faster startup

3. **Antivirus false positives**
   - Sign your executables with a code signing certificate
   - Submit to antivirus vendors for whitelisting

4. **Windows Defender blocking**
   - Add exclusion for your build directory
   - Consider code signing for production releases

## Version Management

For multiple releases:

1. **Update version numbers** in your code
2. **Create changelog** with new features/fixes
3. **Tag releases** in git
4. **Update documentation** for new features

## Security Considerations

1. **Code signing** - Sign executables for trust
2. **Virus scanning** - Scan before distribution
3. **Dependency auditing** - Keep dependencies updated
4. **User permissions** - Ensure proper file permissions

## Support and Maintenance

1. **Documentation** - Keep user guides updated
2. **Bug reports** - Provide clear reporting channels
3. **Updates** - Plan for future releases
4. **Compatibility** - Test with different Windows versions

## Advanced Customization

### Custom Icons
Replace `icon.ico` with your own icon file (256x256 recommended)

### Custom Branding
Modify the GUI title and styling in `client_gui.py`

### Additional Files
Add more files to the release package by modifying `build_exe.py`

### Auto-updates
Consider implementing auto-update functionality for future releases 