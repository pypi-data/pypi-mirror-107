"""
:requires: socket, threading
:sub_package: wizzi_utils.json
"""
try:
    from wizzi_utils.socket.test.test_socket_tools import *
except ModuleNotFoundError as e:
    pass
