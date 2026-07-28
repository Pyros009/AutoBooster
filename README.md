# AutoBooster
A lightweight computer vision-based auto-clicker for boosting a server.
Uses Bluestacks as interface.

- Status: under active development, approaching first stable release.

## Overview
Autobooster uses computer vision to detect specific UI elements on the screen and automatically
perform the required clicks at the appropriate time.

Once the boost cycle is fully complete, or under manual request, the application stops automatically.

Requirements (v0.9.x):
- Bluestacks with ADB turned on
- Resolution 960 x 540
- 160 DPI

    Note: Other resolutions or DPI settings are not officially supported in v0.9.x and may lead to incorrect template detection or inaccurate clicks.

## Features

- Automatic ADB detection
- Automatic updates
- Computer vision-based target detection
- Automatic stop after the boost cycle is completed
- Portable executable

## Known issues
 - Unsupported screen resolutions or DPI settings may cause detection errors, loops, or missed clicks.

## Roadmap
- add automatic rollback on failed program update
- improve installation and configuration documentation
- prepare the first stable release
- add more resolution/dpi compatibility options

## Changelog

### 0.9.4
- Completed automatic application patching

### 0.9.3
- Added logging system
- Added automatic program update framework

### 0.9.2
- Added program updater foundation

### 0.9.1
- Added additional troubleshooting support