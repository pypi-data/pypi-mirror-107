import os
import datetime
from timeit import default_timer as timer
from typing import Callable
import cProfile
import pstats
import io
import numpy as np
import random
import inspect
import sys
import time
import pickle
from itertools import combinations
import shutil
import math
import psutil
import platform

LINES = '-' * 80
NOT_FOUND = '{} Not found'
CREATED = '{} Created'
EXISTS = '{} Exists'
DELETED = '{} Deleted'
SAVED = '{} Saved'
LOADED = '{} Loaded'
CONTENT = 'Content: {}'
SUCCESS_C = 'light_green'
SUCCESS_C2 = ('black', ['bold', 'background_green'])
FAIL_C = 'red'
FAIL_C2 = ('black', ['bold', 'background_red'])

CONST_COLOR_SHORTCUTS = {
    'b': 'blue',
    'g': 'green',
    'r': 'red',
    'c': 'cyan',
    'm': 'magenta',
    'y': 'yellow',
    'k': 'black',
    'w': 'white',
    'bo': 'bold',
    'un': 'underlined',
    're': 'reverse',
}

CONST_COLOR_MAP = {
    'reset_all': "\033[0m",
    'bold': "\033[1m",
    'underlined': "\033[4m",
    'reverse': "\033[7m",  # switch font color and background color

    'blue': "\033[34m",
    'background_blue': "\033[44m",
    'light_blue': "\033[94m",
    'background_light_blue': "\033[104m",

    'green': "\033[32m",
    'background_green': "\033[42m",
    'light_green': "\033[92m",
    'background_light_green': "\033[102m",

    'red': "\033[31m",
    'background_red': "\033[41m",
    'light_red': "\033[91m",
    'background_light_red': "\033[101m",

    'cyan': "\033[36m",
    'background_cyan': "\033[46m",
    'background_light_cyan': "\033[106m",
    'light_cyan': "\033[96m",

    'magenta': "\033[35m",
    'background_magenta': "\033[45m",
    'light_magenta': "\033[95m",
    'background_light_magenta': "\033[105m",

    'yellow': "\033[33m",
    'background_yellow': "\033[43m",
    'light_yellow': "\033[93m",
    'background_light_yellow': "\033[103m",

    'light_gray': "\033[37m",
    'background_light_gray': "\033[47m",
    'dark_gray': "\033[90m",
    'background_dark_gray': "\033[100m",

    'black': "\033[97m",
    'background_black': "\033[107m",

    'white': "\033[30m",
    'background_white': "\033[40m",
}


def exception_error(e: (Exception, str), tabs: int = 1):
    """
    Aux function - print exception error in red with function name
    :param e: error. e.g. <class 'ModuleNotFoundError'>
    :param tabs:
    :return:
    """
    error_str = '{}{}: {}'.format(tabs * '\t', get_function_name(depth=2), e)
    print(add_color(string=error_str, op1='Red'))
    return


def chop_microseconds(delta: datetime.timedelta) -> datetime.timedelta:
    """
    Aux function - removes micro seconds from datetime.timedelta object
    e.g. 0:00:02.000001 -> 0:00:02
    :param delta:
    :return:
    """
    return delta - datetime.timedelta(microseconds=delta.microseconds)


def get_timer_delta(s_timer: float, with_ms: bool = False, ack: bool = False, tabs: int = 1) -> datetime.timedelta:
    """
    :param s_timer: begin time
    :param with_ms: if microseconds needed - set to true. else: no microseconds
    :param ack: print time passed
    :param tabs:
    :return:
    see timer_test()
    """
    end_timer = get_timer()
    d = datetime.timedelta(seconds=(end_timer - s_timer))
    if not with_ms:
        d = chop_microseconds(d)
    if ack:
        print('{}Time passed {}'.format(tabs * '\t', d))
    return d


def get_timer() -> float:
    """
    sets a timer beginning
    :return:
    see timer_test()
    """
    return timer()


def timer_action(seconds: int, action: str = '', tabs: int = 1) -> None:
    """
    :param seconds:
    :param action:
    :param tabs:
    :return:
    counts till seconds or block
    see timer_action_test()
    """
    if seconds is None:
        input('{}Press "Enter" key for {}...'.format(tabs * '\t', action))
    else:
        time_in_future = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        print('{}{} IN: {}'.format(tabs * '\t', action, seconds), end='', flush=True)
        while time_in_future > datetime.datetime.now():
            time.sleep(1)
            seconds -= 1
            print(' {}'.format(seconds), end='', flush=True)
        print('')
    return


def get_current_date_hour(format_s: str = '%d-%m-%Y %H:%M:%S', ack: bool = False, tabs: int = 1) -> str:
    """
    :param format_s: date time format
    :param ack: prints current time
    :param tabs:
    :return:
    see get_current_date_hour_test()
    """
    now = datetime.datetime.now()
    current_time = now.strftime(format_s)
    if ack:
        print('{}Current time is {}'.format(tabs * '\t', current_time))
    return current_time


def get_pc_name(ack: bool = False, tabs: int = 1) -> str:
    """
    :param ack:
    :param tabs:
    :return: pc name as str
    see get_pc_name_test()
    """
    try:
        pc_name = platform.uname()[1]
        if ack:
            print('{}* Computer Name: {}'.format(tabs * '\t', pc_name))
    except ModuleNotFoundError as e:
        pc_name = ''
        exception_error(e)
    return pc_name


