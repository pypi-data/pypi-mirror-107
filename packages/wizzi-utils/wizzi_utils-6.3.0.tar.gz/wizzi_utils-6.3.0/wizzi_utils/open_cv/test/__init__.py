"""
:requires: cv2
:sub_package: wizzi_utils.pyplot
:sub_package: wizzi_utils.socket
"""
try:
    from wizzi_utils.open_cv.test.test_open_cv_tools import *
except ModuleNotFoundError as e:
    pass
