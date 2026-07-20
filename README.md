# AutoBooster
A lightweight computer vision-based auto-clicker for boosting a server.
Uses Bluestacks as interface.

- Status: under active development.

## Overview
Autobooster uses computer vision to detect specific UI elements on the screen and automatically
perform the required clicks at the appropriate time.

Once the boost cycle is fully complete or on demand, the application stops automatically.

Requirements (v0.9.x):
- Bluestacks with ADB turned on
- Resolution 960 x 540
- 160 DPI

    Note: Other resolutions or DPI settings are not officially supported in v0.9.x and may lead to incorrect template detection or inaccurate clicks.

## Features

Automatic ADB detection
Automatic updates*
Computer vision-based target detection
Automatic stop after the boost cycle is completed
Portable executable

* Current status: Target updates are fully automatic. Application self-updates are still under development and will be completed before the full release.

patch version 0.9.1
- added further troubleshooting support
