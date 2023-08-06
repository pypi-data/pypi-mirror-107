from wizzi_utils.google import google_tools as got
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.socket import socket_tools as st


def build_gh() -> got.google_handler:
    gh = got.google_handler(
        yaml_path='./GDrive2/settings.yaml',
        tabs=1,
        dir_color='reverse',
        file_color='light_blue',
        title_color=['underlined', 'light_yellow']

    )
    print(gh)
    return gh


def create_test_dir(gh: got.google_handler) -> str:
    print('Creating dir for testing:')
    new_dir_path = 'root/{}'.format(mtt.TEMP_FOLDER_NAME)  # new dir
    gh.create_dir(dst_full_path_on_drive=new_dir_path)
    return new_dir_path


def delete_test_dir(gh: got.google_handler, test_f: str) -> None:
    # delete dir for tests
    print('Deleting dir for testing:')
    gh.delete_empty_dir(full_path_on_drive=test_f)
    # gh.delete_dir_with_files(full_path_on_drive=new_dir_path)
    return


def list_all_files_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    gh.list_all_files()  # root
    gh.list_all_files(starting_dir=test_f)
    # gh.list_all_files(starting_dir='root/fake_dir')  # will fail
    if local_test:
        delete_test_dir(gh, test_f)
    return


def upload_delete_image_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    url = mtt.TEMP_IMAGE_URL
    st.download_file(url, mtt.TEMP_IMAGE_PATH)
    dst_full_path_on_drive = '{}/{}'.format(test_f, mtt.TEMP_IMAGE_NAME)  # new file
    gh.upload_file(dst_full_path_on_drive=dst_full_path_on_drive, local_file_path=mtt.TEMP_IMAGE_PATH)
    gh.delete_file(full_path_on_drive=dst_full_path_on_drive)
    mt.delete_file(mtt.TEMP_IMAGE_PATH)
    if local_test:
        delete_test_dir(gh, test_f)
    return


def upload_download_delete_file_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    mtt.create_demo_file(mtt.TEMP_TXT_PATH)
    dst_full_path_on_drive = '{}/{}'.format(test_f, mtt.TEMP_TXT_NAME)  # new file

    gh.upload_file(dst_full_path_on_drive=dst_full_path_on_drive, local_file_path=mtt.TEMP_TXT_PATH)
    # gh.upload_file(dst_full_path_on_drive=dst_full_path_on_drive, local_file_path=mtt.TEMP_TXT_PATH)  # will fail
    mt.delete_file(mtt.TEMP_TXT_PATH)

    gh.download_file(full_path_on_drive=dst_full_path_on_drive, local_save_path=mtt.TEMP_TXT_PATH)
    mt.delete_file(mtt.TEMP_TXT_PATH)

    gh.delete_file(full_path_on_drive=dst_full_path_on_drive)
    # gh.delete_file(full_path_on_drive=dst_full_path_on_drive)  # will fail
    if local_test:
        delete_test_dir(gh, test_f)
    return


def upload_read_download_delete_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    dst_full_path_on_drive = '{}/{}'.format(test_f, mtt.TEMP_TXT_NAME)  # new file

    content_txt = '\t\thello world'
    content_txt += '\n\t\tnew server ip is 1.1.1.1:2000'
    gh.upload_content_to_new_file(dst_full_path_on_drive=dst_full_path_on_drive, content=content_txt)
    # try_again to see it fails due to duplicated name
    # gh.upload_content_to_new_file(dst_full_path_on_drive=dst_full_path_on_drive, content=content_txt)  # will fail

    # _ = gh.read_file(full_path_on_drive='{}/fake_file.txt'.format(test_f))  # fake file  # will fail
    test_txt_str = gh.read_file(full_path_on_drive=dst_full_path_on_drive)
    print('\tcontent:')
    print(test_txt_str)

    gh.download_file(full_path_on_drive=dst_full_path_on_drive, local_save_path=mtt.TEMP_TXT_PATH)
    mt.delete_file(mtt.TEMP_TXT_PATH)

    gh.delete_file(full_path_on_drive=dst_full_path_on_drive)
    if local_test:
        delete_test_dir(gh, test_f)
    return


def create_and_delete_empty_dir_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    dst_full_path_on_drive = '{}/{}'.format(test_f, mtt.TEMP_FOLDER_NAME)  # new dir
    gh.create_dir(dst_full_path_on_drive=dst_full_path_on_drive)
    gh.delete_empty_dir(full_path_on_drive=dst_full_path_on_drive)
    if local_test:
        delete_test_dir(gh, test_f)
    return


def create_and_delete_dir_with_files_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    dst_full_path_on_drive = '{}/{}'.format(test_f, mtt.TEMP_FOLDER_NAME)  # new dir
    gh.create_dir(dst_full_path_on_drive=dst_full_path_on_drive)
    new_file_dst = '{}/{}'.format(dst_full_path_on_drive, mtt.TEMP_TXT_NAME)
    gh.upload_content_to_new_file(dst_full_path_on_drive=new_file_dst, content='\t\thello world')
    gh.list_all_files(starting_dir=dst_full_path_on_drive)
    gh.delete_dir_with_files(full_path_on_drive=dst_full_path_on_drive)
    if local_test:
        delete_test_dir(gh, test_f)
    return


