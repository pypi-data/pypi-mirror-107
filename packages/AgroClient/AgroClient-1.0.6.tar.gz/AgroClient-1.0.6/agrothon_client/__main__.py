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