import requests
from datetime import datetime


# Class for static usage of vk token by default, with url and default params.
class Head:
    url = 'https://api.vk.com/method/'
    token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    params = {'access_token': token, 'v': '5.131'}


# Class to check user-profile link and obtaining its ID.
class GetProfile:
    # Profile link and the rest 2 attributes like 'user_id' and 'full_name'.
    def __init__(self, page_link: str):
        self.__page_link = page_link.split('/')[-1]
        self.uid, self.full_name = None, None

    # Assigning 'user_id' and checking for profile activeness and accessibility.
    def get_data(self):
        data = requests.get(url=Head.url + 'users.get',
                            params={**Head.params, 'user_ids': self.__page_link}).json()
        # As the first request, checking that data received without errors.
        if 'error' not in data:
            # Getting user info.
            info = data['response'][0]
            # Assigning full name attributes.
            self.full_name = f"{info['first_name']}_{info['last_name']}"

            if 'deactivated' not in info:
                # If we have access or its 'True' then assign 'user_id'.
                if info['can_access_closed']:
                    self.uid = info['id']
                    print(f"{self.full_name}'s Profile Account ID\033[1m successfully\033[0m received.")
                else:
                    print(f"{self.full_name}'s Profile Account\033[1m is closed\033[0m "
                          f"(uploader works for only public accounts).")
            else:
                print(f"{self.full_name}'s Profile Account\033[1m is deactivated\033[0m (profile deleted or banned).")
        else:
            error_msg = data['error']['error_msg']
            print(f"\033[1m[Error]\033[0m {self.__page_link} is \033[1m{error_msg}\033[0m.")


# Class for downloading and distributing data.
class GetPhotos:
    # Only account_id and full_name is enough to get data(pics).
    def __init__(self, account_id: int, full_name: str):
        self.__acc_id = account_id
        self.__full_name = full_name

    # This methods stands for obtaining photos with the selection of both albums 'profile' or 'album'.
    def get_photos(self, album_num):
        # 1 command for profile and 2 for wall album.
        album = ('profile' if album_num == '1' else ('wall' if album_num == '2' else None))
        # Check if album 1 or 2.
        if album is not None:
            params = {'owner_id': self.__acc_id, 'rev': 1, 'album_id': {album},
                      'photo_sizes': 1, 'extended': '1', 'count': 1000}
            data = requests.get(url=Head.url + 'photos.get',
                                params={**Head.params, **params}).json()

            # As we get correct response for our request we are going ahead.
            if 'response' in data:
                num_of_pics = data['response']['count']
                # Counting and avoiding the problem if there is no any photos.
                if num_of_pics == 0:
                    print('No photos detected. (album with 0 photos).')
                    return 0
                # Choosing how many photos to download and some colors for our input by ANSI.
                select_photos = input(f"\033[1mIn total \033[34m{self.__full_name}'s "
                                      f"\033[92m'{num_of_pics}'\033[0;1m profile photos detected, how many pics upload"
                                      f" to your Yandex Disk ? \033[0m\nType(int): ")
                # Checking our input for its correctness.
                if select_photos.strip().isdigit() and int(select_photos.strip()) in range(1, num_of_pics + 1):
                    items = data['response']['items'][:int(select_photos)]

                    # Obtaining timestamp date and converting to utc.
                    outcome = [(datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d %H_%M'),
                                # Selecting max size value of photo.
                                max([(elem['url'], elem['type']) for elem in photo['sizes']],
                                    key=lambda size: dict(w=10, z=9, y=8, r=7, q=6, p=5, o=4, x=3, m=2, s=1)[size[1]]),
                                # Receiving likes of the each selected num of photo.
                                str(photo['likes']['count'])) for photo in items]
                    # Data collecting for template as (full_name_album,[date, (photo_url, size), number of likes]).
                    return f'{self.__full_name}_{album}', outcome
                else:
                    return None
            else:
                raise ConnectionError('Class GetPhotos Error')
        else:
            return None