def download_dir_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    print('\tuploading some files for the test:')
    new_dir = '{}/{}'.format(test_f, mtt.TEMP_FOLDER_NAME)  # new dir
    gh.create_dir(dst_full_path_on_drive=new_dir, tabs=2)
    new_file_dst = '{}/{}'.format(new_dir, mtt.TEMP_TXT_NAME)
    new_file_dst2 = '{}/v2_{}'.format(new_dir, mtt.TEMP_TXT_NAME)
    gh.upload_content_to_new_file(dst_full_path_on_drive=new_file_dst, content='\t\thello world', tabs=3)
    gh.upload_content_to_new_file(dst_full_path_on_drive=new_file_dst2, content='\t\thello world', tabs=3)
    inner_dir = '{}/{}'.format(new_dir, mtt.TEMP_FOLDER_NAME)  # new dir 2
    gh.create_dir(dst_full_path_on_drive=inner_dir, tabs=3)
    new_file_dst3 = '{}/{}'.format(inner_dir, mtt.TEMP_TXT_NAME)
    gh.upload_content_to_new_file(dst_full_path_on_drive=new_file_dst3, content='\t\thello world', tabs=4)
    gh.list_all_files(starting_dir=new_dir)

    # existing dir will fail
    # mt.create_dir(dir_path=mtt.TEMP_FOLDER_NAME)
    # gh.download_dir(full_path_on_drive=new_dir, local_dir_name=mtt.TEMP_FOLDER_NAME)
    # mt.delete_empty_dir(dir_path=mtt.TEMP_FOLDER_NAME)

    gh.download_dir(full_path_on_drive=new_dir, local_dir_name=mtt.TEMP_FOLDER_NAME)
    gh.delete_dir_with_files(full_path_on_drive=new_dir)
    mt.delete_dir_with_files(mtt.TEMP_FOLDER_NAME)
    if local_test:
        delete_test_dir(gh, test_f)
    return


def upload_dir_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    print('\tcreating some local files for the test:')
    new_dir = mtt.TEMP_FOLDER_NAME
    mt.create_dir(dir_path=new_dir, tabs=2)
    mtt.create_demo_file('{}/{}'.format(new_dir, mtt.TEMP_TXT_NAME), tabs=3)
    mtt.create_demo_file('{}/v2_{}'.format(new_dir, mtt.TEMP_TXT_NAME), tabs=3)
    inner_dir = '{}/{}'.format(new_dir, mtt.TEMP_FOLDER_NAME)  # new dir 2
    mt.create_dir(inner_dir, tabs=3)
    mtt.create_demo_file('{}/{}'.format(inner_dir, mtt.TEMP_TXT_NAME), tabs=4)

    # gh.upload_dir(dst_full_path_on_drive=test_f, local_dir_name=mtt.TEMP_FAKE_PATH)  # will fail
    gh.upload_dir(dst_full_path_on_drive='{}/{}'.format(test_f, new_dir), local_dir_name=new_dir, tabs=1)
    gh.delete_dir_with_files(full_path_on_drive='{}/{}'.format(test_f, new_dir))
    mt.delete_dir_with_files(dir_path=new_dir)
    if local_test:
        delete_test_dir(gh, test_f)
    return


def rename_file_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    new_file_dst = '{}/{}'.format(test_f, mtt.TEMP_TXT_NAME)
    gh.upload_content_to_new_file(dst_full_path_on_drive=new_file_dst, content='\t\thello world')
    gh.list_all_files(starting_dir=test_f)
    new_name = 'v2_{}'.format(mtt.TEMP_TXT_NAME)
    gh.rename_file(file_full_path_on_drive=new_file_dst, new_name=new_name)
    gh.list_all_files(starting_dir=test_f)

    # try again - will fail
    # gh.upload_content_to_new_file(dst_full_path_on_drive=new_file_dst, content='\t\thello world')
    # gh.rename_file(file_full_path_on_drive=new_file_dst, new_name=new_name)
    # gh.delete_file(full_path_on_drive=new_file_dst)

    gh.delete_file(full_path_on_drive='{}/{}'.format(test_f, new_name))
    if local_test:
        delete_test_dir(gh, test_f)
    return


def update_file_content_test(gh: got.google_handler = None, test_f: str = None):
    mt.get_function_name(ack=True, tabs=0)
    local_test = False
    if gh is None:
        gh = build_gh()
        test_f = create_test_dir(gh)
        local_test = True
    new_file_dst = '{}/{}'.format(test_f, mtt.TEMP_TXT_NAME)
    gh.upload_content_to_new_file(dst_full_path_on_drive=new_file_dst, content='\t\thello world')
    content = gh.read_file(new_file_dst)
    print(content)
    gh.update_file_content(file_full_path_on_drive=new_file_dst, new_content='\t\tgoodbye world')
    new_content = gh.read_file(new_file_dst)
    print(new_content)
    gh.delete_file(full_path_on_drive=new_file_dst)
    if local_test:
        delete_test_dir(gh, test_f)
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    mt.get_function_name(ack=True, tabs=0)
    gh = build_gh()
    new_dir_path = create_test_dir(gh)

    list_all_files_test(gh, test_f=new_dir_path)
    upload_download_delete_file_test(gh, test_f=new_dir_path)
    upload_delete_image_test(gh, test_f=new_dir_path)
    upload_read_download_delete_test(gh, test_f=new_dir_path)
    create_and_delete_empty_dir_test(gh, test_f=new_dir_path)
    create_and_delete_dir_with_files_test(gh, test_f=new_dir_path)
    download_dir_test(gh, test_f=new_dir_path)
    upload_dir_test(gh, test_f=new_dir_path)
    rename_file_test(gh, test_f=new_dir_path)
    update_file_content_test(gh, test_f=new_dir_path)

    delete_test_dir(gh, new_dir_path)
    print('{}'.format('-' * 20))
    return