def get_mac_address(with_colons: bool = True, ack: bool = False, tabs: int = 1) -> str:
    """
    :return: pc mac as str
    see get_mac_address_test()
    """
    try:
        from uuid import getnode as get_mac
        mac = get_mac()
        mac = "{:X}".format(mac)  # turn to Hex
        if with_colons:
            mac = ':'.join(mac[i:i + 2] for i in range(0, 12, 2))
        if ack:
            print('{}* Computer Mac: {}'.format(tabs * '\t', mac))
    except ModuleNotFoundError as e:
        mac = ''
        exception_error(e)
    return mac


def get_cuda_version(ack: bool = False, tabs: int = 1) -> str:
    """
    :param ack:
    :param tabs:
    :return: cuda version if found on environment variables
    see get_cuda_version_test()
    """
    cuda_path = get_env_variable(key='CUDA_PATH')
    if cuda_path is not None:
        cuda_v = add_color('{}* CUDA Version: {}'.format(tabs * '\t', os.path.basename(cuda_path)), op1=SUCCESS_C)
    else:
        cuda_v = add_color('* No CUDA_PATH found', op1=FAIL_C)
    if ack:
        print(cuda_v)
    return cuda_v


def get_env_variables(ack: bool = False, tabs: int = 1) -> dict:
    """
    :param ack:
    :param tabs:
    :return: dict with envs
    see get_env_variables_test()
    """
    env_d = dict(os.environ)
    if ack:
        print('{}Environment variables:'.format(tabs * '\t'))
        for k, v in env_d.items():
            print('{}\t{} = {}'.format(tabs * '\t', k, v))
    return env_d


def set_env_variable(key: str, val: str, ack: bool = False, tabs: int = 1) -> None:
    """
    :param key:
    :param val:
    :param ack:
    :param tabs:
    insert new env variable
    see set_env_variable_test()
    """
    key = key.upper()
    os.environ[key] = val
    if ack:
        print('{}Inserted to environment: {} = {}'.format(tabs * '\t', key, val))
    return


def get_env_variable(key: str, ack: bool = False, tabs: int = 1) -> str:
    """
    :param key:
    :param ack:
    :param tabs:
    :return: env variable value
    see get_env_variable_test()
    """
    key = key.upper()
    ret_val = os.environ[key] if key in os.environ else None
    if ack:
        if ret_val is not None:
            print('{}{} = {}'.format(tabs * '\t', key, ret_val))
        else:
            exception_error(NOT_FOUND.format(key), tabs)
    return ret_val


def del_env_variable(key: str, ack: bool = False, tabs: int = 1) -> None:
    """
    :param key:
    :param ack:
    :param tabs:
    :return: env variable value
    see get_env_variable_test()
    """
    key = key.upper()
    if key in os.environ:
        del os.environ[key]
        if ack:
            print('{}{}'.format(tabs * '\t', DELETED.format(key)))
    else:
        exception_error(NOT_FOUND.format(key), tabs)
    return


def make_cuda_invisible() -> None:
    """
        disable gpu 0
        FUTURE - support disabling many GPUS
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # GPU 0 available
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1, 0'  # GPU 0 not available
        os.environ['CUDA_VISIBLE_DEVICES'] = '0, -1, 0'  # GPU 0 available but 1 disabled
        os.environ['CUDA_VISIBLE_DEVICES'] = '1, 2, -1, 0'  # GPU 1,2 available but 0 disabled

        read more: https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars
        see make_cuda_invisible_test()
    """
    set_env_variable(key='CUDA_VISIBLE_DEVICES', val='-1, 0')
    return


def start_profiler() -> cProfile.Profile:
    """
    starts profiling
    :return: profiling object that is needed for end_profiler()
    see profiler_test()
    """
    pr = cProfile.Profile()
    pr.enable()
    return pr


def end_profiler(pr: cProfile.Profile, rows: int = 10, ack: bool = False) -> str:
    """
    profiling output
    :param pr: object returned from start_profiler()
    :param rows: how many rows to print sorted by 'cumulative' run time
    :param ack:
    :return: profiler output as string
    see profiler_test()
    """
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(rows)
    profiler_str = s.getvalue()
    if ack:
        print('{}'.format(profiler_str))
    return profiler_str


def set_seed(seed: int = 42) -> None:
    """
    :param seed: setting numpy and random seeds
    :return:
    see main_wrapper_test() - uses set_seed
    """
    np.random.seed(seed)
    random.seed(seed)
    return


