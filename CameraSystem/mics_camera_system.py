# mics_dev_1
# 2022 kasys1422
# The core app of MICS(Measuring Interest with a Camera System)
VERSION = '0.0.8'

# Import
import math
import os
import numpy as np
import cv2
import time
import datetime
import csv
import json
from openvino.inference_engine import IECore
import dearpygui.dearpygui as dpg
import websocket
import _thread as thread
from time import sleep
import gettext
import locale

# Constant
#PLATFORM = 'Raspberry Pi (arm64)'
#PLATFORM = 'Linux (x86/x64)'
PLATFORM = 'Windows (x86/x64)'
SYSTEM_START_TIME = datetime.datetime.now()
THRESHOLD_PERSON_DETECTION = 0.75
THRESHOLD_FACE_DETECTION = 0.95
DISTANCE_MAGNIFICATION = 1.0                    #1.16
THRESHOLD_PERSON_REIDENTIFICATION = 0.60        #Threshold of Cosine Similarity
SETTING_FILE_PATH = './resources/settings.json'
LAYOUT_SETTING_FILE_PATH = './resources/layout.ini'
COLORS_16 = ((173,255, 47),
             (255,215,  0),
             (255,182,193),
             (255,140,  0),
             (  0,  0,255),
             (  0,  0,128),
             (  0,128,128),
             (  0,128,  0),
             (  0,255,  0),
             (  0,255,255),
             (255,255,  0),
             (255,  0,  0),
             (255,  0,255),
             (128,128,  0),
             (128,  0,128),
             (128,  0,  0))


# Setting param
device_name = 'MYRIAD'                         # Use MYRIAD
device_name = 'CPU'                             # Use CPU
save_mode = 'SERVER'
#save_mode = 'CSV'
server_address = "ws://fast-fjord-64260.herokuapp.com"
server_address = 'ws://localhost:8000'         #"ws://fast-fjord-64260.herokuapp.com" 'ws://localhost:8000'
angle_of_view = 70                              # Angle must be within 180 degrees
cam_id = 0
cam_x = 1280
cam_y = 720
cam_fps = 30           
size_of_interest_check_area = 70                #(cm)    
interest_check_area_offset = 0
save_way_csv = 'Per software launch'
auto_start = True
show_additional_info = True

is_running = True

# Functions

# RestartFlag
restart_flag = False
def RestartCameraSystem():
    global restart_flag
    restart_flag = True

# FPS
fps_time = [time.time(), time.time()]
frame_rate = 0.0
def DrawFPS(frame, fps_time, x:int, y:int):
    fps_time[0] = time.time()
    frame_rate = 1/(fps_time[0] - fps_time[1])
    cv2.putText(frame, text=str(int(frame_rate))+'fps', org=(x, y + 10), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    fps_time[1] =  fps_time[0]
    return frame_rate

def SetupCamera(cam_id, width, height, fps):
    try:
        camera = cv2.VideoCapture(cam_id)
    except:
        camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, max(0,min(7680,int(width))))
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT,max(0,min(4320,int(height))))
    camera.set(cv2.CAP_PROP_FPS, max(0,min(60,int(fps))))
    return camera

def SetupCSV():
    if not os.path.exists('csv'):
        os.makedirs('csv')
    global save_way_csv
    if save_way_csv == 'Per date':
        with open('./csv/MICS_' + SYSTEM_START_TIME.strftime('%Y%m%d') + '.csv', 'a', newline='') as f:
            writer = csv.writer(f)
    elif save_way_csv == 'Identical file':
        with open('./csv/MICS_DATA.csv', 'a', newline='') as f:
            writer = csv.writer(f)
    else:
        with open('./csv/MICS_' + SYSTEM_START_TIME.strftime('%Y%m%d%H%M%S') + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'interested', 'age', 'gender', 'start_time', 'end_time'])
    PrintConsleWindow("[Info] Launch as CSV MODE")

def SetupModel(ie_core, device_name, model_path_without_extension):
    net  = ie_core.read_network(model=model_path_without_extension + '.xml', weights=model_path_without_extension + '.bin')
    input_name  = next(iter(net.input_info))
    input_shape = net.input_info[input_name].tensor_desc.dims
    out_name    = next(iter(net.outputs))
    out_shape   = net.outputs[out_name].shape
    try:
        exec_net    = ie_core.load_network(network=net, device_name=device_name, num_requests=1)  
    except RuntimeError:
        PrintConsleWindow('[ERROR] Can not setup device(' + device_name + '). Using CPU.')
        try:
            exec_net    = ie_core.load_network(network=net, device_name='CPU', num_requests=1)
        except RuntimeError:
            PrintConsleWindow('[ERROR] Can not setup device(CPU). Using MYRIAD.')
            try:
                exec_net    = ie_core.load_network(network=net, device_name='MYRIAD', num_requests=1)
            except RuntimeError:
                PrintConsleWindow('[ERROR] Can not setup device(MYRIAD). Using GPU.')
                try:
                    exec_net    = ie_core.load_network(network=net, device_name='GPU', num_requests=1)
                except RuntimeError:
                    raise ValueError("No corresponding processor was found.")
    del net
    return input_name, input_shape, out_name, out_shape, exec_net

def GetDetectionData(frame, exec_net, input_name, input_shape):
    exec_frame = cv2.resize(frame, (input_shape[3], input_shape[2]))
    exec_frame = exec_frame.transpose((2, 0, 1))
    exec_frame = exec_frame.reshape(input_shape)
    result = exec_net.infer(inputs={input_name: exec_frame})
    return result

def GetXYMinMaxFromDetection(input_object, frame):
    x_min = abs(int(input_object[3] * frame.shape[1]))
    y_min = abs(int(input_object[4] * frame.shape[0]))
    x_max = abs(int(input_object[5] * frame.shape[1]))
    y_max = abs(int(input_object[6] * frame.shape[0]))
    return  [x_min, y_min, x_max, y_max]

def GetAgeGenderData(face_frame, exec_net, input_name, input_shape):
    detection = GetDetectionData(face_frame, exec_net, input_name, input_shape)
    age = int(np.squeeze(detection['age_conv3']) * 100)
    prob = np.squeeze(detection['prob'])
    if prob[0] < prob[1]:
        gender = 'male'
    else:
        gender = 'female'
    result = [age, gender]
    return result

