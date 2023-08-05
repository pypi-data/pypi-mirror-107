from wizzi_utils.misc import misc_tools as mt
import numpy as np


def timer_test():
    mt.get_function_name(ack=True, tabs=0)
    start_t = mt.get_timer()
    total = mt.get_timer_delta(s_timer=start_t, with_ms=True)
    total_full = mt.get_timer_delta(s_timer=start_t, with_ms=False)
    print('\tTotal run time {}'.format(total))
    print('\tTotal run time {}'.format(total_full))
    mt.get_timer_delta(s_timer=start_t, with_ms=False, ack=True, tabs=1)
    return


def timer_action_test():
    mt.get_function_name(ack=True, tabs=0)
    print('\ttimer count down example:')
    for i in range(1):
        mt.timer_action(seconds=2, action='take image {}'.format(i), tabs=2)
    # TODO restore after fixing open cv start minimized
    # print('\t press key example:')
    # mt.timer_action(seconds=None, action='taking an image', tabs=2)
    return


def get_current_date_hour_test():
    mt.get_function_name(ack=True, tabs=0)
    print('\tCurrent time is {}'.format(mt.get_current_date_hour()))
    mt.get_current_date_hour(ack=True, tabs=1)
    return


def get_pc_name_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_pc_name(ack=True, tabs=1)
    print('\tPc name is {}'.format(mt.get_pc_name()))
    return


def get_mac_address_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_mac_address(ack=True, tabs=1)
    mt.get_mac_address(with_colons=False, ack=True, tabs=1)
    print('\tMac address is {}'.format(mt.get_mac_address()))
    return


def get_cuda_version_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_cuda_version(ack=True, tabs=1)
    return


def get_env_variables_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_env_variables(ack=True, tabs=1)
    return


def set_env_variable_test():
    mt.get_function_name(ack=True, tabs=0)
    k = 'made_up_var'
    mt.set_env_variable(key=k, val='temp val', ack=True, tabs=1)
    print('\tCheck:')
    mt.get_env_variable(key=k, ack=True, tabs=2)
    mt.del_env_variable(key=k, ack=True, tabs=1)
    return


def get_env_variable_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_env_variable(key='made_up_var', ack=True, tabs=1)
    mt.get_env_variable(key='PATH', ack=True, tabs=1)
    return


def del_env_variable_test():
    mt.get_function_name(ack=True, tabs=0)
    k = 'made_up_var'
    mt.set_env_variable(key=k, val='temp val', ack=True, tabs=1)

    mt.del_env_variable(key=k, ack=True, tabs=1)
    mt.del_env_variable(key='made_up_var2', ack=True, tabs=1)
    return


def make_cuda_invisible_test():
    mt.get_function_name(ack=True, tabs=0)
    k = 'CUDA_VISIBLE_DEVICES'

    old_value = mt.get_env_variable(key=k)  # save old value
    mt.make_cuda_invisible()  # change to new value
    new_value = mt.get_env_variable(key=k)  # try get new value

    if new_value is not None:
        print('\t{} = {}'.format(k, new_value))
    else:
        print('\tTest Failed')

    # restore old value
    if old_value is None:
        mt.del_env_variable(key=k)  # didn't exist: delete it
    else:
        mt.set_env_variable(key=k, val=old_value)  # existed: restore value

    return


def profiler_test():
    mt.get_function_name(ack=True, tabs=0)
    pr = mt.start_profiler()
    mt.get_function_name(ack=False)
    profiler_str = mt.end_profiler(pr, rows=5, ack=True)
    print(profiler_str)
    return


def main_wrapper_test():
    def temp_function():
        print('hello_world')

    mt.get_function_name(ack=True, tabs=0)
    mt.main_wrapper(
        main_function=temp_function,
        seed=42,
        ipv4=True,
        cuda_off=False,
        torch_v=True,
        tf_v=True,
        cv2_v=True,
        with_profiler=False
    )
    return