def main_wrapper(
        main_function: Callable,
        seed: int = -1,
        ipv4: bool = False,
        cuda_off: bool = False,
        torch_v: bool = False,
        tf_v: bool = False,
        cv2_v: bool = False,
        with_profiler: bool = False
) -> None:
    """
    :param main_function: the function to run
    :param seed: if -1 no seed, else set_seed(seed=seed)
    :param ipv4: print computer ipv4
    :param cuda_off: make gpu invisible and force run on cpu
    :param torch_v: print torch version
    :param tf_v: print tensorflow version
    :param cv2_v: print opencv version
    :param with_profiler: run profiler
    template:
    wu.main_wrapper(
        main_function=main,
        seed=42,
        ipv4=False,
        cuda_off=False,
        torch_v=False,
        tf_v=False,
        cv2_v=False,
        with_profiler=False
    )
    see main_wrapper_test()
    :return:
    """
    print(LINES)
    start_timer = get_timer()

    print('main_wrapper:')
    print('* Run started at {}'.format(get_current_date_hour()))
    print('* Python Version {}'.format(sys.version))
    print('* Interpreter: {}'.format(sys.executable))
    print('* Working Dir: {}'.format(os.getcwd()))
    print('* Computer Name: {}'.format(get_pc_name()))
    print('* Computer Mac: {}'.format(get_mac_address()))
    print('* CPU Info: {}'.format(cpu_info(one_liner=True, tabs=0)))
    print('* Physical Memory: {}'.format(hard_disc(one_liner=True, tabs=0)))
    print('* RAM: {}'.format(ram_size(one_liner=True, tabs=0)))

    if ipv4:
        try:
            from wizzi_utils.socket.socket_tools import get_ipv4
            print('* Computer ipv4: {}'.format(get_ipv4()))
        except (ImportError, ModuleNotFoundError, NameError) as err:
            string = '* {}'.format(err)
            print(string)

    cuda_msg = get_cuda_version(ack=False, tabs=0)
    if cuda_off:
        make_cuda_invisible()
        cuda_msg += ' (Turned off)'
    print(cuda_msg)

    if torch_v:
        try:
            from wizzi_utils.torch.torch_tools import get_torch_version
            print(get_torch_version(ack=False, tabs=0))
        except (ImportError, ModuleNotFoundError, NameError) as err:
            print(add_color('* {}'.format(err), 'r'))

    if tf_v:
        try:
            from wizzi_utils.tensorflow.tensorflow_tools import get_tensorflow_version
            print(get_tensorflow_version(ack=False, tabs=0))
        except (ImportError, ModuleNotFoundError, NameError) as err:
            print(add_color('* {}'.format(err), 'r'))

        try:
            from wizzi_utils.tflite.tflite_tools import get_tflite_version
            print(get_tflite_version(ack=False, tabs=0))
        except (ImportError, ModuleNotFoundError, NameError) as err:
            print(add_color('* {}'.format(err), 'r'))

    if cv2_v:
        try:
            from wizzi_utils.open_cv.open_cv_tools import get_cv_version
            print(get_cv_version(ack=False, tabs=0))
        except (ImportError, ModuleNotFoundError, NameError) as err:
            string = '* {}'.format(err)
            print(string)

    if seed > -1:
        set_seed(seed=seed)
        print('* Seed was initialized to {}'.format(seed))

    print('Function {} started:'.format(main_function))
    print(LINES)
    pr = start_profiler() if with_profiler else None

    main_function()
    if with_profiler:
        print(end_profiler(pr))

    print(LINES)
    print('Total run time {}'.format(get_timer_delta(start_timer)))
    return


def get_data_str(data_str_raw, chars: (int, str)) -> str:
    """
    Aux function for to_str()
    :param data_str_raw:
    :param chars:
    :return: data_str
    """
    data_str_raw = data_str_raw.replace('\n', '').replace('  ', '')
    if chars == 'all':  # all data
        chars = len(data_str_raw) + 1
    elif chars is None:  # no data
        chars = 0

    data_str_rep = ': {}'.format(data_str_raw[:chars])

    if len(data_str_raw) > chars > 0:
        data_str_rep += ' ...too long'
    return data_str_rep


def is_int(var: any) -> bool:
    return isinstance(var, (int, np.int, np.int32, np.uint8))


def is_float(var: any) -> bool:
    return isinstance(var, (float, np.float, np.float32, np.float64))


def to_str(var: any,
           title: str = 'var',
           chars: (int, str) = 100,
           fp: (int, None) = 2,
           wm: bool = True,
           rec: bool = False
           ) -> str:
    """
    :param var: the variable
    :param title: str: the title (usually variable name)
    :param chars: int, None or str:
        chars>0: maximal number of chars
        chars==None: no chars
        chars=='all': all chars
    :param fp: float_precision: round number if possible(float, list or np array of floats...)
            fp>=0 round
            fp==None: no rounding
    :param wm: with_meta: with meta data such as type, len\shape, dtype...
    :param rec: recursive: to keep printing if there are more items inside e.g. np.array(shape=(2,3,4)) -> 3 prints
    :return: informative string of the variable
    see to_str_test()
    """

    string = title

    if is_float(var):
        if wm:
            type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
            string += '({})'.format(type_s)
        if fp is not None and fp >= 0:
            f_format = '{:,.%xf}' % fp
        else:
            f_format = '{:,}'
        data_str_raw = f_format.format(var)
        string += get_data_str(data_str_raw, chars)

    elif is_int(var):
        if wm:
            type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
            string += '({})'.format(type_s)
        data_str_raw = '{:,}'.format(var)
        string += get_data_str(data_str_raw, chars)

    elif isinstance(var, str):
        if wm:
            type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
            string += '({}'.format(type_s)
            string += ',len={})'.format(var.__len__())
        string += get_data_str(var, chars)

    elif isinstance(var, (list, tuple)):
        if wm:
            type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
            string += '({}'.format(type_s)
            string += ',len={})'.format(var.__len__())

        if fp is not None and fp >= 0:
            # 1d list\tuple - nice print
            if all((is_int(item) or is_float(item)) for item in var):
                if fp > 0 and all(isinstance(item, int) for item in var):
                    fp = 0
                f_format = '{:,.%xf}' % fp
                new_v = [f_format.format(li_item) for li_item in var]
            else:  # 2d list\tuple - could fail if found strings or types that cant be rounded
                new_v = round_list(var, fp)
        else:  # fp = None - no rounding
            new_v = var

        if isinstance(var, tuple):
            new_v = tuple(new_v)

        data_str_raw = str(new_v).replace('\'', '')

        string += get_data_str(data_str_raw, chars)
        if rec and len(var) > 0:
            inner_str = to_str(var=var[0], title='{}[0]'.format(title), chars=chars, fp=fp, rec=rec)
            string += '\n\t{}'.format(inner_str)

    elif isinstance(var, np.ndarray):
        if wm:
            type_s = str(type(var)).replace('<class \'', '').replace('\'>', '').replace('numpy.', '')
            string += '({}'.format(type_s)
            string += ',s={}'.format(var.shape)
            string += ',dtype={})'.format(var.dtype)

        if fp is not None and fp >= 0:
            new_v = np.around(var.tolist(), fp).tolist()
        else:
            new_v = var.tolist()
        data_str_raw = str(new_v).replace('\'', '')
        string += get_data_str(data_str_raw, chars)
        if rec and var.shape[0] > 0:  # recursive call
            inner_str = to_str(var=var[0], title='{}[0]'.format(title), chars=chars, fp=fp, rec=rec)
            string += '\n\t{}'.format(inner_str)

    elif isinstance(var, dict):
        if wm:
            type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
            string += '({}'.format(type_s)
            string += ',len={}'.format(var.__len__())
            string += ',keys={})'.format(list(var.keys()))
        string += get_data_str(str(var), chars)
        if rec and len(var) > 0:  # recursive call
            first_k = next(iter(var))
            inner_str = to_str(var=var[first_k], title='{}[{}]'.format(title, first_k), chars=chars, fp=fp, rec=rec)
            string += '\n\t{}'.format(inner_str)

    else:
        # all unidentified elements get default print (title(type): data)
        # must have str() to this type
        if wm:
            type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
            string += '({})'.format(type_s)
        string += get_data_str(str(var), chars)
    return string


