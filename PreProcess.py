"""
The unique fonction image_process() is a function which take two args of string path file
and return a matrice with the current state game.
"""
import cv2
from math import sqrt


def image_process(image_path: str, template_path: str):
    """
    :param template_path: file path to the template of chessboard
    :param image_path: file path to image to process
    :return: matrix of the game state
    """
    def list_of_corners(img):
        """
        :param img: image's pixel matrix, template is best to find corner, use gray mode give better result
        :return: list of position (x, y) of corners on chessboard
        """
        found, corners = cv2.findChessboardCorners(img, (6, 5), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.
                                                   CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_FAST_CHECK)
        corners_list = []
        if found:
            case_one = str(corners[0]).strip('[] ').split(' ')
            case_two = str(corners[int(sqrt(len(corners))) + 2]).strip('[] ').split(' ')
            delta_x = int(float(case_two[0])) - int(float(case_one[0]))
            delta_y = int(float(case_two[-1])) - int(float(case_one[-1]))
            # add exterior corners which is not check by cv2.finChessboardCorners()
            for i in range(len(corners)):
                if i == 0:
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])) - delta_x,
                                         int(float(str(corners[i]).strip('[] ').split(' ')[-1])) - delta_y))
                    # first line of exterior corners (up)
                    for j in range(int(sqrt(len(corners))) + 1):
                        corners_list.append((int(float(str(corners[j]).strip('[] ').split(' ')[0])),
                                            int(float(str(corners[j]).strip('[] ').split(' ')[-1])) - delta_y))
                    corners_list.append((int(float(str(corners[int(sqrt(len(corners)))]).strip('[] ').split(
                        ' ')[0])) + delta_x, int(float(str(corners[int(sqrt(len(corners)))]).strip(
                                        '[] ').split(' ')[-1])) - delta_y))
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])) - delta_x,
                                         int(float(str(corners[i]).strip('[] ').split(' ')[-1]))))
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])),
                                         int(float(str(corners[i]).strip('[] ').split(' ')[-1]))))
                # exterior left side
                elif i in [(int(sqrt(len(corners))) + 1) * (i + 1)for i in range(int(sqrt(len(corners))) - 1)]:
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])) - delta_x,
                                         int(float(str(corners[i]).strip('[] ').split(' ')[-1]))))
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])),
                                         int(float(str(corners[i]).strip('[] ').split(' ')[-1]))))
                # exterior right side
                elif i in [(int(sqrt(len(corners)))) * (i + 1) + i for i in range(int(sqrt(len(corners))))]:
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])),
                                         int(float(str(corners[i]).strip('[] ').split(' ')[-1]))))
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])) + delta_x,
                                         int(float(str(corners[i]).strip('[] ').split(' ')[-1]))))
                # all normals lines
                elif i < len(corners):
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])),
                                         int(float(str(corners[i]).strip('[] ').split(' ')[-1]))))
                # last line
                if i == (len(corners) - 1):
                    corners_list.append((int(float(str(corners[len(corners) - (int(sqrt(len(corners))) + 1)]).strip(
                        '[] ').split(' ')[0])) - delta_x, int(float(str(corners[len(corners) - (int(sqrt(len(corners)))
                                                                        + 1)]).strip('[] ').split(' ')[-1])) + delta_y))
                    for j in range(len(corners) - (int(sqrt(len(corners))) + 1), len(corners)):
                        corners_list.append((int(float(str(corners[j]).strip('[] ').split(' ')[0])),
                                            int(float(str(corners[j]).strip('[] ').split(' ')[-1])) + delta_y))
                    corners_list.append((int(float(str(corners[i]).strip('[] ').split(' ')[0])) + delta_x,
                                        int(float(str(corners[i]).strip('[] ').split(' ')[-1])) + delta_y))
        return corners_list

    # add green point at corners
    image = cv2.imread(image_path, 1)
    template = cv2.imread(template_path, 0)
    corners_lst = list_of_corners(template)
    matrix = [['E' for _ in range(int(sqrt(len(corners_lst))))] for __ in range(int(sqrt(len(corners_lst))) - 1)]
    matrix_case = 0
    matrix_line = 0
    for k in range(len(corners_lst)):
        if k in [int(sqrt(len(corners_lst))) * (n+1) + n for n in range(int(sqrt(len(corners_lst))) - 1)]:
            pass
        elif k > 46:
            pass
        else:
            # pixel = image[y][x]
            pixel = image[int((corners_lst[k][1] + corners_lst[k + 2 + int(sqrt(len(corners_lst)))][1]) / 2)][int((
                                        corners_lst[k][0] + corners_lst[k + 2 + int(sqrt(len(corners_lst)))][0]) / 2)]
            if matrix_case == 7:
                matrix_case = 0
                matrix_line += 1
            pixel = str(pixel).strip('[] ').split(' ')
            int_typed = False
            while not int_typed:
                if len(pixel) == 3:
                    pixel = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
                    int_typed = True
                else:
                    for z in range(len(pixel)):
                        if pixel[z] == '':
                            del pixel[z]
                            break
            pixel_b, pixel_g, pixel_r = pixel[0], pixel[1], pixel[2]
            if 30 < pixel_b < 120 < pixel_r and pixel_g > 120:  # yellow color detection
                matrix[matrix_line][matrix_case] = 'Y'
            elif pixel_b < 100 < pixel_r and pixel_g < 100:  # red color detection
                matrix[matrix_line][matrix_case] = 'R'
            matrix_case += 1
    return matrix
