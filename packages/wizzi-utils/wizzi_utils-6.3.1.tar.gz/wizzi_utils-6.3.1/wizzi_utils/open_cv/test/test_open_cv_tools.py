from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.socket import socket_tools as st
from wizzi_utils.pyplot import pyplot_tools as pyplt
import numpy as np
import os
# noinspection PyPackageRequirements
import cv2


def load_img_from_web() -> np.array:
    url = 'https://cdn.sstatic.net/Sites/stackoverflow/img/logo.png'
    dst = './logo.png'
    if not os.path.exists(dst):
        success = st.download_file(url, dst)
        if not success:
            mt.exception_error('download failed - creating random img')
            img = mt.np_random_integers(size=(240, 320, 3), low=0, high=255)
            img = img.astype('uint8')
            cvt.save_img(dst, img)

    img = cvt.load_img(path=dst)
    return img


def get_cv_version_test():
    mt.get_function_name(ack=True, tabs=0)
    cvt.get_cv_version(ack=True, tabs=1)
    return


def imread_imwrite_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    path = './temp.png'
    cvt.save_img(path, img, ack=True)
    img_loaded = cvt.load_img(path, ack=True)
    print(mt.to_str(img_loaded, '\timg'))
    mt.delete_file(path, ack=True)
    mt.delete_file(file='./logo.png', ack=True)
    return


def list_to_cv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    img_list = img.tolist()
    print(mt.to_str(img_list, '\timg_list'))
    img = cvt.list_to_cv_image(img_list)
    print(mt.to_str(img, '\timg'))
    mt.delete_file(file='./logo.png', ack=True)
    return


def display_open_cv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    print('\tVisual test: stack overflow logo')
    loc = (70, 200)  # move to X,Y
    resize = 1.7  # enlarge to 170%
    cvt.display_open_cv_image(
        img=img,
        ms=1,  # not blocking
        title='stack overflow logo moved to {} and re-sized to {}'.format(loc, resize),
        loc=loc,  # start from x =70 y = 0
        resize=resize
    )
    loc = pyplt.Location.TOP_RIGHT.value  # move to top right corner
    resize = 1.7  # enlarge to 170%
    cvt.display_open_cv_image(
        img=img,
        ms=0,  # blocking
        title='stack overflow logo moved to {} and re-sized to {}'.format(loc, resize),
        loc=loc,  # start from x =70 y = 0
        resize=resize
    )
    cv2.destroyAllWindows()
    mt.delete_file(file='./logo.png', ack=True)
    return


def display_open_cv_image_loop_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    loc = (70, 200)  # move to X,Y
    resize = 1.7  # enlarge to 170%
    title = 'stack overflow logo moved to {} and re-sized to {} - 100 iterations'.format(loc, resize)
    print('\tVisual test: {}'.format(title))
    for i in range(100):
        cvt.display_open_cv_image(
            img=img,
            ms=1,  # not blocking
            title=title,
            loc=loc,  # start from x =70 y = 0
            resize=resize
        )
        if i == 0:  # move just first iter
            loc = None
    cv2.destroyAllWindows()
    mt.delete_file(file='./logo.png', ack=True)
    return


def resize_opencv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    print(mt.to_str(img, '\timg'))
    img = cvt.resize_opencv_image(img, scale_percent=0.6)
    print(mt.to_str(img, '\timg re-sized to 60%'))
    mt.delete_file(file='./logo.png', ack=True)
    return


def move_cv_img_x_y_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    options = [(0, 0), (100, 0), (0, 100), (150, 150), (400, 400), (250, 350)]
    print('\tVisual test: move to all options {}'.format(options))
    print('\t\tClick Esc to close all')
    for x_y in options:
        title = 'move to ({})'.format(x_y)
        cv2.imshow(title, img)
        cvt.move_cv_img_x_y(title, x_y)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    mt.delete_file(file='./logo.png', ack=True)
    return