def save_np(t: np.array, path: str, ack: bool = True, tabs: int = 1) -> None:
    """
    :param t: numpy array
    :param path: suffix '.npy' added automatically if not exists
    :param ack:
    :param tabs:
    :return:
    see save_load_np_test()
    """
    np.save(path, t)
    if ack:
        print('{}{}'.format(tabs * '\t', SAVED.format(path)))
    return


def load_np(path: str, ack: bool = True, tabs: int = 1) -> np.array:
    """
    :param path:
    :param ack:
    :param tabs:
    :return: numpy array
    see save_load_np_test()
    """
    if os.path.exists(path):
        t = np.load(path)
        if ack:
            print('{}{}'.format(tabs * '\t', LOADED.format(path)))
    else:
        exception_error(NOT_FOUND.format(path), tabs=tabs)
        t = None
    return t


def save_npz(arrays_dict: dict, path: str, ack: bool = True, tabs: int = 1) -> None:
    """
    :param arrays_dict: e.g. { 'a': np.ones(3) }
    :param path:
    :param ack:
    :param tabs:
    :return:
    save a dict of numpy arrays
    see save_load_npz_test()
    """
    np.savez(path, **{n: a for n, a in arrays_dict.items()})
    if ack:
        print('{}Saved: {}. Keys={}'.format(tabs * '\t', path, arrays_dict.keys()))
    return


def load_npz(path: str, ack: bool = True, tabs: int = 1) -> dict:
    """
    :param path:
    :param ack:
    :param tabs:
    :return: numpy array
    see save_load_npz_test()
    """
    if os.path.exists(path):
        arrays_obj = np.load(path)
        arrays_dict = {}
        # noinspection PyUnresolvedReferences
        for k in arrays_obj.files:
            arrays_dict[k] = arrays_obj[k]
        if ack:
            print('{}{}. Keys={}'.format(tabs * '\t', LOADED.format(path), arrays_dict.keys()))
    else:
        exception_error(NOT_FOUND.format(path), tabs=tabs)
        arrays_dict = None
    return arrays_dict


def save_pkl(data_dict: dict, path: str, ack: bool = True, tabs: int = 1) -> None:
    """
    :param data_dict:
    :param path:
    :param ack:
    :param tabs:
    :return:
    see save_load_pkl_test()
    """
    file_obj = open(path, "wb")
    pickle.dump(data_dict, file_obj)
    file_obj.close()
    if ack:
        print('{}{}'.format(tabs * '\t', SAVED.format(path)))
    return


def load_pkl(path: str, ack: bool = True, tabs: int = 1) -> dict:
    """
    :param path:
    :param ack:
    :param tabs:
    :return:
    see save_load_pkl_test()
    """
    if os.path.exists(path):
        file_obj = open(path, "rb")
        data_dict = pickle.load(file_obj)
        file_obj.close()
        if ack:
            print('{}{}'.format(tabs * '\t', LOADED.format(path)))
    else:
        exception_error(NOT_FOUND.format(path), tabs=tabs)
        data_dict = None
    return data_dict


def get_uniform_dist_by_dim(A: [np.array, list]) -> (np.array, np.array):
    """
    :param A:
    :return:
    for every dimension gets the lowest and highest
    see get_uniform_dist_by_dim_test()
    """
    lows = np.min(A, axis=0)
    highs = np.max(A, axis=0)
    return lows, highs


def get_normal_dist_by_dim(A: [np.array, list]) -> (np.array, np.array):
    """
    :param A:
    :return:
    see get_normal_dist_by_dim_test()
    """
    means = np.mean(A, axis=0)
    stds = np.std(A, axis=0)
    return means, stds


def np_uniform(shape: tuple, lows: [list, int], highs: [list, int]) -> np.array:
    """
    :param shape:
    :param lows:
    :param highs:
    :return:
    see np_uniform_test()
    """
    ret = np.random.uniform(low=lows, high=highs, size=shape)
    return ret


