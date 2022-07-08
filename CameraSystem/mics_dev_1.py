##############
# mics_dev_1 #
##############

# Import
from asyncio.windows_events import NULL
import math
import numpy as np
import cv2
import time
import datetime
from openvino.inference_engine import IECore

# Constant

#DEVICE_NAME = 'MYRIAD'               # Use MYRIAD
DEVICE_NAME = 'CPU'                   # Use CPU
THRESHOLD_PERSON_DETECTION = 0.80
THRESHOLD_FACE_DETECTION = 0.75
ANGLE_OF_VIEW = 70
CAM_ID = 0
CAM_X = 1280
CAM_Y = 720
CAM_FPS = 30
DISTANCE_MAGNIFICATION = 1.16
#PERSON_REIDENTIFICATION_MODEL = 'person-reidentification-retail-0288'
PERSON_REIDENTIFICATION_MODEL = 'person-reidentification-retail-0287'
THRESHOLD_PERSON_REIDENTIFICATION = ((0.60,     #[0][1] = Get data threshold (face)
                                      0.85,     #[0][2] = Update id threshold (face)
                                      0.40),    #[0][3] = Create object threshold (face)
                                     (0.60,     #[1][1] = Get data threshold (person)
                                      0.85,     #[1][2] = Update id threshold (person)
                                      0.60))    #[1][3] = Create object threshold (person)


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
    return math.sqrt((abs(pos2[0] - pos1[0]) * abs(pos2[0] - pos1[0]))+(abs(pos2[1] - pos1[1]) * abs(pos2[1] - pos1[1])))

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
    delta_z = delta_x / math.tan(radian_angle_cam_to_face[0])
    cam_to_point_x = delta_z * math.tan(radian_angle_obj_to_target[0] - radian_angle_cam_to_face[0]) + delta_x
    cam_to_point_y = delta_z * math.tan(radian_angle_obj_to_target[1] - radian_angle_cam_to_face[1]) + delta_y
    r = GetLength([0.0, 0.0], [cam_to_point_x, cam_to_point_y])
    return (cam_to_point_x, cam_to_point_y, r)

def GetCosineSimilarity(vec1, vec2):
    a = np.sum(vec1 * vec2)
    b = math.sqrt(np.sum(vec1 * vec1))
    c = math.sqrt(np.sum(vec2 * vec2))
    #print(str(a / (b * c)))
    return a / (b * c)

def GetPersonCosineSimilarity(vec1, vec2):
    if PERSON_REIDENTIFICATION_MODEL == 'person-reidentification-retail-0288':
        vec1 = vec1['reid_embedding'][:]
        vec2 = vec2['reid_embedding'][:]
        return GetCosineSimilarity(vec1, vec2)
    elif PERSON_REIDENTIFICATION_MODEL == 'person-reidentification-retail-0287':
        vec1 = vec1['reid_embedding'][:]
        vec2 = vec2['reid_embedding'][:]
        return GetCosineSimilarity(vec1, vec2)
    else:
        return 0

def GetFaceCosineSimilarity(vec1, vec2):
    vec1 = vec1['658'][:]
    vec2 = vec2['658'][:]
    return GetCosineSimilarity(vec1, vec2)

# Check if it is in the rectangle.(obj1 is outside)
def CheckWithinRectangle(x_min1, y_min1, x_max1, y_max1, x_min2, y_min2, x_max2, y_max2):
    if x_min1 < x_min2 and y_min1 < y_min2 and x_max1 > x_max2 and y_max1 > y_max2:
        return True
    else:
        return False



# Class
class Object:
    def __init__(self, input_id, x_min, y_min, x_max, y_max, first_time, last_time):
        self.obj_id = input_id
        self.x_min = int(x_min)
        self.x_max = int(x_max)
        self.y_min = int(y_min)
        self.y_max = int(y_max)
        self.first_time = first_time
        self.last_time = last_time


class Person:
    def Update(self, update_mode, input_id, update_id_flag, x_min, y_min, x_max, y_max, last_time):
        if update_mode == 'person':
            if update_id_flag == True:
                self.person.temporary_object = Object(input_id, x_min, y_min, x_max, y_max, self.face.temporary_object.first_time, last_time)
            else:
                self.person.temporary_object = Object(self.person.temporary_object.obj_id, x_min, y_min, x_max, y_max, self.face.temporary_object.first_time, last_time)
        elif update_mode == 'face':
            if update_id_flag == True:
                self.face.temporary_object = Object(input_id, x_min, y_min, x_max, y_max, self.face.temporary_object.first_time, last_time)
            else:
                self.face.temporary_object = Object(self.face.temporary_object.obj_id, x_min, y_min, x_max, y_max, self.face.temporary_object.first_time, last_time)   
        
    def __init__(self, person, face):
        self.face = face
        self.person = person
        print('Create new person object!')

