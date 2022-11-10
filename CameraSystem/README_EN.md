[EN/[JP](https://github.com/yunTum/MICS/blob/main/CameraSystem/README.md)]

# Camera System

## Python Environment

#### [x64(Windows/Linux)]

- Python 3.9

- OpenVINO 2022.1

- DearPyGUI

- websocket-client

- Pillow

- numpy

- opencv-python

#### [Raspberry Pi 3B(Arm) + Intel NCS]

- Python 3.7

- OpenVINO 2020.3

- websocket-client

- Pillow

- numpy

- opencv-python

## How to build & run

#### [Windows (x64, exe version)]

1. Download the MICS Camera System file (exe version) and extract it to the desired location.

2. Run the file "mics_camera_system.exe".

#### [Windows (x64, Python Edition)

1. Install Python 3.9.

2. Create a virtual environment of your choice.

3. Download the MICS Camera System file (Python version) and extract it to an arbitrary location.

4. Open "resources/platform.jsonc" and rewrite the necessary items according to the instructions in the file.

5. Activate the virtual environment.

6. Go to the extracted folder in Terminal.

7. Install the module by entering the following commands in order.
   
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

8. Run "mics_camera_system.py".
   
   ```
   python mics_camera_system.py
   ```

#### [Arm(Raspberry Pi 3B) + Intel NCS]

1. Install Python 3.7 . Open a terminal and type the following command to install Python 3.7 .
   
   ```
    sudo apt-get update
    sudo apt-get upgrade -y
   
    wget https://www.python.org/ftp/python/3.7.13/Python-3.7.13.tgz
   
    tar zxvf Python-3.7.13.tgz
   
    cd Python-3.7.13
    ./configure --enable-shared
    make
    sudo make install
   
    python3.7 -v
   ```

2. Download the OpenVINO Runtime.
   
   Download l_openvino_toolkit_runtime_raspbian_p_2020.3.34.tgz from [Intel® Open Source Technology Center](https://download.01.org/opencv/2020/openvinotoolkit/2020.3/) .

3. Navigate to the folder where you downloaded the software.

4. Create a destination folder for installation.
   
   ```
   sudo mkdir -p /opt/intel/openvino
   ```

5. Extract the downloaded file.
   
   ```sudo
   sudo tar -xf l_openvino_toolkit_runtime_raspbian_p_2020.3.34.tgz --strip 1 -C /opt/intel/openvino
   ```

6. Updates environment variables. (Must be run each time the terminal is opened)
   
   ```
   source /opt/intel/openvino/bin/setupvars.sh
   ```
   
   (Optional) Automate environment variable updates by writing them to .bash_profile. You do not need to execute the above commands each time if you execute the following commands.
   
   ```
   echo "source /opt/intel/openvino/bin/setupvars.sh" >> ~/.bashrc
   ```

7. Activate Intel NCS.
   
   ```
   sudo usermod -a -G users "$(whoami)"
   source /opt/intel/openvino/bin/setupvars.sh
   sh /opt/intel/openvino/install_dependencies/install_NCS_udev_rules.sh
   ```

8. Go to any location to create a virtual environment.

9. Create a virtual environment.
   
   ```
   python3.7 -m venv [Any name]
   ```

10. Activate the virtual environment.
    
    ```
    . [Any name]/bin/activate
    ```

11. Automate the startup of the virtual environment. Open the file "/opt/intel/openvino/bin/setupvars.sh" in your editor.
    
    ```
    sudo nano /opt/intel/openvino/bin/setupvars.sh
    ```
    
    Add the following text to the file and save it.
    
    ```
    command=". [path of a virtual environment]/bin/activate"
    eval $command
    ```

12. Download the MICS Camera System file (Python version, for RaspberryPI3+NCS) and extract it to the desired location.

13. Navigate to the extracted location using a terminal.

14. Install the module by entering the following commands in order
    
    ```
    python -m pip install --upgrade pip
    pip install -r requirements_pi3.txt
    ```

15. Connect the Intel NCS to the Raspberry Pi if it is not already connected.

16. Run "mics_camera_system.py".
    
    ```
    python mics_camera_system.py
    ```

## Configuration required for the environment

#### [Camera Settings]

The resolution, frame rate, and angle of view of the camera must be set. Set these in the GUI or edit "resources/settings.json".