def np_normal(shape: tuple, mius: [list, int, float], stds: [list, int, float]) -> np.array:
    """
    :param shape:
    :param mius:
    :param stds:
    :return:
    see np_normal_test()
    """
    ret = np.random.normal(loc=mius, scale=stds, size=shape)
    return ret


def generate_new_data_from_old(old_data: np.array, new_data_n: int, dist: str = 'normal'):
    """
    :param old_data:
    :param new_data_n:
    :param dist:
    :return:
    see generate_new_data_from_old_test()
    """
    d = old_data.shape[1]
    if dist == 'uniform':
        lows, highs = get_uniform_dist_by_dim(old_data)
        new_data = np_uniform(shape=(new_data_n, d), lows=lows, highs=highs)
    else:  # else normal
        means, stds = get_normal_dist_by_dim(old_data)
        new_data = np_normal(shape=(new_data_n, d), mius=means, stds=stds)
    return new_data


def np_random_integers(low: int, high: int, size: tuple) -> np.array:
    """
    :param low:
    :param high:
    :param size:
    :return:
    see np_random_integers_test()
    """
    ret = np.random.random_integers(low=low, high=high, size=size)
    return ret


def augment_x_y_numpy(X: np.array, y: np.array) -> np.array:
    """
    :param X:
    :param y:
    :return:
    see augment_x_y_numpy_test()
    """
    assert X.shape[0] == y.shape[0], 'row count must be the same'
    if len(X.shape) == 1:  # change x size()=[n,] to size()=[n,1]
        X = X.reshape(X.shape[0], 1)
    if len(y.shape) == 1:  # change y size()=[n,] to size()=[n,1]
        y = y.reshape(y.shape[0], 1)
    A = np.column_stack((X, y))
    return A


def de_augment_numpy(A: np.array) -> (np.array, np.array):
    """
    :param A:
    :return:
    see de_augment_numpy_test()
    """
    if len(A.shape) == 1:  # A is 1 point. change from size (n) to size (1,n)
        A = A.reshape(1, A.shape[0])
    X, y = A[:, :-1], A[:, -1]
    if len(X.shape) == 1:  # change x size()=[n,] to size()=[n,1]
        X = X.reshape(X.shape[0], 1)
    if len(y.shape) == 1:  # change y size()=[n,] to size()=[n,1]
        y = y.reshape(y.shape[0], 1)
    return X, y


def nCk(n: int, k: int, as_int: bool = False):
    """
    :param n:
    :param k:
    :param as_int:
    :return: if as_int True: the result of nCk, else the combinations of nCk
    n choose k
    see nCk_test()
    """
    range_list = np.arange(0, n, 1)
    combs = list(combinations(range_list, k))
    combs = [list(comb) for comb in combs]
    if as_int:
        combs = len(combs)
    return combs


def redirect_std_start() -> (io.TextIOWrapper, io.StringIO):
    """
    redirect all prints to summary_str
    :return:
        io.TextIOWrapper - to revert back the prints to sys.stdout
        io.StringIO - to extract output
    see redirect_std_test()
    """
    old_stdout = sys.stdout
    sys.stdout = summary_str = io.StringIO()
    return old_stdout, summary_str


def redirect_std_finish(old_stdout: io.TextIOWrapper, summary_str: io.StringIO) -> str:
    """
    :param old_stdout: to revert back the prints to sys.stdout
    :param summary_str: to extract output
    :return:
    redirect all prints back to std out and return a string of what was captured"
    see redirect_std_test()
    """
    sys.stdout = old_stdout
    return summary_str.getvalue()


def get_line_number(depth: int = 1, ack: bool = False, tabs: int = 1) -> str:
    """
    :param depth:
    :param ack:
    :param tabs:
    :return:
    see get_line_number_test()
    """
    ret_val = ''
    try:
        scope_1_back = inspect.stack()[depth]  # stack()[0] is this function
        ret_val = '{}'.format(scope_1_back.lineno)
        if ack:
            print('{}Line {}:'.format(tabs * '\t', ret_val))
    except IndexError as e:
        exception_error(e)
    return ret_val


def get_function_name(depth: int = 1, ack: bool = False, tabs: int = 1) -> str:
    """
    :param depth:
    :param ack:
    :param tabs:
    :return:
    see
    """
    ret_val = ''
    try:
        scope_1_back = inspect.stack()[depth]  # stack()[0] is this function
        ret_val = '{}'.format(scope_1_back.function)
        if ack:
            print('{}{}:'.format(tabs * '\t', ret_val))
    except IndexError as e:
        exception_error(e)
    return ret_val


def get_file_name(depth: int = 1, ack: bool = False, tabs: int = 1) -> str:
    """
    :param depth:
    :param ack:
    :param tabs:
    :return:
    see get_file_name_test()
    """
    ret_val = ''
    try:
        scope_1_back = inspect.stack()[depth]  # stack()[0] is this function
        ret_val = '{}'.format(scope_1_back.filename)
        if ack:
            print('{}{}:'.format(tabs * '\t', ret_val))
    except IndexError as e:
        exception_error(e)
    return ret_val


def get_base_file_name(depth: int = 1, ack: bool = False, tabs: int = 1) -> str:
    """
    :param depth:
    :param ack:
    :param tabs:
    :return:
    see get_base_file_name_test()
    """
    # +1 because of this function
    file_name = get_file_name(depth + 1)
    base_name = os.path.basename(file_name)
    if ack:
        print('{}{}:'.format(tabs * '\t', base_name))
    return base_name