def to_str_test():
    mt.get_function_name(ack=True, tabs=0)

    # INTS
    x = 1234
    print('\t{}'.format(mt.to_str(var=x)))  # minimal

    x = 12345678912345
    print(mt.to_str(var=x, title='\tvery long int'))

    # FLOATS
    f = 3.2
    print(mt.to_str(var=f, title='\tsmall float'))

    f = 3.2123123
    print(mt.to_str(var=f, title='\tlong float(rounded 4 digits)', fp=4))

    f = 1234567890.223123123123123123
    print(mt.to_str(var=f, title='\tbig long float(rounded 3 digits)', fp=3))

    s = 'hello world'
    print(mt.to_str(var=s, title='\tregular string'))

    s = ''
    print(mt.to_str(var=s, title='\tempty string'))

    # LISTS
    li = []
    print(mt.to_str(var=li, title='\tempty list'))

    li = [112312312, 3, 4]
    print(mt.to_str(var=li, title='\tlist of ints(recursive print)', rec=True))

    li = [112312312, 3, 4]
    print(mt.to_str(var=li, title='\tlist of ints(no metadata)', wm=False))

    li = [1, 3123123]
    print(mt.to_str(var=li, title='\t1d list of ints(no data)', chars=None))
    print(mt.to_str(var=li, title='\t1d list of ints(all data)', chars='all'))

    li = [1.0000012323, 3123123.22454875123123]
    print(mt.to_str(var=li, title='\t1d list(rounded 7 digits)', fp=7))

    li = [12, 1.2323, 'HI']
    print(mt.to_str(var=li, title='\t1d mixed list'))

    li = [4e-05, 6e-05, 4e-05, 5e-05, 4e-05, 7e-05, 2e-05, 7e-05, 5e-05, 8e-05]
    print(mt.to_str(var=li, title='\te-0 style', fp=6))

    li = [[4e-05, 6e-05, 4e-05, 5e-05, 4e-05, 7e-05, 2e-05, 7e-05, 5e-05, 8e-05]]
    print(mt.to_str(var=li, title='\t2d e-0 style', fp=6, rec=True))

    li = [11235] * 1000
    print(mt.to_str(var=li, title='\t1d long list'))

    li = [[1231.2123123, 15.9], [3.0, 7.55]]
    print(mt.to_str(var=li, title='\t2d list', rec=True))

    li = [(1231.2123123, 15.9), (3.0, 7.55)]
    print(mt.to_str(var=li, title='\t2d list of tuples', rec=True))

    # TUPLES
    t = (1239.123123, 3.12, 9.123123123123)
    print(mt.to_str(var=t, title='\t1d tuple', rec=True))

    # NUMPY
    ni = np.array([4e-05, 6e-02], dtype=float)
    print(mt.to_str(var=ni, title='\t1d np array', fp=2, rec=False))

    ni = np.array([1.0000012323, 3123123.22454875123123], dtype=float)
    print(mt.to_str(var=ni, title='\t1d np array', fp=2, rec=False))

    ni = np.array([[1231.123122, 15.9], [3.0, 7.55], [4e-05, 6e-02]])
    print(mt.to_str(var=ni, title='\t2d np array', rec=True))

    cv_img = np.zeros(shape=[480, 640, 3], dtype=np.uint8)
    print(mt.to_str(var=cv_img, title='\tcv_img', chars=20))

    # DICTS
    di = {'a': [1213, 2]}
    print(mt.to_str(var=di, title='\tdict of lists', rec=True))

    di = {'a': [{'k': [1, 2]}, {'c': [7, 2]}]}
    print(mt.to_str(var=di, title='\tnested dict', rec=True))
    return


def save_load_np_test():
    mt.get_function_name(ack=True, tabs=0)
    path = './a.npy'
    a = np.ones(shape=(2, 3, 29))
    print(mt.to_str(a, '\ta'))
    mt.save_np(a, path=path)
    a2 = mt.load_np(path, ack=True)
    print(mt.to_str(a2, '\ta2'))
    mt.delete_file(path, tabs=1)
    _ = mt.load_np('./no_such_file.np', ack=True)
    return


def save_load_npz_test():
    mt.get_function_name(ack=True, tabs=0)
    path = './b_c.npz'
    b = np.ones(shape=(2, 3, 29))
    c = np.ones(shape=(2, 3, 29))
    b_c = {'b': b, 'c': c}
    print(mt.to_str(b_c, '\tb_c'))
    mt.save_npz(b_c, path=path)
    b_c2 = mt.load_npz(path)
    print(mt.to_str(b_c2, '\tb_c2', rec=True))
    mt.delete_file(path)
    return


def save_load_pkl_test():
    mt.get_function_name(ack=True, tabs=0)
    path = './data.pkl'
    a = {'2': 'a', 'b': 9, 'x': np.ones(shape=3)}
    print(mt.to_str(a, '\ta'))
    mt.save_pkl(data_dict=a, path=path)
    a2 = mt.load_pkl(path=path)
    print(mt.to_str(a2, '\ta2'))
    mt.delete_file(path)
    return


