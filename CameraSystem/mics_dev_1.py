# mics_dev_1
# 2022 kasys1422
# The core app of MICS(Measuring Interest with a Camera System)
VERSION = '0.0.6'

# Import
import math
import os
import numpy as np
import cv2
import time
import datetime
import csv
from openvino.inference_engine import IECore

# Constant

#DEVICE_NAME = 'MYRIAD'                         # Use MYRIAD
DEVICE_NAME = 'CPU'                             # Use CPU
#SAVE_MODE = 'SERVER'
SAVE_MODE = 'CSV'
SYSTEM_START_TIME = datetime.datetime.now()
THRESHOLD_PERSON_DETECTION = 0.75
THRESHOLD_FACE_DETECTION = 0.95
ANGLE_OF_VIEW = 70                              # Angle must be within 180 degrees
CAM_ID = 0
CAM_X = 1280
CAM_Y = 720
CAM_FPS = 30
DISTANCE_MAGNIFICATION = 1.0                    #1.16
THRESHOLD_PERSON_REIDENTIFICATION = 0.60        #Threshold of Cosine Similarity
SIZE_OF_INTEREST_CHECK_AREA = 70                #(cm)                                
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


# Functions

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
    camera = cv2.VideoCapture(cam_id)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    camera.set(cv2.CAP_PROP_FPS, fps)
    return camera