def get_function_name_and_line(depth: int = 1, ack: bool = False, tabs: int = 1) -> str:
    """
    :param depth:
    :param ack:
    :param tabs:
    :return:
    see get_function_name_and_line_test()
    """
    # +1 because of this function
    ret_val = '{}::{}'.format(get_file_name(depth + 1), get_line_number(depth + 1))
    if ack:
        print('{}{}:'.format(tabs * '\t', ret_val))
    return ret_val


def get_base_file_and_function_name(depth: int = 1, ack: bool = False, tabs: int = 1) -> str:
    """
    :param depth:
    :param ack:
    :param tabs:
    :return:
    see get_base_file_and_function_name_test()
    """
    # +1 because of this function
    ret_val = '{}::{}'.format(get_base_file_name(depth + 1), get_line_number(depth + 1))
    if ack:
        print('{}{}:'.format(tabs * '\t', ret_val))
    return ret_val


def add_color(
        string: str,
        op1: str = 'red',
        extra_ops: list = None,
) -> str:
    """
    :param string:
    :param op1: color, bg_color, bold, underline, reverse
    :param extra_ops: color, bg_color, bold, underline, reverse
    colors:
    * X = { blue(b), green(g), red(r), cyan(c), magenta(m), yellow(y) }
        for x in X: x, background_x, light_x, background_light_x
    * more colors:
        light_gray, background_light_gray, dark_gray, background_dark_gray
        black, background_black
        white, background_white

    special options:
    * bold(bo), underlined(un), reverse(re)

    to see all colors and options:
        for k, v in wu.CONST_COLOR_MAP.items():
            print('{}{}{}'.format(v, k, wu.CONST_COLOR_MAP['reset_all']))
    see add_color_test()
    """
    out_string = string
    # first to lower and check shortcuts
    op1 = op1.lower()
    if op1 in CONST_COLOR_SHORTCUTS:
        op1 = CONST_COLOR_SHORTCUTS[op1]

    if extra_ops is not None:
        for i in range(len(extra_ops)):
            extra_ops[i] = extra_ops[i].lower()
            if extra_ops[i] in CONST_COLOR_SHORTCUTS:
                extra_ops[i] = CONST_COLOR_SHORTCUTS[extra_ops[i]]

    # second build str with color tags
    if op1 in CONST_COLOR_MAP:
        # concat (color, string, reset tag)
        out_string = CONST_COLOR_MAP[op1]
        if extra_ops is not None:
            for op in extra_ops:
                if op in CONST_COLOR_MAP:
                    out_string += CONST_COLOR_MAP[op]
        out_string += '{}{}'.format(string, CONST_COLOR_MAP['reset_all'])
    return out_string


# noinspection PyTypeChecker
def init_logger(logger_path: str = './log.txt') -> io.TextIOWrapper:
    """
    :param: logger_path
    :return: logger obj
    see logger_test()
    """
    global logger
    logger = open(file=logger_path, mode='w', encoding='utf-8')
    return logger


def flush_logger() -> None:
    """
    good for loops - writes every iteration if used
    see logger_test()
    """
    global logger
    if logger is not None:
        logger.flush()
    return


def log_print(line: str, tabs: int = 0) -> None:
    """
    :param line:
    :param tabs:
    :return:
    see logger_test()
    """
    global logger
    print('{}{}'.format(tabs * '\t', line))
    if logger is not None:
        logger.write('{}{}\n'.format(tabs * '\t', line))
    return


def log_print_dict(my_dict, tabs: int = 1) -> None:
    """
    :param my_dict:
    :param tabs:
    :return:
    see logger_test()
    """
    for k, v in my_dict.items():
        log_print('{}{}: {}'.format(tabs * '\t', k, v))
    return


def close_logger() -> None:
    """
    :return:
    see logger_test()
    """
    global logger
    if logger is not None:
        logger.close()
    return


def create_dir(dir_path: str, ack: bool = True, tabs: int = 1):
    """
    :param dir_path:
    :param ack:
    :param tabs:
    :return:
    see create_and_delete_dir_test()
    """

    if not os.path.exists(dir_path):
        try:
            os.mkdir(dir_path)
            if ack:
                print('{}{}'.format(tabs * '\t', CREATED.format(dir_path)))
        except OSError as e:
            exception_error(e)
    else:
        exception_error(EXISTS.format(dir_path), tabs=tabs)
    return


def delete_dir(dir_path: str, ack: bool = True, tabs: int = 1):
    """
    :param dir_path:
    :param ack:
    :param tabs:
    :return:
    see create_and_delete_dir_test()
    """
    if os.path.exists(dir_path):
        files_n = len(os.listdir(dir_path))
        if files_n > 0:
            err = '{} HAS {} FILES - use delete_dir_with_files()'.format(dir_path, files_n)
            exception_error(err, tabs=tabs)
        else:
            try:
                os.rmdir(dir_path)
                if ack:
                    print('{}{}'.format(tabs * '\t', DELETED.format(dir_path)))
            except OSError as e:
                exception_error(e)
    else:
        exception_error(NOT_FOUND.format(dir_path), tabs=tabs)
    return


def delete_dir_with_files(dir_path: str, ack: bool = True, tabs: int = 1):
    """
    :param dir_path:
    :param ack:
    :param tabs:
    :return:
    see create_and_delete_dir_test()
    """
    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        try:
            shutil.rmtree(dir_path)
            status = '({} files - {})'.format(len(files), files)
            if ack:
                print('{}{} - {}'.format(tabs * '\t', DELETED.format(dir_path), status))
        except OSError as e:
            exception_error(e)
    else:
        exception_error(NOT_FOUND.format(dir_path), tabs=tabs)
    return