def get_uniform_dist_by_dim_test():
    mt.get_function_name(ack=True, tabs=0)
    A = np.array([[1, 100], [7, 210], [3, 421]])
    lows, highs = mt.get_uniform_dist_by_dim(A)
    print(mt.to_str(A, '\tA'))
    print(mt.to_str(lows, '\tlows'))
    print(mt.to_str(highs, '\thighs'))
    A = A.tolist()
    print(mt.to_str(A, '\tA'))
    lows, highs = mt.get_uniform_dist_by_dim(A)
    print(mt.to_str(lows, '\tlows'))
    print(mt.to_str(highs, '\thighs'))
    A = mt.np_uniform(shape=(500, 2), lows=[3, 200], highs=[12, 681])
    print(mt.to_str(A, '\tA(lows=[3, 200],highs=[12, 681])'))
    lows, highs = mt.get_uniform_dist_by_dim(A)
    print(mt.to_str(lows, '\tlows'))
    print(mt.to_str(highs, '\thighs'))
    return


def get_normal_dist_by_dim_test():
    mt.get_function_name(ack=True, tabs=0)
    A = np.array([[1, 100], [7, 210], [3, 421]])
    means, stds = mt.get_normal_dist_by_dim(A)
    print(mt.to_str(A, '\tA'))
    print(mt.to_str(means, '\tmeans'))
    print(mt.to_str(stds, '\tstds'))
    A = A.tolist()
    print(mt.to_str(A, '\tA'))
    means, stds = mt.get_normal_dist_by_dim(A)
    print(mt.to_str(means, '\tmeans'))
    print(mt.to_str(stds, '\tstds'))
    A = mt.np_normal(shape=(500, 2), mius=[3, 200], stds=[12, 121])
    print(mt.to_str(A, '\tA(mius=[3, 200],stds=[12, 121])'))
    means, stds = mt.get_normal_dist_by_dim(A)
    print(mt.to_str(means, '\tmeans'))
    print(mt.to_str(stds, '\tstds'))
    return


def np_uniform_test():
    mt.get_function_name(ack=True, tabs=0)
    A = mt.np_uniform(shape=(500, 2), lows=[3, 200], highs=[12, 681])
    print(mt.to_str(A, '\tA(lows=[3, 200],highs=[12, 681])'))
    return


def np_normal_test():
    mt.get_function_name(ack=True, tabs=0)
    A = mt.np_normal(shape=(500, 2), mius=[3, 200], stds=[12, 121])
    print(mt.to_str(A, '\tA(mius=[3, 200],stds=[12, 121])'))
    return


def generate_new_data_from_old_test():
    mt.get_function_name(ack=True, tabs=0)
    print('\tgenerate uniform data example')
    old_data = mt.np_uniform(shape=(500, 2), lows=[3, 200], highs=[12, 681])
    print(mt.to_str(old_data, '\t\told_data(lows=[3, 200],highs=[12, 681])'))
    new_data = mt.generate_new_data_from_old(old_data, new_data_n=4000, dist='uniform')
    lows, highs = mt.get_uniform_dist_by_dim(new_data)
    print(mt.to_str(new_data, '\t\tnew_data'))
    print(mt.to_str(lows, '\t\tlows'))
    print(mt.to_str(highs, '\t\thighs'))

    print('\tgenerate normal data example')
    old_data = mt.np_normal(shape=(500, 2), mius=[3, 200], stds=[12, 121])
    print(mt.to_str(old_data, '\t\told_data(mius=[3, 200],stds=[12, 121])'))
    new_data = mt.generate_new_data_from_old(old_data, new_data_n=4000, dist='normal')
    means, stds = mt.get_normal_dist_by_dim(new_data)
    print(mt.to_str(new_data, '\t\tnew_data'))
    print(mt.to_str(means, '\t\tmeans'))
    print(mt.to_str(stds, '\t\tstds'))
    return


def np_random_integers_test():
    mt.get_function_name(ack=True, tabs=0)
    random_ints = mt.np_random_integers(low=5, high=20, size=(2, 3))
    print(mt.to_str(random_ints, '\trandom_ints from 5-20'))
    return


