from wizzi_utils.socket import socket_tools as st
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.json import json_tools as jt
import socket
import os
import threading

SERVER_ADDRESS = ('localhost', 10000)
BUF_LEN = 20
END_MSG = "$#$#"


def connect_to_server():
    connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = SERVER_ADDRESS
    print("\tClientOutput:Connecting to server {}".format(server_address))
    try:
        connect_socket.connect(server_address)
        print('\t\tClientOutput:Connected to {}'.format(server_address))
    except ConnectionRefusedError:
        assert False, '\t\tClientOutput:No server is found on {}'.format(server_address)

    j_out = {'name': 'client', 'msg': 'hello', 'time': 'msg 1'}
    j_out_str = jt.json_to_string(j_out)

    st.send_msg(
        connection=connect_socket,
        buflen=BUF_LEN,
        data=j_out_str,
        msg_end=END_MSG
    )

    print(
        st.buffer_to_str(
            data=j_out_str,
            prefix='ClientOutput:OUT',
            tabs=2
        )
    )

    j_in_str = st.receive_msg(connect_socket, buflen=BUF_LEN, msg_end=END_MSG)
    if j_in_str:
        print(
            st.buffer_to_str(
                data=j_in_str,
                prefix='ClientOutput:IN',
                tabs=2
            )
        )

        j_out = {'name': 'client', 'msg': 'hello', 'time': 'msg 3'}
        j_out_str = jt.json_to_string(j_out)

        st.send_msg(
            connection=connect_socket,
            buflen=BUF_LEN,
            data=j_out_str,
            msg_end=END_MSG
        )

        print(
            st.buffer_to_str(
                data=j_out_str,
                prefix='ClientOutput:OUT',
                tabs=2
            )
        )
    else:
        print('\t\tClientOutput:No Data from {}'.format(connect_socket))
    return


def open_server_test():
    mt.get_function_name(ack=True, tabs=0)
    sock = st.open_server(
        server_address=SERVER_ADDRESS,
        ack=True,
        tabs=1
    )

    # OPEN WITH A DIFFERENT THREAD THE CLIENT
    thread = threading.Thread(target=connect_to_server)
    thread.start()

    print('\t\tWaiting for connection {}/{}:'.format(1, 1))
    client_sock, client_address = sock.accept()
    j_in_str = st.receive_msg(client_sock, buflen=BUF_LEN, msg_end=END_MSG)
    if j_in_str:
        print(
            st.buffer_to_str(
                data=j_in_str,
                prefix='IN',
                tabs=2
            )
        )

        j_out = {'name': 'server', 'msg': 'wait', 't': 'msg 2'}
        j_out_str = jt.json_to_string(j_out)
        st.send_msg(
            connection=client_sock,
            buflen=BUF_LEN,
            data=j_out_str,
            msg_end="$#$#"
        )
        print(
            st.buffer_to_str(
                data=j_out_str,
                prefix='OUT',
                tabs=2
            )
        )

        j_in_str = st.receive_msg(client_sock, buflen=BUF_LEN, msg_end=END_MSG)
        if j_in_str:
            print(
                st.buffer_to_str(
                    data=j_in_str,
                    prefix='IN',
                    tabs=2
                )
            )
        else:
            print('\t\tNo Data from {}'.format(client_address))

        # CLIENT is wait for more messages
        # when finished - close client connection

        print('\t\tTerminating connection...')
        client_sock.close()
    else:
        print('\t\tNo Data from {}'.format(client_address))
    return


def get_host_name_test():
    mt.get_function_name(ack=True, tabs=0)
    print('\t{}'.format(st.get_host_name()))
    return


def get_ipv4_test():
    mt.get_function_name(ack=True, tabs=0)
    print('\t{}'.format(st.get_ipv4()))
    return


def buffer_to_str_test():
    mt.get_function_name(ack=True, tabs=0)
    data = 'hi server, how you doing???'  # len(data)==27
    print(st.buffer_to_str(data, prefix='client1', tabs=1, max_chars=27))
    print(st.buffer_to_str(data, prefix='client1', tabs=1, max_chars=26))
    print(st.buffer_to_str(data, prefix='client1', tabs=1, max_chars=15))
    return


def rounds_summary_test():
    mt.get_function_name(ack=True, tabs=0)
    times_ti = []
    for t in range(10):
        print('\tt={}:'.format(t))
        begin_timer_i = mt.get_timer()
        # do_work of round t
        mt.sleep(seconds=0.03)
        end_timer_i = mt.get_timer()
        times_ti.append(end_timer_i - begin_timer_i)
        print('\t\tDONE round={}: total time={}'.format(t, mt.get_timer_delta(begin_timer_i, with_ms=True)))
    st.rounds_summary(times_ti, tabs=1)
    return


def download_file_test():
    mt.get_function_name(ack=True, tabs=0)
    img_url = 'https://cdn.sstatic.net/Sites/stackoverflow/img/logo.png'
    # img_url = "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
    dst_path = 'logo.png'

    mt.delete_file('./{}'.format(dst_path))
    st.download_file(img_url, dst_path='./{}'.format(dst_path))
    print('\t{} exists ? {}'.format(dst_path, os.path.exists('./{}'.format(dst_path))))

    st.download_file(img_url, dst_path='./{}'.format(dst_path))  # check no overwrite
    mt.delete_file('./{}'.format(dst_path))

    mt.create_dir('./a')
    st.download_file(img_url, dst_path='./a/{}'.format(dst_path))
    mt.delete_dir_with_files(dir_path='./a')
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    open_server_test()
    get_host_name_test()
    get_ipv4_test()
    buffer_to_str_test()
    rounds_summary_test()
    download_file_test()
    print('{}'.format('-' * 20))
    return