class TemporaryObject:
    def Update(self, input_id, update_id_flag, x_min, y_min, x_max, y_max, last_time):
        if update_id_flag == True:
            self.temporary_object = Object(input_id, x_min, y_min, x_max, y_max, self.temporary_object.first_time, last_time)
        else:
            self.temporary_object = Object(self.temporary_object.obj_id, x_min, y_min, x_max, y_max, self.temporary_object.first_time, last_time)
    def __init__(self, input_id, x_min, y_min, x_max, y_max, first_time):
        self.temporary_object = Object(input_id, x_min, y_min, x_max, y_max, first_time, first_time)
        print('Create new temporary object!')



def CheckPersonClassList(result_of_id, class_list, face_or_person, threshold_list, x_min, y_min, x_max, y_max, now_time):
    if len(class_list) != 0:
        if face_or_person == 'face':
            p_id = CheckParentObject(class_list, x_min, y_min, x_max, y_max)
            if p_id != -1:
                if class_list[p_id].person.temporary_object.last_time == now_time:
                    class_list[p_id].Update('face', result_of_id, True, x_min, y_min, x_max, y_max, now_time)
                    return p_id

        i_list = []
        for i in range(len(class_list)):
            if face_or_person == 'face':
                if GetFaceCosineSimilarity(result_of_id, class_list[i].face.temporary_object.obj_id) > threshold_list[0][0]:
                    i_list.append(i)
            else:
                if GetPersonCosineSimilarity(result_of_id, class_list[i].person.temporary_object.obj_id) > threshold_list[1][0]:
                    i_list.append(i)
        if len(i_list) != 0:
            max_i = i_list[0]
            max_buf = 0
            for j in range(len(i_list)):
                if face_or_person == 'face':
                    buf = GetFaceCosineSimilarity(result_of_id, class_list[i_list[j]].face.temporary_object.obj_id)
                else:
                    buf = GetPersonCosineSimilarity(result_of_id, class_list[i_list[j]].person.temporary_object.obj_id)
                if max_buf < buf:
                    max_buf = buf
                    max_i = i_list[j]
            if face_or_person == 'face':
                if max_buf > threshold_list[0][1]:
                    class_list[max_i].Update('face', result_of_id, True, x_min, y_min, x_max, y_max, now_time)
                else:
                    class_list[max_i].Update('face', result_of_id, False, x_min, y_min, x_max, y_max, now_time)
            elif face_or_person == 'person':
                if max_buf > threshold_list[1][1]:
                    class_list[max_i].Update('person', result_of_id, True, x_min, y_min, x_max, y_max, now_time)
                else:
                    class_list[max_i].Update('person', result_of_id, False, x_min, y_min, x_max, y_max, now_time)
            return max_i
        else:
            return - 1
    return -1

def CheckTemporaryPersonClassList(result_of_id, child_class_list, face_or_person, threshold_list, x_min, y_min, x_max, y_max, now_time):
    result = 0
    if len(child_class_list) != 0:
        # Check list
        i_list = []
        all_list = []
        for i in range(len(child_class_list)):
            if face_or_person == 'face':
                all_list.append(GetFaceCosineSimilarity(result_of_id, child_class_list[i].temporary_object.obj_id))
                if all_list[i] > threshold_list[0][0]:
                    i_list.append(i)
            else:
                all_list.append(GetPersonCosineSimilarity(result_of_id, child_class_list[i].temporary_object.obj_id))
                if all_list[i] > threshold_list[1][0]:
                    i_list.append(i)
        # Update object
        if len(i_list) != 0:
            max_i = i_list[0]
            max_buf = 0
            for j in range(len(i_list)):
                if face_or_person == 'face':
                    buf = GetFaceCosineSimilarity(result_of_id, child_class_list[i_list[j]].temporary_object.obj_id)
                else:
                    buf = GetPersonCosineSimilarity(result_of_id, child_class_list[i_list[j]].temporary_object.obj_id)
                if max_buf < buf:
                    max_buf = buf
                    max_i = i_list[j]
            if face_or_person == 'face' and max_buf > threshold_list[0][1]:
                child_class_list[max_i].Update(result_of_id, True, x_min, y_min, x_max, y_max, now_time)
            elif face_or_person == 'person' and max_buf > threshold_list[1][1]: 
                child_class_list[max_i].Update(result_of_id, True, x_min, y_min, x_max, y_max, now_time)
            else:
                child_class_list[max_i].Update(result_of_id, False, x_min, y_min, x_max, y_max, now_time)
            result = max_i
        # New object
        else:
            if face_or_person == 'face' and np.max(all_list) < threshold_list[0][2]:
                child_class_list.append(TemporaryObject(result_of_id, x_min, y_min, x_max, y_max, now_time)) 
                result = len(child_class_list) - 1
            elif face_or_person == 'person' and np.max(all_list) < threshold_list[1][2]: 
                child_class_list.append(TemporaryObject(result_of_id, x_min, y_min, x_max, y_max, now_time)) 
                result = len(child_class_list) - 1
            else:
                result = - 1
    # First object
    else:
        child_class_list.append(TemporaryObject(result_of_id, x_min, y_min, x_max, y_max, now_time)) 
        result = len(child_class_list) - 1

    return result