def augment_x_y_numpy_test():
    mt.get_function_name(ack=True, tabs=0)
    X = mt.np_random_integers(low=5, high=20, size=(10, 3))
    Y = mt.np_random_integers(low=0, high=10, size=(10,))
    print(mt.to_str(X, '\tX'))
    print(mt.to_str(Y, '\tY'))
    A = mt.augment_x_y_numpy(X, Y)
    print(mt.to_str(A, '\tA'))
    return


def de_augment_numpy_test():
    mt.get_function_name(ack=True, tabs=0)
    A = mt.np_random_integers(low=5, high=20, size=(10, 4))
    print(mt.to_str(A, '\tA'))
    X, Y = mt.de_augment_numpy(A)
    print(mt.to_str(X, '\tX'))
    print(mt.to_str(Y, '\tY'))
    return


def nCk_test():
    mt.get_function_name(ack=True, tabs=0)
    A = np.random.randint(low=-10, high=10, size=(3, 2))
    print(mt.to_str(A, '\tA'))

    # let's iterate on every 2 different indices of A
    combs_count = mt.nCk(len(A), k=2, as_int=True)
    print('\t{}C2={}:'.format(len(A), combs_count))  # result is 3

    combs_list = mt.nCk(len(A), k=2)  # result is [[0, 1], [0, 2], [1, 2]]
    for i, comb in enumerate(combs_list):
        print('\t\tcomb {}={}. A[comb]={}'.format(i, comb, A[comb].tolist()))
    return


def redirect_std_test():
    mt.get_function_name(ack=True, tabs=0)
    old_stdout, summary_str = mt.redirect_std_start()
    print('\t\tbla bla bla')
    print('\t\tline2')
    string = mt.redirect_std_finish(old_stdout, summary_str)
    print('\tcaptured output:')
    print(string, end='')  # there is '\n' at the end of the last line
    return


def get_line_number_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_line_number(ack=True)
    return


def get_function_name_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_function_name(ack=True)
    return


def get_file_name_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_file_name(ack=True)
    return


def get_base_file_name_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_base_file_name(ack=True)
    return


def get_function_name_and_line_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_function_name_and_line(ack=True)
    return


def get_base_file_and_function_name_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_base_file_and_function_name(ack=True)
    return


def add_color_test():
    mt.get_function_name(ack=True, tabs=0)
    print(mt.add_color(string='\tred ,bold and underlined', ops=['Red', 'bold', 'underlined']))
    print('\t{}'.format(mt.add_color(string='blue ,bold and underlined', ops=['BlUe', 'bo', 'un'])))
    print(mt.add_color(string='\tjust bold', ops='bold'))
    print(mt.add_color(string='\treverse color and bg color', ops='re'))
    print(mt.add_color(string='\tred with background_dark_gray', ops=['red', 'background_dark_gray']))
    print('\t{}'.format(mt.add_color(string='background_light_yellow', ops='background_light_yellow')))
    print(mt.add_color(string='\tblack and background_magenta', ops=['black', 'background_magenta']))
    my_str = 'using mt.to_str()'
    my_str = mt.to_str(var=my_str, title='\t{}'.format(my_str))
    print(mt.add_color(my_str, ops='Green'))
    return


def logger_test():
    mt.get_function_name(ack=True, tabs=0)
    path = './log_{}.txt'.format(mt.get_time_stamp())
    mt.init_logger(logger_path=path)
    mt.log_print(line='\tline 1')
    mt.flush_logger()
    mt.log_print(line='line 2', tabs=1)
    mt.log_print(line='line 3', tabs=3)
    mt.close_logger()

    print('\treading from {}'.format(path))
    file1 = open(path, 'r')
    Lines = file1.readlines()
    file1.close()
    for i, line in enumerate(Lines):
        print("\t\tLine{}: {}".format(i + 1, line.rstrip()))
    mt.delete_file(path)
    return


def create_and_delete_dir_test():
    mt.get_function_name(ack=True, tabs=0)
    path = 'TEMP_DIR1'
    mt.create_dir(dir_path=path)
    mt.delete_dir(dir_path=path)
    return


def create_and_delete_dir_with_files_test():
    mt.get_function_name(ack=True, tabs=0)
    path = 'TEMP_DIR2'
    mt.create_dir(dir_path=path)
    f1 = open(file='./{}/temp1.txt'.format(path), mode='w', encoding='utf-8')
    f1.close()
    f2 = open(file='./{}/temp2.txt'.format(path), mode='w', encoding='utf-8')
    f2.close()
    mt.delete_dir(dir_path=path)
    mt.delete_dir_with_files(dir_path=path)
    return


