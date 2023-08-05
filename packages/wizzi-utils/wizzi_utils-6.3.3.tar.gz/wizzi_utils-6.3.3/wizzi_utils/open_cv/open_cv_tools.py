import numpy as np
import math
import os
from wizzi_utils.pyplot import pyplot_tools as pyplt
from wizzi_utils.misc import misc_tools as mt
# noinspection PyPackageRequirements
import cv2


def get_cv_version(ack: bool = False, tabs: int = 1) -> str:
    """ see get_cv_version_test() """
    string = mt.add_color('{}* OpenCv Version {}'.format(tabs * '\t', cv2.getVersionString()), ops=mt.SUCCESS_C)
    if ack:
        print(string)
    return string


def load_img(path: str, ack: bool = True, tabs: int = 1) -> np.array:
    """ see imread_imwrite_test() """
    if os.path.exists(path):
        img = cv2.imread(path)
        if ack:
            print('{}{}'.format(tabs * '\t', mt.LOADED.format(path)))
    else:
        mt.exception_error(mt.NOT_FOUND.format(path), tabs=tabs)
        img = None
    return img


def save_img(path: str, img: np.array, ack: bool = True, tabs: int = 1) -> None:
    """ see imread_imwrite_test() """
    cv2.imwrite(path, img)
    if ack:
        print('{}{}'.format(tabs * '\t', mt.SAVED.format(path)))
    return


def list_to_cv_image(cv_img: [list, np.array]) -> np.array:
    """
    :param cv_img: numpy or list. if list: convert to numpy with dtype uint8
    :return: cv_img
    see list_to_cv_image_test()
    """
    if isinstance(cv_img, list):
        cv_img = np.array(cv_img, dtype='uint8')
    return cv_img


def display_open_cv_image(
        img: np.array,
        ms: int = 0,
        title: str = '',
        loc: (tuple, str) = (0, 0),
        resize: float = None
) -> None:
    """
    :param img: cv image in numpy array or list
    :param ms: 0 blocks, else time in milliseconds before image is closed
    :param title: window title
    :param loc: top left corner window location
        if tuple: x,y coordinates
        if str: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    :param resize: None for original size. else img_size *= resize (resize > 0)
    see display_open_cv_image_test()
    """
    img = list_to_cv_image(img)
    if resize is not None:
        img = resize_opencv_image(img, resize)
    cv2.imshow(title, img)
    if isinstance(loc, str):
        move_cv_img_by_str(img, title, where=loc)
    elif isinstance(loc, tuple):
        move_cv_img_x_y(title, x_y=loc)
    cv2.waitKey(ms)
    return


def resize_opencv_image(img: np.array, scale_percent: float):
    """
    :param img: cv img
    :param scale_percent: float>0(could be bigger than 1)
    img_size *= scale_percent
    see resize_opencv_image_test()
    """
    if scale_percent is None or scale_percent <= 0:
        resize_image = img
        mt.exception_error('illegal value for scale_percent={}'.format(scale_percent), tabs=0)
    else:
        width = math.ceil(img.shape[1] * scale_percent)
        height = math.ceil(img.shape[0] * scale_percent)
        dim = (width, height)
        resize_image = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resize_image


def move_cv_img_x_y(win_title: str, x_y: tuple) -> None:
    """
    :param win_title: cv img with win_title to be moved
    :param x_y: tuple of ints. x,y of top left corner
    Move cv img upper left corner to pixel (x, y)
    see move_cv_img_x_y_test()
    """
    cv2.moveWindow(win_title, x_y[0], x_y[1])
    return


def move_cv_img_by_str(img: np.array, win_title: str, where: str = pyplt.Location.TOP_LEFT.value) -> None:
    """
    :param img: to get the dims of the image
    :param win_title: cv img with win_title to be moved
    :param where: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    Move cv img upper left corner to pixel (x, y)
    see move_cv_img_by_str_test()
    """
    try:
        window_w, window_h = pyplt.screen_dims()  # screen dims in pixels
        if window_w != -1 and window_h != -1:
            fig_w, fig_h = img.shape[1], img.shape[0]
            task_bar_offset = 75  # about 75 pixels due to task bar

            x, y = 0, 0  # Location.TOP_LEFT.value: default
            if where == pyplt.Location.TOP_CENTER.value:
                x = (window_w - fig_w) / 2
                y = 0
            elif where == pyplt.Location.TOP_RIGHT.value:
                x = window_w - fig_w
                y = 0
            elif where == pyplt.Location.CENTER_LEFT.value:
                x = 0
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.CENTER_CENTER.value:
                x = (window_w - fig_w) / 2
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.CENTER_RIGHT.value:
                x = window_w - fig_w
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.BOTTOM_LEFT.value:
                x = 0
                y = window_h - fig_h - task_bar_offset
            elif where == pyplt.Location.BOTTOM_CENTER.value:
                x = (window_w - fig_w) / 2
                y = window_h - fig_h - task_bar_offset
            elif where == pyplt.Location.BOTTOM_RIGHT.value:
                x = window_w - fig_w
                y = window_h - fig_h - task_bar_offset
            x, y = int(x), int(y)
            move_cv_img_x_y(win_title, x_y=(x, y))
        else:
            move_cv_img_x_y(win_title, x_y=(0, 0))
    except (ValueError, Exception) as e:
        mt.exception_error(e)
        move_cv_img_x_y(win_title, x_y=(0, 0))
    return