def delete_file(file: str, ack: bool = True, tabs: int = 1) -> None:
    """
    :param file:
    :param ack:
    :param tabs:
    see delete_file_test()
    """
    if os.path.exists(file):
        os.remove(file)
        if ack:
            print('{}{} '.format(tabs * '\t', DELETED.format(file)))
    else:
        exception_error(NOT_FOUND.format(file), tabs=tabs)
    return


def delete_files(files: list, ack: bool = True, tabs: int = 1) -> None:
    """
    :param files:
    :param ack:
    :param tabs:
    :return:
    see delete_files_test()
    """
    for file in files:
        delete_file(file, ack=False, tabs=tabs)
    if ack:
        print('{}{} '.format(tabs * '\t', DELETED.format(files)))
    return


def sleep(seconds: (int, float), ack: bool = False, tabs: int = 1):
    """
    :param seconds:
    :param ack:
    :param tabs:
    :return:
    see sleep_test()
    """
    if ack:
        print('{}Sleeping {} seconds'.format(tabs * '\t', seconds))
    time.sleep(seconds)
    return


def reverse_tuple_or_list(orig: [tuple, list]) -> [tuple, list]:
    """
    :param orig: list or tuple
    :return: dst: reversed list or tuple
    see reverse_tuple_or_list_test()
    """
    dst = orig[::-1]
    return dst


def get_time_stamp(format_s: str = '%Y_%m_%d_%H_%M_%S') -> str:
    """
    :param format_s:
    examples:
    "%Y_%m_%d_%H_%M_%S_%f" >>> 2020_07_19_13_36_24_597247
    "%Y_%m_%d" >>> 2021_04_07
    :return:
    see get_time_stamp_test()
    """
    date_time_obj = datetime.datetime.now()
    timestamp_str = date_time_obj.strftime(format_s)
    return timestamp_str


def round_tuple(t: tuple, fp: int = 3, warn: bool = False):
    """
    :param t: tuple 1D of floats
    :param fp: float precision >=0
    :param warn: if to should warning in case of rounding failure(e.g. string in list)
    :return: new_t: rounded tuple
    """
    if fp >= 0:
        new_t = tuple(round_list(li=t, fp=fp, warn=warn))
    else:
        new_t = t
    return new_t


def round_list(li: (list, tuple), fp: int = 3, warn: bool = False):
    """
    :param li: list or tuple 1D of floats
    :param fp: float precision >= 0
    :param warn: if to should warning in case of rounding failure(e.g. string in list)
    :return: new_li: rounded list
    see round_list_test()
    """
    new_li = li
    if fp >= 0:
        try:
            new_np = np.array(li)
            if np.dtype == np.float64 or np.dtype == np.float32 or np.float:
                new_li = np.around(new_np, fp).tolist()
        except TypeError as e:
            if warn:
                exception_error(e)
    return new_li


def shuffle_np_array(arr: np.array) -> np.array:
    """
    :param arr:
    :return:
    shuffles an array
    see shuffle_np_array_test()
    """
    if isinstance(arr, np.ndarray):
        arr = arr[np.random.permutation(arr.shape[0])]
    return arr


def shuffle_np_arrays(arr_tuple: tuple) -> tuple:
    """
    :param arr_tuple: tuple of arrays (numpy)
        len(arr) is equal on all arrays
    :return: shuffled arrays

    see shuffle_np_arrays_test()
    """
    arrays_size = len(arr_tuple[0])
    rand_perm = np.random.permutation(arrays_size)

    out_tuple = ()
    for arr in arr_tuple:
        arr_shf = arr[rand_perm]
        out_tuple += (arr_shf,)
    return out_tuple


def array_info_print(
        array: np.array,
        title: str = 'var',
        chars: (int, str) = 100,
        fp: (int, None) = 2,
        wm: bool = True,
        rec: bool = False,
        tabs: int = 1
) -> None:
    """
    :param array: (recommended 1d)
    :param title:
    :param chars:
    :param fp:
    :param wm:
    :param rec:
    :param tabs:
    :return:
    prints to_str and then mean, std and sum
    see array_info_print_test()
    """
    print(to_str(var=array, title='{}{}'.format(tabs * '\t', title), chars=chars, fp=fp, wm=wm, rec=rec))
    mean_s = 'mean={:,.%xf}' % fp
    mean_s = mean_s.format(np.mean(array))
    std_s = 'std={:,.%xf}' % fp
    std_s = std_s.format(np.std(array))
    sum_s = 'sum={:,.%xf}' % fp
    sum_s = sum_s.format(np.sum(array))
    print('{}\t{}, {}, {}'.format(tabs * '\t', mean_s, std_s, sum_s))
    return


def get_key_by_value(d: dict, value: any) -> str:
    """
    :param d: dict
    :param value:
    Notice that it will return the first key of the value given. if value not unique...
    :return: the key of the value
    see get_key_by_value_test()
    """
    key = None
    for k, v in d.items():
        if v == value:
            key = k
            break
    return key


def to_hex(num: int) -> str:
    """
    :param num:
    :return:
    convert decimal to hex as str
    see to_hex_and_bin_test()
    """
    string = '{:X}'.format(num)
    return string


def to_bin(num: int) -> str:
    """
    :param num:
    :return:
    convert decimal to bin as str
    see to_hex_and_bin_test()
    """
    string = '{:b}'.format(num)
    return string