def delete_file_test():
    mt.get_function_name(ack=True, tabs=0)
    path = './temp.txt'
    f1 = open(file=path, mode='w', encoding='utf-8')
    f1.close()
    mt.delete_file(file=path)
    return


def delete_files_test():
    mt.get_function_name(ack=True, tabs=0)
    path1 = './temp1.txt'
    f1 = open(file=path1, mode='w', encoding='utf-8')
    f1.close()
    path2 = './temp2.txt'
    f2 = open(file=path2, mode='w', encoding='utf-8')
    f2.close()
    mt.delete_files(files=[path1, path2])
    return


def sleep_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.sleep(seconds=2, ack=True, tabs=1)
    return


def reverse_tuple_or_list_test():
    mt.get_function_name(ack=True, tabs=0)
    my_tuple = (0, 0, 255)
    print(mt.to_str(my_tuple, '\tmy_tuple'))
    print(mt.to_str(mt.reverse_tuple_or_list(my_tuple), '\tmy_tuple_reversed'))
    my_list = [0, 0, 255]
    print(mt.to_str(my_list, '\tmy_list'))
    print(mt.to_str(mt.reverse_tuple_or_list(my_list), '\tmy_list_reversed'))
    return


def get_time_stamp_test():
    mt.get_function_name(ack=True, tabs=0)
    print('\tdate no day: {}'.format(mt.get_time_stamp(format_s='%Y_%m')))
    print('\tdate: {}'.format(mt.get_time_stamp(format_s='%Y_%m_%d')))
    print('\ttime: {}'.format(mt.get_time_stamp(format_s='%H_%M_%S')))
    print('\tdate and time: {}'.format(mt.get_time_stamp(format_s='%Y_%m_%d_%H_%M_%S')))
    print('\tdate and time with ms: {}'.format(mt.get_time_stamp(format_s='%Y_%m_%d_%H_%M_%S_%f')))
    return


def round_list_test():
    mt.get_function_name(ack=True, tabs=0)
    li = [1.23123123, 12.123123123123123123, 1.2, 1.0]
    print(mt.to_str(var=li, title='\torigin', fp=None))
    print(mt.to_str(var=mt.round_list(li, fp=1), title='\tfp=1', fp=None))
    print(mt.to_str(var=mt.round_list(li, fp=3), title='\tfp=3', fp=None))
    l2 = [5e-05, 0.00014, 5e-10, 0.0001, 6e-07, 5e-05, 8e-05, 6e-05, 5e-05, 5e-05]
    print(mt.to_str(var=l2, title='\torigin', fp=None))
    print(mt.to_str(var=mt.round_list(l2, fp=5), title='\tfp=5', fp=None))
    l2 = ['x', 'y', 'z']
    print(mt.to_str(var=l2, title='\torigin', fp=None))
    print(mt.to_str(var=mt.round_list(l2, fp=5, warn=True), title='\tfp=5', fp=None))
    return


def round_tuple_test():
    mt.get_function_name(ack=True, tabs=0)
    li = (1.23123123, 12.123123123123123123, 1.2, 1.0)
    print(mt.to_str(var=li, title='\torigin', fp=None))
    print(mt.to_str(var=mt.round_tuple(li, fp=1), title='\tfp=1', fp=None))
    print(mt.to_str(var=mt.round_tuple(li, fp=3), title='\tfp=3', fp=None))
    l2 = (5e-05, 0.00014, 5e-10, 0.0001, 6e-07, 5e-05, 8e-05, 6e-05, 5e-05, 5e-05)
    print(mt.to_str(var=l2, title='\torigin', fp=None))
    print(mt.to_str(var=mt.round_tuple(l2, fp=5), title='\tfp=5', fp=None))
    l2 = ('x', 'y', 'z')
    print(mt.to_str(var=l2, title='\torigin', fp=None))
    print(mt.to_str(var=mt.round_tuple(l2, fp=5, warn=True), title='\tfp=5', fp=None))
    return


def shuffle_np_array_test():
    mt.get_function_name(ack=True, tabs=0)
    A = mt.np_normal(shape=(6,), mius=3.5, stds=10.2)
    print(mt.to_str(A, '\tA'))
    A = mt.shuffle_np_array(A)
    print(mt.to_str(A, '\tA'))
    return