def unpack_list_imgs_to_big_image(imgs: list, grid: tuple, resize: float = None) -> np.array:
    """
    :param imgs: list of cv images
    :param resize: resize factor
    :param grid: the layout you want as output
        (1,len(imgs)): 1 row
        (len(imgs),1): 1 col
        (2,2): 2x2 grid - supports len(imgs)<=4 but not more
    see unpack_list_imgs_to_big_image_test()
    """
    for i in range(len(imgs)):
        imgs[i] = list_to_cv_image(imgs[i])
        if resize is not None:
            imgs[i] = resize_opencv_image(imgs[i], resize)
        if len(imgs[i].shape) == 2:  # if gray - see as rgb
            imgs[i] = gray_scale_img_to_BGR_form(imgs[i])

    imgs_n = len(imgs)
    if imgs_n == 1:
        big_img = imgs[0]
    else:
        padding_bgr = list(pyplt.get_BGR_color('red'))
        height, width, cnls = imgs[0].shape
        rows, cols = grid
        big_img = np.zeros(shape=(height * rows, width * cols, cnls), dtype='uint8') + 255  # white big image

        row_ind, col_ind = 1, 1
        for i, img in enumerate(imgs):
            h_begin, h_end = height * (row_ind - 1), height * row_ind
            w_begin, w_end = width * (col_ind - 1), width * col_ind
            big_img[h_begin:h_end, w_begin:w_end, :] = img  # 0

            if rows > 1:  # draw bounding box on the edges. no need if there is 1 row or 1 col
                big_img[h_begin, w_begin:w_end, :] = padding_bgr
                big_img[h_end - 1, w_begin:w_end - 1, :] = padding_bgr
            if cols > 1:
                big_img[h_begin:h_end, w_begin, :] = padding_bgr
                big_img[h_begin:h_end, w_end - 1, :] = padding_bgr

            col_ind += 1
            if col_ind > cols:
                col_ind = 1
                row_ind += 1
    return big_img


def display_open_cv_images(
        imgs: list,
        ms: int = 0,
        title: str = '',
        loc: (tuple, str) = (0, 0),
        resize: float = None,
        grid: tuple = (1, 2)
) -> None:
    """
    :param imgs: list of RGB or gray scale images
    :param ms: 0 blocks, else time in milliseconds before image is closed
    :param title: window title
    :param loc: top left corner window location
        if tuple: x,y coordinates
        if str: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    :param resize: None for original size. else img_size *= resize (resize > 0)
    :param grid: size of rows and cols of the new image. e.g. (2,1) 2 rows with 1 img on each
        grid slots must be >= len(imgs)
    see display_open_cv_images_test()
    """
    imgs_n = len(imgs)
    if imgs_n > 0:
        total_slots = grid[0] * grid[1]
        assert imgs_n <= total_slots, 'grid has {} total_slots, but len(imgs)={}'.format(total_slots, imgs_n)
        big_img = unpack_list_imgs_to_big_image(imgs, grid=grid, resize=resize)
        display_open_cv_image(big_img, ms, title, loc, resize=None)
    return


def gray_scale_img_to_BGR_form(gray_img: np.array) -> np.array:
    """
    :param gray_img: from shape (x,y) - 1 channel (gray)
    e.g 480,640
    :return: RGB form image e.g 480,640,3. no real colors added - just shape as RGB
    see gray_to_BGR_and_back_test()
    """
    BGR_image = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    return BGR_image


def BGR_img_to_gray(bgr_img: np.array) -> np.array:
    """
    :param bgr_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: gray image e.g 480,640. colors are replaced to gray colors
    see gray_to_BGR_and_back_test()
    """
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    return gray


def BGR_img_to_RGB(bgr_img: np.array) -> np.array:
    """
    :param bgr_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: rgb image
    see BGR_img_to_RGB_and_back_test()
    """
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    return rgb_img


def RGB_img_to_BGR(rgb_img: np.array) -> np.array:
    """
    :param rgb_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: bgr image
    see BGR_img_to_RGB_and_back_test()
    """
    bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
    return bgr_img
