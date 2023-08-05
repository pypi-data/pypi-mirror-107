from wizzi_utils import misc_tools as mt  # misc tools
import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # removes tf informative messages
warnings.simplefilter(action='ignore', category=FutureWarning)  # remove tf future warnings
# noinspection PyPackageRequirements
import tensorflow as tf  # noqa E402


def get_tensorflow_version(ack: bool = False, tabs: int = 1) -> str:
    """
    :param ack:
    :param tabs:
    :return:
    see get_tensorflow_version_test()
    """
    # print(tf.__version__)
    # print(tf.VERSION)
    # print(tf.version.VERSION)
    string = mt.add_color('{}* TensorFlow Version {}'.format(tabs * '\t', tf.__version__), op1=mt.SUCCESS_C)
    string += mt.add_color(' - GPU detected ? ', op1=mt.SUCCESS_C)
    if gpu_detected():
        string += mt.add_color('True', op1=mt.SUCCESS_C2[0], extra_ops=mt.SUCCESS_C2[1])
    else:
        string += mt.add_color('False', op1=mt.FAIL_C2[0], extra_ops=mt.FAIL_C2[1])
    if ack:
        print(string)
    return string


def gpu_detected() -> bool:
    """
    :return:
    """
    gpu_on = False
    try:
        # version >= 2
        if len(tf.config.list_physical_devices('GPU')) >= 1:
            gpu_on = True
    # except AttributeError as e:
    except AttributeError:
        # print(e)
        if 'GPU' in tf.test.gpu_device_name():
            gpu_on = True
    return gpu_on
