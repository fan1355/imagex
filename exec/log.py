import logging

def initCmdLog():
    logger = logging.getLogger("cmd")
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # 输出到console的log等级的开关
    # 第四步和第五步分别加入以下代码即可
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("init log")