def SetupModel(ie_core, device_name, model_path_without_extension):
    net  = ie_core.read_network(model=model_path_without_extension + '.xml', weights=model_path_without_extension + '.bin')
    input_name  = next(iter(net.input_info))
    input_shape = net.input_info[input_name].tensor_desc.dims
    out_name    = next(iter(net.outputs))
    out_shape   = net.outputs[out_name].shape 
    exec_net    = ie_core.load_network(network=net, device_name=device_name, num_requests=1)
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
            if CheckInsideRectangle(body_class.x_min[0], body_class.y_min[0], body_class.x_max[0], body_class.y_max[0], temporary_face_list[i][0], temporary_face_list[i][1], temporary_face_list[i][2], temporary_face_list[i][3]) == True and body_class.last_time == now_time:
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
def PushDatabase(body_class_object):
    global counted_number
    counted_number += 1
    interested = body_class_object.interest / body_class_object.number_of_frame
    age = body_class_object.age
    gender = body_class_object.gender
    if age == None:
        age = -1
    if len(gender) == 0:
        gender = 'unknown'
    else:
        gender_average = np.average(np.array(gender))
        if gender_average > 0.5:
            gender = 'male'
        else:
            gender = 'female'
    start_time = body_class_object.first_time
    end_time = body_class_object.last_time
    # Save as csv file
    if SAVE_MODE == 'CSV':
        while True:
            try:
                with open('./csv/MICS_' + SYSTEM_START_TIME.strftime('%Y%m%d%H%M%S') + '.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([str(counted_number), str(interested), str(age), gender, start_time.strftime('%Y%m%d%H%M%S'), end_time.strftime('%Y%m%d%H%M%S')])
                    break
            except PermissionError:
                print("[PermissionError] Cannot write to CSV file. Please close the CSV file(./csv/MICS_" + SYSTEM_START_TIME.strftime('%Y%m%d%H%M%S') + ".csv). Processing will be temporarily suspended until the file is closed.")

    elif SAVE_MODE == 'SERVER':
        pass
    print('pushed person object No.' + str(counted_number) + ' to databese')

def IsInterested(perspective):
    if perspective[0] / 10 < SIZE_OF_INTEREST_CHECK_AREA / 2 and perspective[0] / 10 > -SIZE_OF_INTEREST_CHECK_AREA / 2:
        return 1.0
    else:
        return 0

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
        print('create body object [global id =' + str(self.global_id) + ']')

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
        print('delete body object [global id =' + str(self.global_id) + ']')

# Main
def Main():
    # Launch message
    print('[mics-dev version ' + VERSION + ']')

    # Setup camera
    capture = SetupCamera(CAM_ID, CAM_X, CAM_Y, CAM_FPS)

    # Setup OpenVINO
    # Generate Inference Engine Core object
    ie = IECore()
    
    # Setup person detection
    input_name_PD, input_shape_PD, _, _, exec_net_PD = SetupModel(ie, DEVICE_NAME, './models/person-detection-retail-0013/FP16/person-detection-retail-0013')

    # Setup person re-identification
    input_name_PR, input_shape_PR, _, _, exec_net_PR = SetupModel(ie, DEVICE_NAME, './models/person-reidentification-retail-0288/FP16/person-reidentification-retail-0288')

    # Setup face detection
    input_name_FD, input_shape_FD, out_name_FD, _, exec_net_FD = SetupModel(ie, DEVICE_NAME, './models/face-detection-adas-0001/FP16/face-detection-adas-0001')

    # Setup age gender detectuon
    input_name_AGD, input_shape_AGD, _, _, exec_net_AGD = SetupModel(ie, DEVICE_NAME, './models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013')
    
    # Setup face landmark(5) detection
    input_name_LD5, input_shape_LD5, out_name_LD5, _, exec_net_LD5 = SetupModel(ie, DEVICE_NAME, './models/landmarks-regression-retail-0009/FP16/landmarks-regression-retail-0009')

    # Setup head pose estimation
    input_name_HPE, input_shape_HPE, _, _, exec_net_HPE = SetupModel(ie, DEVICE_NAME, './models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001')

    # Create body class list
    body_list = []

    # Make csv file (CSV mode)
    if SAVE_MODE == 'CSV': 
        if not os.path.exists('csv'):
            os.makedirs('csv')
        with open('./csv/MICS_' + SYSTEM_START_TIME.strftime('%Y%m%d%H%M%S') + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'interested', 'age', 'gender', 'start_time', 'end_time'])

    # Loop
    while(True):
        # Get a frame
        ret, frame = capture.read()
        if ret==False:
            break

        # Get now time
        now_time = datetime.datetime.now()

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
                    result_of_distance_estimation, face_to_cam_angle = GetDistanceFromLandmark(result_of_face_landmaek_detection[0], result_of_face_landmaek_detection[1], result_of_head_pose_estimation, result_of_age_gender_detection, frame.shape[1], frame.shape[0], ANGLE_OF_VIEW)

                    # Get perspective data
                    perspective = GetPerspective(result_of_distance_estimation, face_to_cam_angle, [(result_of_head_pose_estimation[0] * np.pi / 180.0), (result_of_head_pose_estimation[1] * np.pi / 180.0)])

                    # Update object
                    temporary_face_list.append([x_min, y_min, x_max, y_max, result_of_age_gender_detection[0], result_of_age_gender_detection[1], perspective])

                    # Show data in frame
                    # Face Detection
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    #DrawHeadPose(frame, result_of_head_pose_estimation, int((x_max + x_min) / 2), int((y_max + y_min) / 2), color=(0,255,0), scale=2)
                    #'''
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
                    #'''

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
                if body_list[i - di].last_time - body_list[i - di].first_time < datetime.timedelta(seconds=5) and now_time - body_list[i - di].last_time > datetime.timedelta(seconds=2):
                    del body_list[i - di]
                    di += 1    
       
        # Delete lost instance
        if len(body_list) != 0:
            di = 0
            for i in range(len(body_list)):
                if body_list[i - di].last_time - body_list[i - di].first_time >= datetime.timedelta(seconds=5) and now_time - body_list[i - di].last_time > datetime.timedelta(seconds=10):
                    PushDatabase(body_list[i - di])
                    del body_list[i - di]
                    di += 1     

        # Show FPS
        frame_rate = DrawFPS(frame, fps_time, 10, 10)

        # Show frame in window
        cv2.imshow('mics-dev-1',frame)

        # Exit (key is esc)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Exit process
    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
	Main()