def GetFaceLandmarkDetectionData(face_frame, exec_net, input_name, input_shape, out_name, face_pos):
    landmaeks = GetDetectionData(face_frame, exec_net, input_name, input_shape)
    result = landmaeks[out_name][0][:]

    for i in range(len(result)):
        result[i] = face_pos[i % 2] + result[i] * face_frame.shape[(i + 1) % 2]
    return result.reshape(int(len(result) / 2), 2)

def GetHeadPoseEstimationData(face_frame, exec_net, input_name, input_shape):
    head_pose_data = GetDetectionData(face_frame, exec_net, input_name, input_shape)
    # [yaw, pitch, roll]
    result = [head_pose_data['angle_y_fc'][0][0], head_pose_data['angle_p_fc'][0][0], head_pose_data['angle_r_fc'][0][0]]
    return result

def DrawHeadPose(frame, head_pose_data, x:int, y:int, color, scale):
    # Conversion to radians
    yaw = head_pose_data[0] * np.pi / 180.0
    pitch = head_pose_data[1] * np.pi / 180.0
    # Calculate
    x2 = math.tan(yaw) * scale * 100
    y2 = math.tan(pitch) * scale * 100
    # Draw
    cv2.arrowedLine(frame, (x, y), (x + int(x2), y + int(y2)), color, thickness=4)

def GetLength(pos1, pos2):
    return math.sqrt((abs(pos2[0] - pos1[0]) * abs(pos2[0] - pos1[0])) + (abs(pos2[1] - pos1[1]) * abs(pos2[1] - pos1[1])))

def GetDistanceFromLandmark(eye1, eye2, face_rotation, age_gender_detection, frame_width, frame_hight, angle_of_camera):
    # Get pixel distance of PD (Pupillary distance) 
    length = GetLength(eye1, eye2)
    # Adjust camera angle
    angle_camera = (angle_of_camera / 2)
    # Yaw adjustment and conversion to radians
    yaw = (face_rotation[0] - (((((eye1[0] + eye2[0]) / 2) - (frame_width / 2)) / (frame_width / 2)) * angle_camera)) * np.pi / 180.0
    # Adjust pixcel distance of PD
    length = length / math.cos(yaw)
    # Pupillary distance estimated from gender
    if age_gender_detection[1] == 'male':
        pixel_per_millimeter = 64 / length
    else:
        pixel_per_millimeter = 62 / length
    # Calculate distance
    distance = (pixel_per_millimeter * frame_width) / (2 * math.tan(angle_camera  * np.pi / 180.0))
    # Estimates the angle between the camera and the object
    angle_object = ((math.atan((((eye1[0] + eye2[0]) / 2) - (frame_width / 2)) * pixel_per_millimeter / distance), math.atan((((eye1[1] + eye2[1]) / 2) - (frame_hight / 2)) * pixel_per_millimeter / distance)) )
    # Correct distance
    distance = distance / math.cos(angle_object[0])
    distance = distance / math.cos(angle_object[1])
    return distance * DISTANCE_MAGNIFICATION, angle_object

def GetPerspective(distance, radian_angle_cam_to_face, radian_angle_obj_to_target):
    delta_x = math.sin(radian_angle_cam_to_face[0]) * distance
    delta_y = math.sin(radian_angle_cam_to_face[1]) * distance
    if radian_angle_cam_to_face[0] != 0 and radian_angle_cam_to_face[1] != 0:
        delta_z = delta_x / math.tan(radian_angle_cam_to_face[0])
    elif radian_angle_cam_to_face[0] == 0:
        delta_z = delta_y
    else:
        delta_z = delta_x     
    cam_to_point_x = delta_z * math.tan(radian_angle_obj_to_target[0] - radian_angle_cam_to_face[0]) + delta_x
    cam_to_point_y = delta_z * math.tan(radian_angle_obj_to_target[1] - radian_angle_cam_to_face[1]) + delta_y
    r = GetLength([0.0, 0.0], [cam_to_point_x, cam_to_point_y])
    return (cam_to_point_x, cam_to_point_y, r)

def GetCosineSimilarity(vec1, vec2):
    a = np.sum(vec1 * vec2)
    b = math.sqrt(np.sum(vec1 * vec1))
    c = math.sqrt(np.sum(vec2 * vec2))
    return a / (b * c)

def GetPersonCosineSimilarity(vec1, vec2):
    if vec1 == -1 or vec2 == -1:
        return 0.0
    vec1 = vec1['reid_embedding'][:]
    vec2 = vec2['reid_embedding'][:]
    return GetCosineSimilarity(vec1, vec2)

# Check if it is in the rectangle(rectangle1 is outside)
def CheckInsideRectangle(x_min1, y_min1, x_max1, y_max1, x_min2, y_min2, x_max2, y_max2):
    if x_min1 < x_min2 and y_min1 < y_min2 and x_max1 > x_max2 and y_max1 > y_max2:
        return True
    else:
        return False

def CheckContactRectangle(x_min1, y_min1, x_max1, y_max1, x_min2, y_min2, x_max2, y_max2):
    if (max(x_min1, x_min2) < min(x_max1, x_max2)) and (max(y_max1, y_max2) > min(y_min1, y_min2)):
        return True
    else:
        return False

def GetIndexFromObjectGlobalID(global_id, object_list):
    i = 0
    for obj in object_list:
        if obj.global_id == global_id:
            return i
        i += 1    

def GetIOU(x_min1, y_min1, x_max1, y_max1, x_min2, y_min2, x_max2, y_max2):
    x_min = max(x_min1, x_min2)
    x_max = min(x_max1, x_max2)
    y_min = max(y_min1, y_min2)
    y_max = min(y_max1, y_max2)
    if (x_min < x_max and y_min > y_max):
        x = x_max - x_min
        y = y_max - y_min
        x1 = x_max1 - x_min1
        y1 = y_max1 - y_min1
        x2 = x_max2 - x_min2
        y2 = y_max2 - y_min2
        IOU = (x * y) / ((x1 * y1) + (x2 * y2) - (x * y))
        return IOU
    else:
        return 0.0

def GetChildObject(body_class, temporary_face_list, now_time):
    result = []
    distance = []
    if len(temporary_face_list) != 0:
        for i in range(len(temporary_face_list)):
            if CheckContactRectangle(body_class.x_min[0], body_class.y_min[0], body_class.x_max[0], body_class.y_max[0], temporary_face_list[i][0], temporary_face_list[i][1], temporary_face_list[i][2], temporary_face_list[i][3]) == True and body_class.last_time == now_time:
                result.append(i)
                distance.append(GetLength(((body_class.x_min[0] + body_class.x_max[0]) / 2, body_class.y_min[0] + ((body_class.y_max[0] - body_class.y_min[0]) / 4)), ((temporary_face_list[i][0] + temporary_face_list[i][2]) / 2, (temporary_face_list[i][1] + temporary_face_list[i][3]) / 2)))
        if len(result) != 0:
            distance = np.array(distance)
            min_distance_index = np.argmin(distance) 
            return result[min_distance_index]
        else:
            result = -1
    else:    
        result = -1
    return result

