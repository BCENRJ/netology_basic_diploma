import os
import json
import requests
from tqdm import tqdm


class YaUploader:
    # Asking for the Yandex Token for our object to initialize.
    def __init__(self, token):
        self.token = token
        self.__url = 'https://cloud-api.yandex.net/v1/disk/'
        self.__headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': self.token}
        self.__loaded_files = []

    # Getter stands to check self.token for its accessibility.
    @property
    def check_ya_token(self):
        return requests.get(url=self.__url, headers=self.__headers).status_code == 200

    # Creating Folder or if its exists just returning name of the folder.
    def create_folder(self, folder_name):
        params = {'path': folder_name}
        requests.put(url=self.__url + 'resources', headers=self.__headers, params=params)
        return folder_name

    # Checking for given folder`s files.
    def __check_folder(self, folder_name):
        resources = requests.get(url=self.__url + 'resources', headers=self.__headers,
                                 params={'path': f'{folder_name}', 'limit': 1000}).json()
        return tuple(elem['name'] for elem in resources['_embedded']['items'])

    # Calling to create folder with the name of object 'Full_Name_Album' then assigning the rest photo data by index.
    def upload_file(self, data):
        folder_name = self.create_folder(data[0])
        photos = data[1]

        # TQDM module stands for progress bar of our uploads.
        with tqdm(total=len(data[1]), colour='green', desc='Loading', ncols=100,
                  dynamic_ncols=True, unit='', ascii='•█') as bar:
            for photo in photos:
                # Name of the items in selected or created folder
                folder_items = self.__check_folder(folder_name)

                # If the same likes of the multiple photos then getting the date of photo-upload for photo_file name.
                if photo[2] in folder_items:
                    params = {'path': f'{folder_name}/{photo[0]}', 'url': photo[1][0]}
                    s = requests.post(url=self.__url + 'resources/upload', headers=self.__headers, params=params)
                    self.__recording_files(photo[0], photo[1][0], photo[1][1])
                    bar.update()
                else:
                    params = {'path': f'{folder_name}/{photo[2]}', 'url': photo[1][0]}
                    s = requests.post(url=self.__url + 'resources/upload',  headers=self.__headers, params=params)
                    self.__recording_files(photo[2], photo[1][0], photo[1][1])
                    bar.update()

    # Recording each photo uploaded details and adding to our private obj attribute.
    def __recording_files(self, file_name, url, size):
        file_type = url.split('?', 1)[0].split('.', maxsplit=3)[-1]
        outcome = {'file_name': f'{file_name}.{file_type}', 'size': f'{size}'}
        self.__loaded_files.append(outcome)

    # Checking for 'logs' folder or creating it then converting our data_info object to json file.
    def get_logs(self):
        path = os.getcwd() + '/logs'
        is_exist = os.path.exists(path)
        if not is_exist:
            os.makedirs(path)

        # Serializing json
        json_object = json.dumps(self.__loaded_files, indent=3)
        with open(f"logs/yandex_logs.json", "a") as file:
            file.write(json_object)
            file.write('\n')
