from check import multihsvcheck

if __name__ == "__main__":
    color = {
        "h": [[[13, 108, 0], [26, 255, 255]]],
        "m": [[[23, 0, 0], [68, 102, 255]]],
        "l": [[[73, 20, 174], [97, 255, 255]]]
    }
    path = "/Users/fan/python-workspace/imagex/check-img/std_pic.jpeg"
    rslt, draw_img = multihsvcheck.get_info(path, color)
    print(rslt)