counted_number = 0
def PushDatabase(body_class_object, client):
    global counted_number
    counted_number += 1
    interested = body_class_object.interest / body_class_object.number_of_frame
    age = body_class_object.age
    gender = body_class_object.gender
    if age == None:
        age = -1
    if len(gender) == 0:
        gender = -1
    else:
        gender_average = np.average(np.array(gender))
        if gender_average > 0.5:
            gender = 0
        else:
            gender = 1
    start_time = body_class_object.first_time
    end_time = body_class_object.last_time
    # Save as csv file
    if save_mode == 'CSV':
        while True:
            try:
                if save_way_csv == 'Identical file':
                    with open('./csv/MICS_DATA.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([str(counted_number), str(interested * 100), str(int(age)), str(int(gender)), start_time.strftime('%Y%m%d%H%M%S'), end_time.strftime('%Y%m%d%H%M%S')])
                        PrintConsleWindow('[Info] Push person object No.' + str(counted_number) + ' to csv')   
                        break
                elif save_way_csv == 'Per date':
                    with open('./csv/MICS_' + SYSTEM_START_TIME.strftime('%Y%m%d') + '.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([str(counted_number), str(interested * 100), str(int(age)), str(int(gender)), start_time.strftime('%Y%m%d%H%M%S'), end_time.strftime('%Y%m%d%H%M%S')])
                        PrintConsleWindow('[Info] Push person object No.' + str(counted_number) + ' to csv')   
                        break
                else:
                    with open('./csv/MICS_' + SYSTEM_START_TIME.strftime('%Y%m%d%H%M%S') + '.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([str(counted_number), str(interested * 100), str(int(age)), str(int(gender)), start_time.strftime('%Y%m%d%H%M%S'), end_time.strftime('%Y%m%d%H%M%S')])
                        PrintConsleWindow('[Info] Push person object No.' + str(counted_number) + ' to csv')   
                        break
            except PermissionError:
                PrintConsleWindow("[PermissionError] Cannot write to CSV file. Please close the CSV file(./csv/MICS_" + SYSTEM_START_TIME.strftime('%Y%m%d%H%M%S') + ".csv). Processing will be temporarily suspended until the file is closed.")

    elif save_mode == 'SERVER':
        client.PushDataList(int(interested * 100), int(age), int(gender), start_time.strftime('%Y%m%d%H%M%S'), end_time.strftime('%Y%m%d%H%M%S'))
        PrintConsleWindow('[Info] Push person object No.' + str(counted_number) + ' to waiting list for transmission')   
        pass


def IsInterested(perspective):
    if perspective[0] / 10 < (size_of_interest_check_area / 2) + interest_check_area_offset and perspective[0] / 10 > (-size_of_interest_check_area / 2) + interest_check_area_offset:
        return 1.0
    else:
        return 0

def ConvertImageOpenCVToDearPyGUI(image):
    data = np.flip(image, 2)
    data = data.ravel()
    data = np.asfarray(data, dtype='f')
    return np.true_divide(data, 255.0)

def PrintConsleWindow(text):
    print(text)
    now_text = dpg.get_value('console_text')
    if now_text.count('\n') > 200:
       now_text = now_text[now_text.find('\n', 0) + 1:]
    dpg.set_value('console_text', now_text + '\n' + text)
    dpg.render_dearpygui_frame()
    try: 
        #print(dpg.get_y_scroll('console_window'))
        #print(dpg.get_y_scroll_max('console_window'))
        if dpg.get_y_scroll_max('console_window') - 30.0 <= dpg.get_y_scroll('console_window') or (dpg.get_y_scroll_max('console_window') >= 1.0 and dpg.get_y_scroll_max('console_window') <= 20.0):
            dpg.set_y_scroll('console_window', dpg.get_y_scroll_max('console_window') + 13.0)
    except SystemError:
        pass

def SaveLayout():
    PrintConsleWindow('[Info] Save layout setting to "'+ LAYOUT_SETTING_FILE_PATH + '"')
    dpg.save_init_file(LAYOUT_SETTING_FILE_PATH)

# Class
global_id = 0
class Object:
    def __init__(self, input_id, x_min, y_min, x_max, y_max, first_time, last_time):
        self.obj_id = input_id
        self.x_min = [int(x_min)]
        self.x_max = [int(x_max)]
        self.y_min = [int(y_min)]
        self.y_max = [int(y_max)]
        self.x_delta = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.y_delta = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.time_delta = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        self.first_time = first_time
        self.last_time = last_time
        self.estimated_x_min = int(x_min)
        self.estimated_x_max = int(x_max)
        self.estimated_y_min = int(y_min)
        self.estimated_y_max = int(y_max)
        self.number_of_frame = 1
        global global_id
        self.global_id = global_id
        self.check_update_flag = False
        self.update_flag = False
        global_id += 1
    
    def Update(self, input_id, x_min, y_min, x_max, y_max, last_time):
        self.obj_id = input_id
        self.x_min.insert(0, int(x_min))
        self.x_max.insert(0, int(x_max))
        self.y_min.insert(0, int(y_min))
        self.y_max.insert(0, int(y_max))
        time_delta = last_time - self.last_time
        self.time_delta.insert(0, (max(0.01,time_delta.microseconds) / 1000 + time_delta.seconds))
        self.x_delta.insert(0, (((self.x_max[0] + self.x_min[0]) / 2) - ((self.x_max[1] + self.x_min[1]) / 2)) * (1 / self.time_delta[0]))
        self.y_delta.insert(0, (((self.y_max[0] + self.y_min[0]) / 2) - ((self.y_max[1] + self.y_min[1]) / 2)) * (1 / self.time_delta[0]))
        if len(self.x_min) > 10:
            self.x_min.pop(10)
            self.x_max.pop(10)
            self.y_min.pop(10)
            self.y_max.pop(10)
            self.x_delta.pop(10)
            self.y_delta.pop(10)
            self.time_delta.pop(10)
        self.last_time = last_time
        self.estimated_x_min = int(x_min) + self.x_delta[1] * self.time_delta[0]
        self.estimated_x_max = int(x_max) + self.x_delta[1] * self.time_delta[0]
        self.estimated_y_min = int(y_min) + self.y_delta[1] * self.time_delta[0]
        self.estimated_y_max = int(y_max) + self.y_delta[1] * self.time_delta[0]
        self.number_of_frame += 1
        self.check_update_flag = True

    def GetIOU(self, x_min, y_min, x_max, y_max, now_time):
        time_delta = now_time - self.last_time
        time_delta = (max(0.01,time_delta.microseconds) / 1000 + time_delta.seconds)
        estimated_x_min = int(x_min) + self.x_delta[0] * time_delta
        estimated_x_max = int(x_max) + self.x_delta[0] * time_delta
        estimated_y_min = int(y_min) + self.y_delta[0] * time_delta
        estimated_y_max = int(y_max) + self.y_delta[0] * time_delta
        return GetIOU(x_min, y_min, x_max, y_max, estimated_x_min, estimated_x_max, estimated_y_min, estimated_y_max)

    def CheckUpdate(self):
        if self.check_update_flag == True:
            self.update_flag = True
        else:
            self.update_flag = False
        self.check_update_flag = False
            
class Body(Object):
    def __init__(self, input_id, x_min, y_min, x_max, y_max, first_time):
        super().__init__(input_id, x_min, y_min, x_max, y_max, first_time, first_time)
        self.age = None
        self.gender = []
        self.perspective = None
        self.interest = 0
        PrintConsleWindow('[Info] Create body object [global id =' + str(self.global_id) + ']')

    def Update(self, input_id, x_min, y_min, x_max, y_max, last_time):
        super().Update(input_id, x_min, y_min, x_max, y_max, last_time)

    def UpdateFaceData(self, age, gender, perspective):
        self.age = age
        if gender == 'male':
            self.gender.insert(0, 1.0)
        else:
            self.gender.insert(0, 0.0)
        if len(self.gender) > 20:
            self.gender.pop(20)
        self.perspective = perspective
        self.interest += IsInterested(perspective)

    def __del__(self):
        PrintConsleWindow('[Info] Delete body object [global id =' + str(self.global_id) + ']')

# WebSocketClient class
class WebSocketClient():
    def __init__(self, address):
        self.host = address              #"ws://fast-fjord-64260.herokuapp.com"
        self.data_list = []
        websocket.enableTrace(True)     # print log option
        self.isConnected = False
        #Setting of WebSocket
        PrintConsleWindow("[Info] Launch as SERVER MODE")
        self.Connect()
        self.last_time = datetime.datetime.now()
        if self.isConnected == True:
            self.ws.ping()

    def Connect(self):
        if self.isConnected == False:
            PrintConsleWindow('[Info] Connect to the server(address="' + self.host + '")')
            for i in range(5):
                try:
                    self.ws = websocket.WebSocket()
                    self.ws.connect(self.host)
                    self.ws.settimeout(60)
                    self.isConnected = True
                    PrintConsleWindow("[Info] Successfully connected to server")   
                    break    
                except:
                    self.isConnected = False
                    PrintConsleWindow("[Error] Could not connect to server. Try to reconnect. Number of connection attempts = " + str(i + 1))
                    sleep(1)
                if i == 5:
                    PrintConsleWindow("[Error] Tried " + str(i) + " times but could not connect to the server. Start software without recording.")

    def Disonnect(self):
        if self.isConnected == True:
             PrintConsleWindow("[Info] Disonnected")   
             self.ws.close()

    def CheckTimeout(self):
        if self.isConnected == True:
            time_delta = datetime.datetime.now() - self.last_time
            if time_delta > datetime.timedelta(seconds=self.ws.timeout - 10):
                self.ws.ping()          # send ping
                self.last_time = datetime.datetime.now()
                PrintConsleWindow("[Info] Send ping to server")   

    def PushDataList(self, interested, age, gender, start_time, end_time):
        self.data_list.append((interested, age, gender, start_time, end_time))

    def PushSequentially(self):
        if len(self.data_list) != 0 and datetime.datetime.now() - self.last_time > datetime.timedelta(seconds=3):
            data_buffer = self.data_list.pop(0)
            self.RunAsThread(data_buffer[0], data_buffer[1], data_buffer[2], data_buffer[3], data_buffer[4])     
            self.last_time = datetime.datetime.now()

    def RunAsThread(self, interested, age, gender, start_time, end_time):
        thread.start_new_thread(self.Run, (interested, age, gender, start_time, end_time))

    # Send messge to server
    def Run(self, interested, age, gender, start_time, end_time):
        #self.Connect()
        send_msg = '{"interested":' + str(interested) + ',"age":' + str(age) + ',"gender":' + str(gender) + ',"start_time":"' + start_time + '","end_time":"' + end_time + '"}'
        # send data without id
        if self.isConnected == True:
            for i in range(2):
                try:
                    self.ws.send(send_msg)
                    PrintConsleWindow('[Info] Send message [message=' + send_msg + ']')
                    break
                except:
                    PrintConsleWindow('[Error] Could not send message')
        else:
            PrintConsleWindow('[Error] Could not send message')

# Settings
class Settings():
    def __init__(self, path):
        self.path = path
        pass

    def SetValues(self, input_device_name, input_save_mode, input_server_address, input_angle_of_view, input_cam_id, input_cam_x, input_cam_y, input_cam_fps, input_size_of_interest_check_area, input_interest_check_area_offset, input_save_way_csv, input_auto_start, input_show_additional_info):
        global device_name
        global save_mode
        global server_address
        global angle_of_view
        global cam_id
        global cam_x
        global cam_y
        global cam_fps
        global size_of_interest_check_area
        global interest_check_area_offset
        global save_way_csv
        global auto_start
        global show_additional_info
        device_name                 = input_device_name
        save_mode                   = input_save_mode
        server_address              = input_server_address
        angle_of_view               = input_angle_of_view
        cam_id                      = input_cam_id
        cam_x                       = input_cam_x
        cam_y                       = input_cam_y
        cam_fps                     = input_cam_fps
        size_of_interest_check_area = input_size_of_interest_check_area
        interest_check_area_offset  = input_interest_check_area_offset
        save_way_csv                = input_save_way_csv
        auto_start                  = input_auto_start
        show_additional_info        = input_show_additional_info
        
    def SetValuesFromDearPyGUI(self):
        self.SetValues(dpg.get_value('device_name'                ), 
                       dpg.get_value('save_mode'                  ),
                       dpg.get_value('server_address'             ),
                       dpg.get_value('angle_of_view'              ),
                       dpg.get_value('cam_id'                     ),
                       dpg.get_value('cam_x'                      ),
                       dpg.get_value('cam_y'                      ),
                       dpg.get_value('cam_fps'                    ),
                       dpg.get_value('size_of_interest_check_area'),
                       dpg.get_value('interest_check_area_offset' ),
                       dpg.get_value('save_way_csv'               ),
                       dpg.get_value('auto_start'                 ),
                       dpg.get_value('show_additional_info'       ))

    def Load(self):
        if not os.path.exists('resources'):
            os.makedirs('resources')
        try:
            with open( self.path, 'r') as f:
                load_value = json.load(f)
                global device_name
                global save_mode
                global server_address
                global angle_of_view
                global cam_id
                global cam_x
                global cam_y
                global cam_fps
                global size_of_interest_check_area
                global interest_check_area_offset
                global save_way_csv
                global auto_start
                global show_additional_info
                device_name                 = load_value['device_name'                ]
                save_mode                   = load_value['save_mode'                  ]
                server_address              = load_value['server_address'             ]
                angle_of_view               = load_value['angle_of_view'              ]
                cam_id                      = load_value['cam_id'                     ]
                cam_x                       = load_value['cam_x'                      ]
                cam_y                       = load_value['cam_y'                      ]
                cam_fps                     = load_value['cam_fps'                    ]
                size_of_interest_check_area = load_value['size_of_interest_check_area']
                interest_check_area_offset  = load_value['interest_check_area_offset' ]
                save_way_csv                = load_value['save_way_csv'               ]
                auto_start                  = load_value['auto_start'                 ]
                show_additional_info        = load_value['show_additional_info'       ]
        except:
            self.Save()
        pass

    def Save(self):
        global device_name
        global save_mode
        global server_address
        global angle_of_view
        global cam_id
        global cam_x
        global cam_y
        global cam_fps
        global size_of_interest_check_area
        global interest_check_area_offset
        global save_way_csv
        global auto_start
        global show_additional_info
        if not os.path.exists('resources'):
            os.makedirs('resources')
        save_value = {'device_name'                 : device_name                ,
                      'save_mode'                   : save_mode                  ,
                      'server_address'              : server_address             ,
                      'angle_of_view'               : angle_of_view              ,
                      'cam_id'                      : cam_id                     ,
                      'cam_x'                       : cam_x                      ,
                      'cam_y'                       : cam_y                      ,
                      'cam_fps'                     : cam_fps                    ,
                      'size_of_interest_check_area' : size_of_interest_check_area,
                      'interest_check_area_offset'  : interest_check_area_offset ,
                      'save_way_csv'                : save_way_csv               ,
                      'auto_start'                  : auto_start                 ,
                      'show_additional_info'        : show_additional_info       }
        with open(self.path, 'w') as f:
            json.dump(save_value, f)
        pass
    

# Main
def Main():

    # Load settings
    settings = Settings(SETTING_FILE_PATH)
    settings.Load()

    # Translation
    now_locale, _ = locale.getdefaultlocale()
    _ = gettext.translation(domain='messages',
                            localedir = 'locale',
                            languages=[now_locale], 
                            fallback=True).gettext

    # Gloval var
    global restart_flag
    global counted_number
    global global_id
    global auto_start
    global is_running

    # Setup DearPyGUI
    dpg.create_context()
    dpg.create_viewport(title=('MICS Camera System version ' + VERSION), width=1136, height=640)
    dpg.setup_dearpygui()

    # Setup window
    dpg.configure_app(init_file=LAYOUT_SETTING_FILE_PATH)

    with dpg.texture_registry(show=False):
        dpg.add_raw_texture(480, 270, ConvertImageOpenCVToDearPyGUI(np.zeros((480, 270, 3))), tag='video_frame', format=dpg.mvFormat_Float_rgb, use_internal_label=False)

    with dpg.font_registry():
        with dpg.font(file="./resources/Mplus1-Medium.ttf", size = 18) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        dpg.bind_font(default_font)

    with dpg.window(label=(_('Dashboard')), tag='dashboard',  no_collapse=False, no_close=True, horizontal_scrollbar=True):
        dpg.add_text(_('Welcome to MICS Camera System version %s') % VERSION)
        

        # Debug option. Do not enable when release.
        #dpg.add_button(label="Save Window Layout", tag="save_layout", callback=SaveLayout)

    with dpg.window(label=_('Advanced settings'), tag='advanced_settings',  no_collapse=False, no_close=True, horizontal_scrollbar=True):
        dpg.add_text(_('Changing these settings may cause the software to stop working properly.'))
        dpg.add_text(_('Please change the settings only if you understand them.'))
        dpg.add_separator()
        dpg.add_text(_('[Advanced settings]'))
        dpg.add_text(_('Inference Processor'))
        dpg.add_radio_button(tag='device_name', items=['CPU', 'GPU', 'MYRAID'], default_value=device_name)
        dpg.add_text(_('Where to save data'))
        dpg.add_radio_button(tag='save_mode', items=['CSV', 'SERVER'], default_value=save_mode)
        dpg.add_text(_('Save method<Only CSV mode>'))
        dpg.add_combo(tag='save_way_csv', items=['Per software launch', 'Per date', 'Identical file'], default_value=save_way_csv)
        dpg.add_text(_('Server address<Only SERVER mode>'))
        dpg.add_input_text(tag='server_address', default_value=server_address)
        dpg.add_text('')
        dpg.add_button(label=_("Save and restart"), tag="save_and_restart2", callback=RestartCameraSystem)
        dpg.add_separator()
    
    with dpg.window(label=_('General settings'), tag='general_settings',  no_collapse=False, no_close=True, horizontal_scrollbar=True):
        dpg.add_text(_('[Execution]'))
        dpg.add_checkbox(label=_("Enable interest measurement"), tag="is_running", default_value=is_running)
        dpg.add_separator()
        dpg.add_text(_('[General settings]'))
        dpg.add_checkbox(label=_("Auto start camera system when software launch"), tag="auto_start", default_value=auto_start)
        dpg.add_checkbox(label=_("Show additional information in the camera window"), tag="show_additional_info", default_value=show_additional_info)
        dpg.add_text('')
        dpg.add_text(_('Camera id'))        
        dpg.add_input_int(min_value=0, max_value=100, min_clamped=True, max_clamped=True,default_value=cam_id,tag="cam_id")
        dpg.add_text(_('Camera vertical resolution'))
        dpg.add_input_int(label="(px)",min_value=320,max_value=7680, min_clamped=True, max_clamped=True,default_value=cam_x,tag="cam_x")
        dpg.add_text(_('Camera horizontal resolution'))
        dpg.add_input_int(label="(px)",min_value=320,max_value=4320, min_clamped=True, max_clamped=True,default_value=cam_y,tag="cam_y")
        dpg.add_text(_('Camera frame rate'))
        dpg.add_combo(label="(fps)",tag='cam_fps', items=[5, 10, 15, 20, 30, 60], default_value=cam_fps)
        dpg.add_text(_('Camera angle of view'))
        dpg.add_input_int(label="(degrees)",min_value=1,max_value=179, min_clamped=True, max_clamped=True,default_value=angle_of_view,tag="angle_of_view")
        dpg.add_text(_('Width of region to detect interest'))
        dpg.add_input_int(label="(cm)",min_value=0, min_clamped=True,default_value=size_of_interest_check_area,tag="size_of_interest_check_area")
        dpg.add_text(_('Location of the center of the region of interest detection (relative to the camera)'))
        dpg.add_input_int(label="(cm)",default_value=interest_check_area_offset,tag="interest_check_area_offset")
        dpg.add_text('')
        dpg.add_button(label=_("Save and restart"), tag="save_and_restart1", callback=RestartCameraSystem)
        dpg.add_separator()
    
    with dpg.window(label=_('Camera'), tag='video_window', no_collapse=False, no_close=True, no_scrollbar=True):
        dpg.add_image('video_frame')

    with dpg.window(label=_('Software Information'), tag='soft_info_window',  no_collapse=False, no_close=True, horizontal_scrollbar=True):
        dpg.add_text(_('[Software version]') + '\nMICS Camera System version ' + VERSION + ' for ' + PLATFORM)
        dpg.add_text(_('[Third Party Licenses]'))
        try:
            f = open('./resources/third_party_licenses.txt', 'r', encoding='UTF-8')
            licenses_text = f.read()
            f.close()
            dpg.add_text(licenses_text)
        except NameError:
            print("[Error] Could not open licenses file")
        except FileNotFoundError:
            print("[Error] Could not open licenses file")

    with dpg.window(label=_('Console'), tag='console_window',  no_collapse=False, no_close=True, horizontal_scrollbar=True):
        dpg.add_text('[Info] Launch virtual console window', tag='console_text')


    dpg.configure_app(docking=True, docking_space=True)
    dpg.show_viewport()
    

    # Setup OpenVINO
    # Generate Inference Engine Core object
    ie = IECore()
    
    # Setup person detection
    input_name_PD, input_shape_PD, _, _, exec_net_PD = SetupModel(ie, device_name, './models/person-detection-retail-0013/FP16/person-detection-retail-0013')

    # Setup person re-identification
    input_name_PR, input_shape_PR, _, _, exec_net_PR = SetupModel(ie, device_name, './models/person-reidentification-retail-0288/FP16/person-reidentification-retail-0288')

    # Setup face detection
    input_name_FD, input_shape_FD, out_name_FD, _, exec_net_FD = SetupModel(ie, device_name, './models/face-detection-adas-0001/FP16/face-detection-adas-0001')

    # Setup age gender detectuon
    input_name_AGD, input_shape_AGD, _, _, exec_net_AGD = SetupModel(ie, device_name, './models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013')
    
    # Setup face landmark(5) detection
    input_name_LD5, input_shape_LD5, out_name_LD5, _, exec_net_LD5 = SetupModel(ie, device_name, './models/landmarks-regression-retail-0009/FP16/landmarks-regression-retail-0009')

    # Setup head pose estimation
    input_name_HPE, input_shape_HPE, _, _, exec_net_HPE = SetupModel(ie, device_name, './models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001')

    # Create body class list
    body_list = []

    # Launch message
    PrintConsleWindow('[Info] Launch mics-dev version ' + VERSION)


    # Setup camera
    capture = SetupCamera(cam_id, cam_x, cam_y, cam_fps)

    # Make csv file (CSV mode)
    if save_mode == 'CSV': 
        SetupCSV()

    # Accsess to server (SERVER mode)
    if save_mode == 'SERVER':
        client = WebSocketClient(server_address)

    # Set runnning flag
    is_running = auto_start
        
    # Loop
    while dpg.is_dearpygui_running():
        # Restart
        if restart_flag == True:
            PrintConsleWindow('\n[Info] Reboot the system')
            # Close capture and client
            capture.release()
            if save_mode == 'SERVER':
                client.Disonnect()
            # Change settings value
            settings.SetValuesFromDearPyGUI()
            # Setup again
            capture = SetupCamera(cam_id, cam_x, cam_y, cam_fps)
            if save_mode == 'CSV': 
                SetupCSV()
            if save_mode == 'SERVER':
                client = WebSocketClient(server_address)
            input_name_PD, input_shape_PD, _, _, exec_net_PD = SetupModel(ie, device_name, './models/person-detection-retail-0013/FP16/person-detection-retail-0013')
            input_name_PR, input_shape_PR, _, _, exec_net_PR = SetupModel(ie, device_name, './models/person-reidentification-retail-0288/FP16/person-reidentification-retail-0288')
            input_name_FD, input_shape_FD, out_name_FD, _, exec_net_FD = SetupModel(ie, device_name, './models/face-detection-adas-0001/FP16/face-detection-adas-0001')
            input_name_AGD, input_shape_AGD, _, _, exec_net_AGD = SetupModel(ie, device_name, './models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013')
            input_name_LD5, input_shape_LD5, out_name_LD5, _, exec_net_LD5 = SetupModel(ie, device_name, './models/landmarks-regression-retail-0009/FP16/landmarks-regression-retail-0009')
            input_name_HPE, input_shape_HPE, _, _, exec_net_HPE = SetupModel(ie, device_name, './models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001')
            is_running = auto_start
            restart_flag = False
            counted_number = 0
            global_id = 0
            settings.Save()
            pass

        # Get a frame
        ret, frame = capture.read()
        if ret == False:
            break

        # Get now time
        now_time = datetime.datetime.now()

        # Check runnning flag
        is_running = dpg.get_value('is_running')
        
        # Check server
        if save_mode == 'SERVER':
            client.CheckTimeout()
            client.PushSequentially()
        else:
            client = None

        if is_running == True:
            # Get person detction data
            temporary_body_list = []
            result_of_person_detection = GetDetectionData(frame, exec_net_PD, input_name_PD, input_shape_PD)
            for person_object in result_of_person_detection[out_name_FD][0][0]:
                if person_object[2] > THRESHOLD_PERSON_DETECTION:
                    px_min, py_min, px_max, py_max = GetXYMinMaxFromDetection(person_object,frame)
                    #print("get person!")

                    person = frame[py_min:py_max,px_min:px_max]

                    # Get person id and check
                    result_of_person_id = GetDetectionData(person, exec_net_PR, input_name_PR, input_shape_PR)

                    # Update object
               
                    temporary_body_list.append([result_of_person_id, px_min, py_min, px_max, py_max])
                    # Show in window
                    cv2.rectangle(frame, (px_min, py_min), (px_max, py_max), (255, 0, 255), 2)

            # Check body instance
            if len(body_list) != 0:
                for j in range(len(body_list)):
                    # Chack update body instance
                    if len(temporary_body_list) != 0:
                        compare_list = []
                        cos_sim_list = []
                        iou_list = []
                        for i in range(len(temporary_body_list)):
                            cos_sim = GetPersonCosineSimilarity(temporary_body_list[i][0], body_list[j].obj_id)
                            iou = body_list[j].GetIOU(temporary_body_list[i][1], temporary_body_list[i][2], temporary_body_list[i][3], temporary_body_list[i][4], now_time)
                            compare_list.append([iou, cos_sim])
                            cos_sim_list.append([cos_sim])
                            iou_list.append([iou])
                        cos_sim_list = np.array(cos_sim_list)
                        iou_list = np.array(iou_list)
                        row_index = [np.argmax(iou_list), np.argmax(cos_sim_list)]
                    
                        if compare_list[row_index[0]][0] < 0.1 and compare_list[row_index[1]][1] <  THRESHOLD_PERSON_REIDENTIFICATION:
                            pass
                        else:
                            # Maximized IOU and cos_sim are same
                            if row_index[0] == row_index[1]:
                                body_list[j].Update(temporary_body_list[row_index[0]][0], temporary_body_list[row_index[0]][1], temporary_body_list[row_index[0]][2], temporary_body_list[row_index[0]][3], temporary_body_list[row_index[0]][4], now_time)
                                temporary_body_list[row_index[0]][0] = -1

                            # Use IOU
                            elif compare_list[row_index[0]][0] >= compare_list[row_index[1]][1] / 2 and now_time - body_list[j].last_time > datetime.timedelta(seconds=1):
                                body_list[j].Update(temporary_body_list[row_index[0]][0], temporary_body_list[row_index[0]][1], temporary_body_list[row_index[0]][2], temporary_body_list[row_index[0]][3], temporary_body_list[row_index[0]][4], now_time)
                                temporary_body_list[row_index[0]][0] = -1

                            # Use Cosine Similarity
                            else:
                                body_list[j].Update(temporary_body_list[row_index[1]][0], temporary_body_list[row_index[1]][1], temporary_body_list[row_index[1]][2], temporary_body_list[row_index[1]][3], temporary_body_list[row_index[1]][4], now_time)
                                temporary_body_list[row_index[1]][0] = -1
                        
                            # Info
                            color = COLORS_16[(body_list[j].global_id + 1) % 16]
                            #cv2.rectangle(frame, (int(body_list[j].estimated_x_min), int(body_list[j].estimated_y_min)), (int(body_list[j].estimated_x_max), int(body_list[j].estimated_y_max)), color, 2)                        
                            cv2.rectangle(frame, (int(body_list[j].x_min[0]), int(body_list[j].y_min[0])), (int(body_list[j].x_max[0]), int(body_list[j].y_max[0])), color, 2)                        
                            cv2.putText(frame, text='id = ' + str(body_list[j].global_id), org=(body_list[j].x_min[0], body_list[j].y_min[0] - 5), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=color, thickness=2, lineType=cv2.LINE_AA)                              

            # Create new body instance
            if len(temporary_body_list) != 0:
                for i in range(len(temporary_body_list)):
                    if temporary_body_list[i][0] != -1:
                        body_list.append(Body(temporary_body_list[i][0], temporary_body_list[i][1], temporary_body_list[i][2], temporary_body_list[i][3], temporary_body_list[i][4], now_time))  

            # CheckUpdate (experimental)     
            if len(body_list) != 0:
                for j in range(len(body_list)):
                    body_list[j].CheckUpdate()

            # Get face detection data
            temporary_face_list = []
            result_of_face_detection = GetDetectionData(frame, exec_net_FD, input_name_FD, input_shape_FD)
            for face_object in result_of_face_detection[out_name_FD][0][0]:
                if face_object[2] > THRESHOLD_FACE_DETECTION:
                    face_pos = GetXYMinMaxFromDetection(face_object,frame)
                    x_min, y_min, x_max, y_max = face_pos
                    # Error check
                    if ((x_max - x_min) * 1.8) - (y_max - y_min) < 0:
                        pass
                    else:
                        # Get face image
                        face = frame[y_min:y_max,x_min:x_max]

                        # Get age and gender from face image
                        result_of_age_gender_detection = GetAgeGenderData(face, exec_net_AGD, input_name_AGD, input_shape_AGD)

                        # Get head pose estimation
                        result_of_head_pose_estimation = GetHeadPoseEstimationData(face, exec_net_HPE, input_name_HPE,input_shape_HPE)
                
                        # Get face landmark from face image
                        result_of_face_landmaek_detection = GetFaceLandmarkDetectionData(face, exec_net_LD5, input_name_LD5, input_shape_LD5, out_name_LD5, face_pos)

                        # Get distance from face landmark and gender
                        result_of_distance_estimation, face_to_cam_angle = GetDistanceFromLandmark(result_of_face_landmaek_detection[0], result_of_face_landmaek_detection[1], result_of_head_pose_estimation, result_of_age_gender_detection, frame.shape[1], frame.shape[0], angle_of_view)

                        # Get perspective data
                        perspective = GetPerspective(result_of_distance_estimation, face_to_cam_angle, [(result_of_head_pose_estimation[0] * np.pi / 180.0), (result_of_head_pose_estimation[1] * np.pi / 180.0)])

                        # Update object
                        temporary_face_list.append([x_min, y_min, x_max, y_max, result_of_age_gender_detection[0], result_of_age_gender_detection[1], perspective])

                        # Show data in frame
                        if show_additional_info == True:
                            # Face Detection
                            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                            # Age Gender Detection
                            cv2.putText(frame, text='[gender, age]', org=(x_min, y_min - 25), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            age_gender = ' '+result_of_age_gender_detection[1] + ', ' + str(result_of_age_gender_detection[0])
                            cv2.putText(frame, text=age_gender, org=(x_min, y_min - 5), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            # Face Landmerk Detection
                            for i in range(len(result_of_face_landmaek_detection)):
                                cv2.circle(frame, center=(int(result_of_face_landmaek_detection[i][0]), int(result_of_face_landmaek_detection[i][1])), radius=1, color=(0, 255, 0), thickness=1)
                                cv2.putText(frame, text=str(i), org=(int(result_of_face_landmaek_detection[i][0] + 1), int(result_of_face_landmaek_detection[i][1])), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            # Distance Estimation
                            cv2.putText(frame, text='[distance]', org=(x_min, y_max + 20), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            cv2.putText(frame, text=' {:.3f}(cm)'.format(result_of_distance_estimation / 10), org=(x_min, y_max + 40), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            # Head Pose Estimation
                            cv2.putText(frame, text='[head pose]', org=(x_min, y_max + 60), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            cv2.putText(frame, text=' yaw   = {:.3f}(degrees)'.format(result_of_head_pose_estimation[0]), org=(x_min, y_max + 80), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            cv2.putText(frame, text=' pitch = {:.3f}(degrees)'.format(result_of_head_pose_estimation[1]), org=(x_min, y_max + 100), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            cv2.putText(frame, text=' roll  = {:.3f}(degrees)'.format(result_of_head_pose_estimation[2]), org=(x_min, y_max + 120), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            DrawHeadPose(frame, result_of_head_pose_estimation, int((x_max + x_min) / 2), int((y_max + y_min) / 2), color=(0,255,0), scale=2)
                            # Perspective
                            cv2.putText(frame, text='[perspective]', org=(x_min, y_max + 140), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            cv2.putText(frame, text=' dx = {:.3f}(cm)'.format(perspective[0] / 10), org=(x_min, y_max + 160), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            cv2.putText(frame, text=' dy = {:.3f}(cm)'.format(-perspective[1] / 10), org=(x_min, y_max + 180), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                            cv2.putText(frame, text=' dr = {:.3f}(cm)'.format(perspective[2] / 10), org=(x_min, y_max + 200), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                        

            # Check face instance
            if len(body_list) != 0:
                for i in range(len(body_list)):
                    check_face = GetChildObject(body_list[i], temporary_face_list, now_time)
                    if check_face != -1:
                        body_list[i].UpdateFaceData(temporary_face_list[check_face][4], temporary_face_list[check_face][5], temporary_face_list[check_face][6])
                        color = COLORS_16[(body_list[i].global_id + 1) % 16]
                        cv2.rectangle(frame, (int(temporary_face_list[check_face][0]), int(temporary_face_list[check_face][1])), (int(temporary_face_list[check_face][2]), int(temporary_face_list[check_face][3])), color, 2)
                        # Age Gender Detection
                        cv2.putText(frame, text='[gender, age]', org=(temporary_face_list[check_face][0], temporary_face_list[check_face][1] - 25), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=color, thickness=2, lineType=cv2.LINE_AA)
                        age_gender = ' '+ temporary_face_list[check_face][5] + ', ' + str(temporary_face_list[check_face][4])
                        cv2.putText(frame, text=age_gender, org=(temporary_face_list[check_face][0], temporary_face_list[check_face][1] - 5), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=color, thickness=2, lineType=cv2.LINE_AA)
                        # IsInterest
                        cv2.putText(frame, text='[isInterest]', org=(temporary_face_list[check_face][0], temporary_face_list[check_face][1] - 65), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=color, thickness=2, lineType=cv2.LINE_AA)
                        if IsInterested(temporary_face_list[check_face][6]) == 1.0:
                            interest = 'yes'
                        else:
                            interest = 'no'
                        cv2.putText(frame, text=interest, org=(temporary_face_list[check_face][0], temporary_face_list[check_face][1] - 45), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=color, thickness=2, lineType=cv2.LINE_AA)

            # Delete error instance
            if len(body_list) != 0:
                di = 0
                for i in range(len(body_list)):
                    if body_list[i - di].last_time - body_list[i - di].first_time < datetime.timedelta(seconds=5) and now_time - body_list[i - di].last_time > datetime.timedelta(seconds=3):
                        del body_list[i - di]
                        di += 1    
       
            # Delete lost instance
            if len(body_list) != 0:
                di = 0
                for i in range(len(body_list)):
                    if body_list[i - di].last_time - body_list[i - di].first_time >= datetime.timedelta(seconds=5) and now_time - body_list[i - di].last_time > datetime.timedelta(seconds=10):
                        PushDatabase(body_list[i - di], client)
                        del body_list[i - di]
                        di += 1     

        # Show FPS
        frame_rate = DrawFPS(frame, fps_time, 10, 10)

        # Resize frame and show it in window
        video_frame_height = max(dpg.get_item_height('video_window') - 35, 16)
        video_frame_width = max(dpg.get_item_width('video_window') - 20, 9)
        if video_frame_width < video_frame_height * (cam_x / cam_y):
            video_frame_height = video_frame_width * (cam_y / cam_x)
        else:
            video_frame_width = video_frame_height * (cam_x / cam_y)
        buffer_frame = ConvertImageOpenCVToDearPyGUI(cv2.resize(frame, (int(video_frame_width), int(video_frame_height))))
        dpg.delete_item('video_window', children_only=True)
        dpg.delete_item('video_frame')
        with dpg.texture_registry(show=False):      
            dpg.add_raw_texture(int(video_frame_width), int(video_frame_height), buffer_frame, tag='video_frame', format=dpg.mvFormat_Float_rgb)
            dpg.add_image('video_frame', parent='video_window')
        dpg.configure_item('video_frame', width=int(video_frame_width), height=int(video_frame_height))
        dpg.set_value('video_frame', buffer_frame)
        dpg.render_dearpygui_frame()

        #[Developing option] save layout
        if dpg.is_key_pressed(dpg.mvKey_L) == True:
            SaveLayout() 

    # Exit process
    if save_mode == 'SERVER':
        client.Disonnect()
    capture.release()
    dpg.destroy_context()


if __name__ == '__main__':
   	Main()