def shuffle_np_arrays_test():
    mt.get_function_name(ack=True, tabs=0)
    A = np.array([1, 2, 3, 4, 5, 6])
    B = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]])
    print(mt.to_str(A, '\tA'))
    print(mt.to_str(B, '\tB'))
    A, B = mt.shuffle_np_arrays(
        arr_tuple=(A, B)
    )
    print(mt.to_str(A, '\tA'))
    print(mt.to_str(B, '\tB'))
    return


def array_info_print_test():
    B = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]])
    mt.array_info_print(B, 'B')
    return


def get_key_by_value_test():
    mt.get_function_name(ack=True, tabs=0)
    j = {"x": 3, "a": "dx"}
    print('\tfirst key that has value 3 is {}'.format(mt.get_key_by_value(j, value=3)))
    print('\tfirst key that has value "dx" is {}'.format(mt.get_key_by_value(j, value="dx")))
    return


def to_hex_and_bin_test():
    mt.get_function_name(ack=True, tabs=0)
    variable = 'no meaning to to content'
    print('\taddress of variable is 0d{}'.format(id(variable)))
    print('\taddress of variable is 0x{}'.format(mt.to_hex(id(variable))))
    print('\taddress of variable is 0b{}'.format(mt.to_bin(id(variable))))
    return


def dict_as_table_test():
    mt.get_function_name(ack=True, tabs=0)
    table = {'gilad': 3, 'a': 11233.1213, 'aasdasd': 9913123, 'b': 'hello'}
    # mt.dict_as_table(table=table, title='my table', str_s=5, tabs=1)
    # mt.dict_as_table(table=table, title='my table', str_s=7, tabs=1)
    mt.dict_as_table(table=table, title='my table', str_s=15, tabs=1)
    return


def is_same_type_test():
    mt.get_function_name(ack=True, tabs=0)
    li = ['s', 123, 'a', 'b']
    print('\tis li {} homogeneous ? {}'.format(li, mt.is_same_type(li)))
    li = ['s', 'a', 'b']
    print('\tis li {} homogeneous ? {}'.format(li, mt.is_same_type(li)))
    t = (1.2, 123, 12, 13)
    print('\tis t {} homogeneous ? {}'.format(t, mt.is_same_type(t)))
    t = (1, 123, 12, 13)
    print('\tis t {} homogeneous ? {}'.format(t, mt.is_same_type(t)))
    return


def hard_disc_test():
    mt.get_function_name(ack=True, tabs=0)
    print(mt.hard_disc(one_liner=True, tabs=1))
    print(mt.hard_disc(one_liner=False, tabs=1))
    return


def ram_size_test():
    mt.get_function_name(ack=True, tabs=0)
    print(mt.ram_size(one_liner=True, tabs=1))
    print(mt.ram_size(one_liner=False, tabs=1))
    return


def cpu_info_test():
    mt.get_function_name(ack=True, tabs=0)
    print(mt.cpu_info(one_liner=True, tabs=1))
    print(mt.cpu_info(one_liner=False, tabs=1))
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name(depth=1)))
    timer_test()
    timer_action_test()
    get_current_date_hour_test()
    get_pc_name_test()
    get_mac_address_test()
    get_cuda_version_test()
    get_env_variables_test()
    set_env_variable_test()
    get_env_variable_test()
    del_env_variable_test()
    make_cuda_invisible_test()
    profiler_test()
    main_wrapper_test()
    to_str_test()
    save_load_np_test()
    save_load_npz_test()
    save_load_pkl_test()
    get_uniform_dist_by_dim_test()
    get_normal_dist_by_dim_test()
    np_uniform_test()
    np_normal_test()
    generate_new_data_from_old_test()
    np_random_integers_test()
    augment_x_y_numpy_test()
    de_augment_numpy_test()
    nCk_test()
    redirect_std_test()
    get_line_number_test()
    get_function_name_test()
    get_file_name_test()
    get_base_file_name_test()
    get_function_name_and_line_test()
    get_base_file_and_function_name_test()
    add_color_test()
    logger_test()
    create_and_delete_dir_test()
    create_and_delete_dir_with_files_test()
    delete_file_test()
    delete_files_test()
    sleep_test()
    reverse_tuple_or_list_test()
    get_time_stamp_test()
    round_list_test()
    round_tuple_test()
    shuffle_np_array_test()
    shuffle_np_arrays_test()
    array_info_print_test()
    get_key_by_value_test()
    to_hex_and_bin_test()
    dict_as_table_test()
    is_same_type_test()
    hard_disc_test()
    ram_size_test()
    cpu_info_test()
    print('{}'.format('-' * 20))
    return
