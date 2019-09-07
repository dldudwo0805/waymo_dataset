import numpy as np
import cv2


def parse_calibration_data(data, sensor_type):
    intrinsic = np.eye(3, dtype=np.float32)
    extrinsic = np.eye(4, dtype=np.float32)
    distortion = np.zeros((1,5), dtype=np.float32)
    sensor_name = None
    if sensor_type == "CAM" or sensor_type == "CAMERA":
        if data.name == 0:
            sensor_name = "Unknown\n"
        elif data.name == 1:
            sensor_name = "Front\n"
        elif data.name == 2:
            sensor_name = "Front Left\n"
        elif data.name == 3:
            sensor_name = "Front Right\n"
        elif data.name == 4:
            sensor_name = "Side Left\n"
        elif data.name == 5:
            sensor_name = "Side Right\n"
        else:
            sensor_name = "Unknown\n"

        intrinsic[0, 0] = data.intrinsic[0]
        intrinsic[1, 1] = data.intrinsic[1]
        intrinsic[0, 2] = data.intrinsic[2]
        intrinsic[1, 2] = data.intrinsic[3]

        distortion[0, 0] = data.intrinsic[4]
        distortion[0, 1] = data.intrinsic[5]
        distortion[0, 2] = data.intrinsic[6]
        distortion[0, 3] = data.intrinsic[7]
        distortion[0, 4] = data.intrinsic[8]

        cnt = 0
        for val in data.extrinsic.transform:
            extrinsic[int(cnt/4), int(cnt % 4)] = val
            cnt += 1

    return sensor_name, intrinsic, extrinsic, distortion


def save_calibration_data(file, sensor_name, intrinsic, extrinsic, distortion=None):
    file.write(sensor_name)
    _intrinsic = "%f, %f, %f\n%f, %f, %f\n%f, %f, %f\n"\
                 %(intrinsic[0, 0], intrinsic[0, 1], intrinsic[0,2],
                   intrinsic[1, 0], intrinsic[1, 1], intrinsic[1,2],
                   intrinsic[2, 1], intrinsic[2, 2], intrinsic[2, 2])
    file.write(_intrinsic)
    _extrinsic = "%f, %f, %f, %f\n%f, %f, %f, %f\n%f, %f, %f, %f\n%f, %f, %f, %f\n"\
                 %(extrinsic[0, 0], extrinsic[0, 1], extrinsic[0, 2], extrinsic[0, 3],
                    extrinsic[1, 0], extrinsic[1, 1], extrinsic[1, 2], extrinsic[1, 3],
                    extrinsic[2, 0], extrinsic[2, 1], extrinsic[2, 2], extrinsic[2, 3],
                    extrinsic[3, 0], extrinsic[3, 1], extrinsic[3, 2], extrinsic[3, 3])
    file.write(_extrinsic)
    if distortion is not None:
        _distortion = "%f, %f, %f, %f, %f\n"\
                      %(distortion[0, 0], distortion[0, 1], distortion[0, 2], distortion[0, 3], distortion[0, 4])
        file.write(_distortion)

    file.write('\n')


def save_image(save_root, sensor_position, index, image):
    filename = "%s/%s_%04d.png"%(save_root, sensor_position, index)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, image)
    cv2.waitKey(1)



