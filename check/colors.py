import numpy as np

def get_color_list(color):
    switch = {
        # 绿色的范围
        "green": [(np.array([47, 65, 18]), np.array([96, 255, 153]))],
        # 红色范围
        "red": [
                (np.array([0, 170, 170]), np.array([7, 255, 255])),
                (np.array([137, 170, 170]), np.array([180, 255, 255]))
            ],
        # 蓝色范围
        "blue": [(np.array([95, 130, 70]), np.array([166, 255, 255]))]
    }

    try:
        return switch[color]
    except KeyError:
        return []