"""
# package wizzi utils:
"""

__version__ = '6.3.1'
# __all__ = ['misc_tools']  # TODO future

# default package - available without extra namespace
from wizzi_utils.misc import *

# extra packages - available with extra namespace - requires extra modules
from wizzi_utils import algorithms as algs
from wizzi_utils import coreset as cot
from wizzi_utils import json as jt
from wizzi_utils import open_cv as cvt
from wizzi_utils import pyplot as pyplt
from wizzi_utils import socket as st
from wizzi_utils import torch as tt
from wizzi_utils import tensorflow as tft
from wizzi_utils import tflite as tflt


def test_all_modules():
    # misc package
    test.test_all()

    try:
        # algorithms package
        algs.test.test_all()
    except AttributeError as err:
        exception_error(err)

    try:
        # coreset package
        cot.test.test_all()
    except AttributeError as err:
        exception_error(err)

    try:
        # json package
        jt.test.test_all()
    except AttributeError as err:
        exception_error(err)

    try:
        # open_cv package
        cvt.test.test_all()
    except AttributeError as err:
        exception_error(err)

    try:
        # pyplot package
        pyplt.test.test_all()
    except AttributeError as err:
        exception_error(err)

    try:
        # socket package
        st.test.test_all()
    except AttributeError as err:
        exception_error(err)

    try:
        # torch package
        tt.test.test_all()
    except AttributeError as err:
        exception_error(err)

    try:
        # tensorflow package
        tft.test.test_all()
    except AttributeError as err:
        exception_error(err)

    try:
        # tflite package
        tflt.test.test_all()
    except AttributeError as err:
        exception_error(err)
    return
