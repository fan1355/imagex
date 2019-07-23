import numpy as np

def get_color_list(color):
    switch = {
        # 绿色的范围
        "green": [(np.array([47, 65, 18]), np.array([96, 255, 153]))],
        # 红色范围
        "red": [
                (np.array([0, 43, 46]), np.array([10, 255, 255])),
                (np.array([156, 43, 46]), np.array([180, 255, 255]))
            ],
        # 蓝色范围
        "blue": [(np.array([95, 130, 70]), np.array([166, 255, 255]))],
        # 白色
        "white": [(np.array([0, 0, 221]), np.array([180, 30, 255]))],
        # 橙色
        # "orange": [(np.array([11, 43, 46]), np.array([25, 255, 255]))],
        "orange": [
            (np.array([6, 123, 110]), np.array([43, 255, 170])),
            (np.array([9, 111, 193]), np.array([180, 255, 255])),
        ], # test
        # 黄色
        "yellow": [(np.array([26, 43, 46]), np.array([34, 255, 255]))],
        # 紫色
        "purple": [(np.array([125, 43, 46]), np.array([155, 255, 255]))],

    }

    try:
        return switch[color]
    except KeyError:
        return []