def move_cv_img_by_str_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    options = [loc.value for loc in pyplt.Location]
    print('\tVisual test: move to all options {}'.format(options))
    print('\t\tClick Esc to close all')
    for where_to in options:
        title = 'move to {}'.format(where_to)
        cv2.imshow(title, img)
        cvt.move_cv_img_by_str(img, title, where=where_to)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    mt.delete_file(file='./logo.png', ack=True)
    return


def unpack_list_imgs_to_big_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    gray = cvt.BGR_img_to_gray(img)
    big_img = cvt.unpack_list_imgs_to_big_image(
        imgs=[img, gray, img],
        resize=None,
        grid=(2, 2)
    )
    title = 'stack overflow logo 2x2(1 empty)'
    print('\tVisual test: {}'.format(title))
    cvt.display_open_cv_image(
        img=big_img,
        ms=0,  # blocking
        title=title,
        loc=(0, 0),
        resize=None
    )
    cv2.destroyAllWindows()
    mt.delete_file(file='./logo.png', ack=True)
    return


def display_open_cv_images_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    title = '2x1 grid'
    print('\tVisual test: {}'.format(title))
    loc1 = (0, 0)
    cvt.display_open_cv_images(
        imgs=[img, img],
        ms=1,  # blocking
        title='{} loc={}'.format(title, loc1),
        loc=loc1,
        resize=None,
        grid=(2, 1)
    )
    loc2 = pyplt.Location.BOTTOM_CENTER.value
    cvt.display_open_cv_images(
        imgs=[img, img],
        ms=0,  # blocking
        title='{} loc={}'.format(title, loc2),
        loc=loc2,
        resize=None,
        grid=(2, 1)
    )
    cv2.destroyAllWindows()
    mt.delete_file(file='./logo.png', ack=True)
    return


def display_open_cv_images_loop_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    loc = (70, 200)  # move to X,Y
    title = 'stack overflow logo moved to {} - 100 iterations'.format(loc)
    print('\tVisual test: {}'.format(title))
    for i in range(100):
        cvt.display_open_cv_images(
            imgs=[img, img],
            ms=1,  # blocking
            title=title,
            loc=loc,
            resize=None,
            grid=(2, 1)
        )
        if i == 0:  # move just first iter
            loc = None
    cv2.destroyAllWindows()
    mt.delete_file(file='./logo.png', ack=True)
    return


def gray_to_BGR_and_back_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web()
    print(mt.to_str(img, '\timgRGB'))
    gray = cvt.BGR_img_to_gray(img)
    print(mt.to_str(img, '\timg_gray'))
    img = cvt.gray_scale_img_to_BGR_form(gray)
    print(mt.to_str(img, '\timgRGB'))
    mt.delete_file(file='./logo.png', ack=True)
    return


def BGR_img_to_RGB_and_back_test():
    mt.get_function_name(ack=True, tabs=0)
    imgBGR1 = load_img_from_web()
    print(mt.to_str(imgBGR1, '\timgBGR'))
    imgRGB = cvt.BGR_img_to_RGB(imgBGR1)
    print(mt.to_str(imgRGB, '\timgRGB'))
    imgBGR2 = cvt.RGB_img_to_BGR(imgRGB)
    print(mt.to_str(imgBGR2, '\timgBGR2'))

    cvt.display_open_cv_images(
        imgs=[imgBGR1, imgRGB, imgBGR2],
        ms=0,  # blocking
        title='imgBGR1, imgRGB, imgBGR2',
        loc=pyplt.Location.CENTER_CENTER,
        resize=None,
        grid=(3, 1)
    )
    cv2.destroyAllWindows()
    mt.delete_file(file='./logo.png', ack=True)
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    get_cv_version_test()
    imread_imwrite_test()
    list_to_cv_image_test()
    display_open_cv_image_test()
    display_open_cv_image_loop_test()
    resize_opencv_image_test()
    move_cv_img_x_y_test()
    move_cv_img_by_str_test()
    unpack_list_imgs_to_big_image_test()
    display_open_cv_images_test()
    display_open_cv_images_loop_test()
    gray_to_BGR_and_back_test()
    BGR_img_to_RGB_and_back_test()
    print('{}'.format('-' * 20))
    return
