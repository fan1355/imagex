
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(filename)s[line:%(lineno)d]: %(message)s')
# logging.basicConfig函数对日志的输出格式及方式做相关配置
logger = logging.getLogger("cmd")

logger.info("test log")


print("hello print")