def dict_as_table(table: dict, title: str = 'table', str_s: int = 10, fp: int = 2, tabs: int = 1):
    """
    :param table:
    :param title:
    :param str_s: k or v string length
    :param fp: if v is number - float precision
    :param tabs:
    :return:
    see dict_as_table_test()
    """
    print('{}{}:'.format(tabs * '\t', title))
    s_format = '{}\t{:%d}  ==> {:%d}' % (str_s, str_s)
    s_format_to_num = '{}\t{:%d}  ==> {:%d,}' % (str_s, str_s)
    for k, v in table.items():
        if is_int(v) or is_float(v):
            print(s_format_to_num.format(tabs * '\t', k, round(v, fp)))
        else:
            print(s_format.format(tabs * '\t', k, v))
    return


def is_same_type(container: (list, tuple)) -> bool:
    """
    :param container:
    :return:
    check if all items in list or tuple are of the same type
    """
    same_type = True
    if len(container) > 0:
        it = iter(container)
        first_type = type(next(it))
        # for item in container:
        #     print(type(item))
        same_type = all((type(x) is first_type) for x in it)
    return same_type


def convert_size(size_bytes: int) -> str:
    """
    :param size_bytes:
    :return:
    get size in bytes and return string e.g. '241.19 MB'
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def hard_disc(one_liner: bool = False, tabs: int = 1):
    """
    :param one_liner: per partition
    :param tabs:
    :return:
    see hard_disc_test()
    """
    partitions = psutil.disk_partitions()

    if one_liner:
        string = '{}'.format(tabs * '\t')
        for i, partition in enumerate(partitions):
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                string_device = '{}: Total {}, Used {}({:.2f}%), Free {}'.format(
                    partition.device.replace(':\\', ''),
                    convert_size(partition_usage.total),
                    convert_size(partition_usage.used),
                    partition_usage.percent,
                    convert_size(partition_usage.free),
                )
            except PermissionError as e:
                string_device = add_color('{}: PermissionError: {}'.format(partition.device.replace(':\\', ''), e))

            string += string_device
            if i < (len(partitions) - 1):
                string += ', '
    else:
        string = '{}disk space:'.format(tabs * '\t')
        for i, partition in enumerate(partitions):
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                string_device = '\n{}\t{}:'.format(tabs * '\t', partition.device.replace(':\\', ''))
                string_device += '\n{}\t\tTotal {}'.format(tabs * '\t', convert_size(partition_usage.total))
                string_device += '\n{}\t\tUsed {}({:.2f}%)'.format(tabs * '\t', partition_usage.used,
                                                                   partition_usage.percent)
                string_device += '\n{}\t\tFree {}'.format(tabs * '\t', convert_size(partition_usage.free))
            except PermissionError as e:
                string_device = '\n{}\t{}:'.format(tabs * '\t', partition.device.replace(':\\', ''))
                string_device += add_color('\n{}\t\tPermissionError: {}'.format(tabs * '\t', e))

            string += string_device
            if i < (len(partitions) - 1):
                string += ', '
    return string


def ram_size(one_liner: bool = False, tabs: int = 1):
    """
    :param one_liner:
    :param tabs:
    :return:
    see ram_size_test()
    """
    mem = psutil.virtual_memory()
    if one_liner:
        string = '{}Total {}, Used {}({}%), Available {} '.format(
            tabs * '\t',
            convert_size(mem.total),
            convert_size(mem.used),
            mem.percent,
            convert_size(mem.available),
        )
    else:
        string = '{}RAM Info:'.format(tabs * '\t')
        string += '\n{}\tTotal {}'.format(tabs * '\t', convert_size(mem.total))
        string += '\n{}\tUsed {}({}%)'.format(tabs * '\t', convert_size(mem.used), mem.percent)
        string += '\n{}\tAvailable {}'.format(tabs * '\t', convert_size(mem.available))
    return string


def cpu_info(one_liner: bool = False, tabs: int = 1):
    """
    :param one_liner:
    :param tabs:
    :return:
    see cpu_info_test()
    """
    if one_liner:
        uname = platform.uname()
        cpufreq = psutil.cpu_freq()
        string = '{}'.format(tabs * '\t')
        string += '{}, '.format(uname.machine)
        string += 'Physical cores {}, '.format(psutil.cpu_count(logical=False))
        string += 'Total cores {}, '.format(psutil.cpu_count(logical=True))
        string += 'Frequency {:.2f}Mhz, '.format(cpufreq.current)
        string += 'CPU Usage {}%'.format(psutil.cpu_percent())
    else:
        string = add_color('{}Full cpu info - Not implemented yet'.format(tabs * '\t'))
    # print("=" * 40, "System Information", "=" * 40)
    # uname = platform.uname()
    # print(f"System: {uname.system}")
    # print(f"Node Name: {uname.node}")
    # print(f"Release: {uname.release}")
    # print(f"Version: {uname.version}")
    # print(f"Machine: {uname.machine}")
    # print(f"Processor: {uname.processor}")
    # # let's print CPU information
    # print("=" * 40, "CPU Info", "=" * 40)
    # # number of cores
    # print("Physical cores:", psutil.cpu_count(logical=False))
    # print("Total cores:", psutil.cpu_count(logical=True))
    # # CPU frequencies
    # cpufreq = psutil.cpu_freq()
    # print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    # print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    # print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # # CPU usage
    # print("CPU Usage Per Core:")
    # for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    #     print(f"Core {i}: {percentage}%")
    # print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    return string
