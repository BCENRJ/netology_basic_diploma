from vk_get_pics import GetProfile, GetPhotos
from ya_disk_upload import YaUploader


# Simple validation func of vk url by splitting it and checking url name.
def is_valid_vk_url(url: str):
    url = url.lower().split('/')
    return True if url[0] == 'https:' and url[2] == 'vk.com' else (True if url[0] == 'vk.com' else False)


def start():
    print('Welcome To the Yandex Uploader for the VK User Profile Photos.\n')
    in_process = True
    while in_process:
        # Checking for the vk url by our validating function.
        vk_link = input('Please, send me link of the VK account page to get photos. '
                        '\n\033[1m(format: "https://vk.com/durov" or "vk.com/durov") '
                        'or "exit" to quit.\033[0m\nType/Paste: ')
        if is_valid_vk_url(vk_link):
            # Creating new instance of our object and using get_data method.
            obj_vk = GetProfile(vk_link)
            obj_vk.get_data()
            # In case we receive accessible url, we are going ahead.
            if obj_vk.uid is not None:
                ex = GetPhotos(obj_vk.uid, obj_vk.full_name)
                while True:
                    # Some ANSI usage for our input(typing).
                    album = input('Enter \033[1m1\033[0m for "profile" album '
                                  'or \033[1m2\033[0m for "wall" album to check. '
                                  'Or "Exit" to close app. \nType(1 or 2): ')
                    # Choosing album. Profile or Wall.
                    if album == '1' or album == '2':
                        while True:
                            data = ex.get_photos(album)
                            # Making sure that there is at least 1 photo in album.
                            if data != 0:
                                # Selection for in between given photo range.
                                if data is not None:
                                    while True:
                                        ya_token = input('Please, send me Yandex Disc Token from Polygon '
                                                         'to upload selected numbers of photos. '
                                                         'Or "Exit" to close app. \nType: ')
                                        # Obtaining Yandex Polygon token from user_input.
                                        if ya_token.lower() != 'exit':
                                            obj_ya = YaUploader(f'OAuth {ya_token.strip()}')
                                            if obj_ya.check_ya_token:
                                                # Starting to upload.
                                                obj_ya.upload_file(data)
                                                # Method for creating json file in 'logs' folder (code dir.)
                                                obj_ya.get_logs()
                                                return print('\033[1mSuccessfully loaded.\033[0m')
                                            else:
                                                print('There is a problem with Yandex Access. '
                                                      '[Possible Error Codes]:'
                                                      '\nAuthorization, 400, 403, 404, 406, 429, 503')
                                        elif ya_token.lower() == 'exit':
                                            print('App is closed, bye.')
                                            return None
                                else:
                                    print('Out of photo available range or not numeric.'
                                          '(Please, type photo num in range of "green" indicator).')
                            else:
                                break
                    elif album.lower() == 'exit':
                        print('App is closed, bye.')
                        return None
                    else:
                        print('Incorrect album selection (1 or 2).')
        elif vk_link.lower() == 'exit':
            print('App is closed, bye.')
            return None
        else:
            print('\033[1mInvalid VK Page Link\033[0m')
            in_process = True


# Start Function Calling
start()







