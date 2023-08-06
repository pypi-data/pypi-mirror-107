"""
@File    :   __main__.py
@Path    :   agrothon_client/
@Time    :   2021/05/28
@Author  :   Chandra Kiran Viswanath Balusu
@Version :   1.0.7
@Contact :   ckvbalusu@gmail.com
@Desc    :   Main Module for Agrothon
"""
from .utils import *
import multiprocessing

def main():
    pool = multiprocessing.Pool()
    sen_result = pool.apply_async(serial_sensor_in)
    pump_result = pool.apply_async(pump_status)
    multiprocessing.Process(motion_intruder_detect(), daemon=True).start()
    sen_result.wait()
    pump_result.wait()


if __name__ == '__main__':
    main()