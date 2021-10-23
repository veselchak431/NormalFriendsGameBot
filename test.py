from numpy import array
def benchmark(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        return_value = func(*args, **kwargs)
        end = time.perf_counter()
        print('[*] Время выполнения: {} секунд.'.format(end - start))
        return return_value
    return wrapper


def ReturnEncodingsFromSQL(SQLStringData):
    array_data = SQLStringData[8:-3].split(",")
    for i in range(len(array_data)):
        array_data[i] = float(array_data[i].strip())
    finaly_data = [array(array_data)]
    return finaly_data