def CheckParentObject(person_class, x_min, y_min, x_max, y_max):
    result = -1
    if len(person_class) != 0:
        for i in range(len(person_class)):
            if CheckWithinRectangle(person_class[i].person.temporary_object.x_min, person_class[i].person.temporary_object.y_min, person_class[i].person.temporary_object.x_max, person_class[i].person.temporary_object.y_max, x_min, y_min, x_max, y_max) == True:
                result = i
                break
    return result

def CheckParentObjectAndMerge(person_class, temporary_person_class, temporary_face_class, face_id_num):
    if len(temporary_person_class) != 0:
        for i in range(len(temporary_person_class)):
            if CheckWithinRectangle(temporary_person_class[i].temporary_object.x_min, temporary_person_class[i].temporary_object.y_min, temporary_person_class[i].temporary_object.x_max, temporary_person_class[i].temporary_object.y_max, temporary_face_class[face_id_num].temporary_object.x_min, temporary_face_class[face_id_num].temporary_object.y_min,temporary_face_class[face_id_num].temporary_object.x_max, temporary_face_class[face_id_num].temporary_object.y_max) == True:
                person_class.append(Person(temporary_person_class.pop(i), temporary_face_class.pop(face_id_num)))
                break

# Main
def Main():
    # Launch message
    print('[mics-dev version0.0.3]')

    # Setup camera
    capture = SetupCamera(CAM_ID, CAM_X, CAM_Y, CAM_FPS)

    # Setup OpenVINO
    # Generate Inference Engine Core object
    ie = IECore()
    
    # Setup person detection
    input_name_PD, input_shape_PD, _, _, exec_net_PD = SetupModel(ie, DEVICE_NAME, './models/person-detection-retail-0013/FP16/person-detection-retail-0013')

    # Setup person detection
    input_name_PRR, input_shape_PRR, _, _, exec_net_PRR = SetupModel(ie, DEVICE_NAME, './models/' + PERSON_REIDENTIFICATION_MODEL + '/FP16/' + PERSON_REIDENTIFICATION_MODEL)

    # Setup face detection
    input_name_FD, input_shape_FD, out_name_FD, _, exec_net_FD = SetupModel(ie, DEVICE_NAME, './models/face-detection-adas-0001/FP16/face-detection-adas-0001')

    # Setup person detection
    input_name_FRR, input_shape_FRR, _, _, exec_net_FRR = SetupModel(ie, DEVICE_NAME, './models/face-reidentification-retail-0095/FP16/face-reidentification-retail-0095')

    # Setup age gender detectuon
    input_name_AGD, input_shape_AGD, _, _, exec_net_AGD = SetupModel(ie, DEVICE_NAME, './models/age-gender-recognition-retail-0013/FP16/age-gender-recognition-retail-0013')
    
    # Setup face landmark detection
    #input_name_LD, input_shape_LD, out_name_LD, _, exec_net_LD = SetupModel(ie, DEVICE_NAME, './models/facial-landmarks-35-adas-0002/FP16/facial-landmarks-35-adas-0002')

    # Setup face landmark(5) detection
    input_name_LD5, input_shape_LD5, out_name_LD5, _, exec_net_LD5 = SetupModel(ie, DEVICE_NAME, './models/landmarks-regression-retail-0009/FP16/landmarks-regression-retail-0009')

    # Setup head pose estimation
    input_name_HPE, input_shape_HPE, out_name_HPE, out_shape_HPE, exec_net_HPE = SetupModel(ie, DEVICE_NAME, './models/head-pose-estimation-adas-0001/FP16/head-pose-estimation-adas-0001')

    # Setup gaze estimation
    #_, input_shape_GE, _, _, exec_net_GE = SetupModel(ie, DEVICE_NAME, './models/gaze-estimation-adas-0002/FP16/gaze-estimation-adas-0002')


    # Create class object
    person_list = []
    temporary_person_list = []
    temporary_face_list = []


    # Loop
    while(True):
        # Get a frame
        ret, frame = capture.read()
        if ret==False:
            break

        # Get now time
        now_time = datetime.datetime.now()

        # Get person detction data
        result_of_person_detection = GetDetectionData(frame, exec_net_PD, input_name_PD, input_shape_PD)
        for person_object in result_of_person_detection[out_name_FD][0][0]:
            if person_object[2] > THRESHOLD_PERSON_DETECTION:
                px_min, py_min, px_max, py_max = GetXYMinMaxFromDetection(person_object,frame)
                #print("get person!")

                person = frame[py_min:py_max,px_min:px_max]

                # Get person id and check
                result_of_person_id = GetDetectionData(person, exec_net_PRR, input_name_PRR, input_shape_PRR)

                # Update object
                person_id_buf = CheckPersonClassList(result_of_person_id, person_list, 'person', THRESHOLD_PERSON_REIDENTIFICATION, px_min, py_min, px_max, py_max, now_time)
                if person_id_buf == -1:
                    buf = CheckTemporaryPersonClassList(result_of_person_id, temporary_person_list, 'person', THRESHOLD_PERSON_REIDENTIFICATION, px_min, py_min, px_max, py_max, now_time)
                    cv2.putText(frame, text='[id] body', org=(px_min, py_min - 25), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                    cv2.putText(frame, text=' id = ' + str(buf), org=(px_min, py_min - 5), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                else:
                    cv2.putText(frame, text='[id] person', org=(px_min, py_min - 25), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 127), thickness=2, lineType=cv2.LINE_AA)
                    cv2.putText(frame, text=' id = ' + str(person_id_buf), org=(px_min, py_min - 5), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 127), thickness=2, lineType=cv2.LINE_AA)

                # Show in window
                cv2.rectangle(frame, (px_min, py_min), (px_max, py_max), (0, 0, 255), 2)

        # Get face detection data
        result_of_face_detection = GetDetectionData(frame, exec_net_FD, input_name_FD, input_shape_FD)
        for face_object in result_of_face_detection[out_name_FD][0][0]:
            if face_object[2] > THRESHOLD_FACE_DETECTION:
                face_pos = GetXYMinMaxFromDetection(face_object,frame)
                x_min, y_min, x_max, y_max = face_pos
                #print("get face!")

                # Get face image
                face=frame[y_min:y_max,x_min:x_max]

                # Get age and gender from face image
                result_of_age_gender_detection = GetAgeGenderData(face, exec_net_AGD, input_name_AGD, input_shape_AGD)

                # Get head pose estimation
                result_of_head_pose_estimation = GetHeadPoseEstimationData(face, exec_net_HPE, input_name_HPE,input_shape_HPE)
                
                # Get face landmark from face image
                result_of_face_landmaek_detection = GetFaceLandmarkDetectionData(face, exec_net_LD5, input_name_LD5, input_shape_LD5, out_name_LD5, face_pos)

                # Get additional face landmark from face image
                #result_of_face_landmaek_detection = np.vstack([result_of_face_landmaek_detection, GetFaceLandmarkDetectionData(face, exec_net_LD, input_name_LD, input_shape_LD, out_name_LD, face_pos)])

                # Get distance from face landmark and gender (experimental)
                result_of_distance_estimation, face_to_cam_angle = GetDistanceFromLandmark(result_of_face_landmaek_detection[0], result_of_face_landmaek_detection[1], result_of_head_pose_estimation, result_of_age_gender_detection, frame.shape[1], frame.shape[0], ANGLE_OF_VIEW)

                # Get perspective data
                perspective = GetPerspective(result_of_distance_estimation, face_to_cam_angle, [(result_of_head_pose_estimation[0] * np.pi / 180.0), (result_of_head_pose_estimation[1] * np.pi / 180.0)])

                # Get face id and check
                result_of_face_id = GetDetectionData(face, exec_net_FRR, input_name_FRR, input_shape_FRR)

                # Update object
                person_id_buf = CheckPersonClassList(result_of_face_id, person_list, 'face', THRESHOLD_PERSON_REIDENTIFICATION, x_min, y_min, x_max, y_max, now_time)
                if person_id_buf == -1:
                    buf = CheckTemporaryPersonClassList(result_of_face_id, temporary_face_list, 'face', THRESHOLD_PERSON_REIDENTIFICATION, x_min, y_min, x_max, y_max, now_time)
                    CheckParentObjectAndMerge(person_list,temporary_person_list,temporary_face_list, buf )
                    cv2.putText(frame, text='[id] face', org=(x_min, y_min - 65), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                    cv2.putText(frame, text=' id = ' + str(buf), org=(x_min, y_min - 45), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                else:
                    cv2.putText(frame, text='[id] person', org=(x_min, y_min - 65), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 127), thickness=2, lineType=cv2.LINE_AA)
                    cv2.putText(frame, text=' id = ' + str(person_id_buf), org=(x_min, y_min - 45), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, color=(0, 255, 127), thickness=2, lineType=cv2.LINE_AA)
                

                # Show data in frame
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