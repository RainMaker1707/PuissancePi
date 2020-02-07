"""
cam_to_frame: se camera to get frame and save images on data_set/temporary as game_state.jpg
Pre-process for Process module which return a matrix of the game state
"""
import cv2


def cam_to_frame(used_cam: int):
    """
    :param used_cam: 0 for default cam 1,2 etc for other
    :return: the frame pixels matrix
    """
    cam = cv2.VideoCapture(used_cam)
    check = False
    frame = None
    while not check:
        check, frame = cam.read()
    cv2.imwrite('data_set/temporary/game_state.jpg', frame)
