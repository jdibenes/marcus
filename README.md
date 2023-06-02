# MARCuS: Milly Augmented Reality Cube Solver

HoloLens 2 Rubik's cube guide.
The guide consists of a **Python client script that runs on a desktop machine** (Tested on Windows 10 and Ubuntu 22.04) and a **Unity server application that runs on the HoloLens**.
Real-time video streaming and server-client communications enabled by [hl2ss](https://github.com/jdibenes/hl2ss).

**Demo**
https://youtu.be/iQYMZVgmVAc

## Preparation

Before using the server software configure your HoloLens as follows:

1. Enable developer mode: Settings -> Update & Security -> For developers -> Use developer features.
2. Enable device portal: Settings -> Update & Security -> For developers -> Device Portal.
3. Enable research mode: Refer to the Enabling Research Mode section in [HoloLens Research Mode](https://docs.microsoft.com/en-us/windows/mixed-reality/develop/advanced-concepts/research-mode).

Please note that **enabling Research Mode on the HoloLens increases battery usage**.

## Installation (sideloading)

The server application is distributed as a single appxbundle file and can be installed using one of the two following methods.

**Method 1**

1. On your HoloLens, open Microsoft Edge and navigate to this repository.
2. Download the [latest appxbundle](https://github.com/jdibenes/marcus/releases).
3. Open the appxbundle and tap Install.

**Method 2**

1. Download the [latest appxbundle](https://github.com/jdibenes/marcus/releases).
2. Go to the Device Portal (type the IP address of your HoloLens in the address bar of your preferred web browser) and upload the appxbundle to the HoloLens (System -> File explorer -> Downloads).
3. On your HoloLens, open the File Explorer and locate the appxbundle. Tap the appxbundle file to open the installer and tap Install.

You can find the server application (PTG Rubiks) in the All apps list.

## Permissions

The first time the server runs it will ask for the necessary permissions to access sensor data. If there are any issues please verify that the server application (PTG Rubiks.exe) has access to:

- Camera (Settings -> Privacy -> Camera).
- Eye tracker (Settings -> Privacy -> Eye tracker).
- Microphone (Settings -> Privacy -> Microphone).
- User movements (Settings -> Privacy -> User movements).

## Using the software

1. Run the server application on your HoloLens.
2. Set the host variable of the [client.py](https://github.com/jdibenes/marcus/blob/main/guide/client.py) script to your HoloLens IP address.
3. Run [client.py](https://github.com/jdibenes/marcus/blob/main/guide/client.py).
4. Follow the instructions displayed on your HoloLens.

**Required Python packages**

- [OpenCV](https://github.com/opencv/opencv-python) `pip install opencv-python`
- [Open3D](http://www.open3d.org/) `pip install open3d`
- [PyAV](https://github.com/PyAV-Org/PyAV) `pip install av`
- [NumPy](https://numpy.org/) `pip install numpy`
- [Websockets](https://github.com/aaugustin/websockets) `pip install websockets`
- [skimage](https://scikit-image.org/docs/stable/install.html)
- [kociemba](https://github.com/muodov/kociemba) `pip install kociemba`

## Building the Unity server application

The server application was developed in Unity 2020.3.42f1.

1. Open the project in Unity. If the MRTK Project Configurator window pops up just close it.
2. Go to Build Settings (File -> Build Settings).
3. Switch to Universal Windows Platform.
4. Set Target Device to HoloLens.
5. Set Architecture to ARM64.
6. Set Build and Run on Remote Device (via Device Portal).
7. Set Device Portal Address to your HoloLens IP address (e.g., https://192.168.1.7) and set your Device Portal Username and Password.
8. Click Build and Run. Unity may ask for a Build folder. You can create a new one named Build.

## References
