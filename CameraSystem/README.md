[[EN](https://github.com/yunTum/MICS/blob/main/CameraSystem/README_EN.md)/JP]

# Camera System

## Python環境

#### [x64(Windows/Linux)]

- Python 3.9

- OpenVINO 2022.1

- DearPyGUI

- websocket-client

- Pillow

- numpy

- opencv-python

#### [Arm(Raspberry Pi 3B) + Intel NCS]

- Python 3.7

- OpenVINO 2020.3

- websocket-client

- Pillow

- numpy

- opencv-python

## 環境構築&実行方法

#### [Windows (x64, exe版)]

1. MICS Camera Systemのファイル(exe版)をダウンロードし、任意の場所に展開します。

2. 中にある "mics_camera_system.exe" を実行します。

#### [Windows (x64, Python版)]

1. Python3.9をインストールします。

2. 任意の仮想環境を構築します。

3. MICS Camera Systemのファイル(Python版)をダウンロードし、任意の場所に展開します。

4. "resources/platform.jsonc" を開き、中の説明に従い必要な項目を書き換えます。

5. 仮想環境を有効化します。

6. ターミナルで展開したフォルダに移動します。

7. 次のコマンドを順に入力してモジュールをインストールします。
   
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

8. "mics_camera_system.py" を実行します。
   
   ```
   python mics_camera_system.py
   ```

#### [Raspberry Pi 3B(Arm) + Intel NCS]

1. Python3.7をインストールします。
   
   ターミナルを開いて次のコマンドを入力してPython3.7をインストールしてください。
   
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

2. OpenVINO Runtime をダウンロードします。
   
   [Intel® Open Source Technology Center](https://download.01.org/opencv/2020/openvinotoolkit/2020.3/) からl_openvino_toolkit_runtime_raspbian_p_2020.3.34.tgzをダウンロードします。

3. ダウンロードしたフォルダに移動します。

4. インストール先のフォルダを作成します。
   
   ```
   sudo mkdir -p /opt/intel/openvino
   ```

5. ダウンロードしたファイルを展開します。
   
   ```sudo
   sudo tar -xf l_openvino_toolkit_runtime_raspbian_p_2020.3.34.tgz --strip 1 -C /opt/intel/openvino
   ```

6. 環境変数を更新します。(ターミナルを開くたびに実行する必要があります)
   
   ```
   source /opt/intel/openvino/bin/setupvars.sh
   ```
   
   (オプション) .bash_profileに書き込んで環境変数の更新を自動化します。
   
   下記のコマンドを実行すれば上記のコマンドを毎回実行する必要はありません。
   
   ```
   echo "source /opt/intel/openvino/bin/setupvars.sh" >> ~/.bashrc
   ```

7. Intel NCSを有効化します。
   
   ```
   sudo usermod -a -G users "$(whoami)"
   source /opt/intel/openvino/bin/setupvars.sh
   sh /opt/intel/openvino/install_dependencies/install_NCS_udev_rules.sh
   ```

8. 仮想環境を作成するために、任意の場所に移動します。

9. 仮想環境を作成します。
   
   ```
   python3.7 -m venv [任意の名前]
   ```

10. 仮想環境を有効化します。
    
    ```
    . [任意の名前]/bin/activate
    ```

11. 仮想環境の起動を自動化します。"/opt/intel/openvino/bin/setupvars.sh"をエディタで開きます。
    
    ```
    sudo nano /opt/intel/openvino/bin/setupvars.sh
    ```
    
    ファイルに次の文章を追記して保存します。
    
    ```
    command=". [仮想環境の絶対パス]/bin/activate"
    eval $command
    ```

12. MICS Camera Systemのファイル(Python版、RaspberryPI3+NCS用)をダウンロードし、任意の場所に展開します。

13. 展開した場所にターミナルで移動します。

14. 次のコマンドを順に入力してモジュールをインストールします。
    
    ```
    python -m pip install --upgrade pip
    pip install -r requirements_pi3.txt
    ```

15. ラズベリーパイに Intel NCS を接続していない場合は接続します。

16. "mics_camera_system.py" を実行します。
    
    ```
    python mics_camera_system.py
    ```

## 環境に合わせて必要な設定

#### [カメラに関する設定]

カメラの解像度、フレームレート、画角の設定が必要です。

GUI上で設定するか、"resources/settings.json"を編集してください。
