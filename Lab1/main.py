import requests
import json
import os.path

from Lab1.token_const import token_vk, token_git

lab1_suffix = 'Lab1\\'


class JsonWork:
    @staticmethod
    def save(filename, json_dict):
        file = open(filename, 'w', encoding='utf-8')
        json_object = json.dumps(json_dict, indent=4, ensure_ascii=False)
        file.write(json_object)

    @staticmethod
    def choose(dict, required):
        i = 0
        for elem in dict:
            elem = {item: elem.get(item) for item in required}
            dict[i] = elem
            i += 1
        return dict

    @staticmethod
    def choose_not(dict, restricted):
        keys = list(dict[0].keys())
        for item in restricted:
            if item in keys:
                keys.remove(item)

        res_dict = JsonWork.choose(dict, keys)
        return res_dict


class Requestor:
    vk_filename_temp = lab1_suffix + 'temp_vk.json'
    vk_filename_res = lab1_suffix + 'vk_groups.json'
    git_filename_temp = lab1_suffix + 'temp_git.json'
    git_filename_res = lab1_suffix + 'git_repos.json'

    @staticmethod
    def json_get(request, headers, filename):
        if (len(headers) > 0):
            req = requests.get(request, headers=headers)
        else:
            req = requests.get(request)

        req_dict = req.json()
        JsonWork.save(filename, req_dict)
        print("Request sent: ", request)
        return req_dict

    @staticmethod
    def get_vk_groups(user_id='emperorar'):
        req_dict = {}
        # Выполнение запроса и сохранение ответа в файл, чтобы не повторять запрос
        if not os.path.exists(Requestor.vk_filename_temp):
            access_token = token_vk
            method_name = 'groups.get'

            req_body = 'https://api.vk.com/method/{}?user_ids={}&extended=1&access_token={}&v=5.199'.format(
                method_name, user_id, access_token)
            req_dict = Requestor.json_get(req_body, {}, Requestor.vk_filename_temp)
        else:
            file = open('{}\\{}'.format(os.getcwd(), Requestor.vk_filename_temp), 'r', encoding='utf-8')
            req_dict = json.load(file)

        # Формирование результирующего файла
        if "response" in req_dict:
            required = ["id", "name", "screen_name"]
            result_dict = req_dict["response"]["items"]

            JsonWork.choose(result_dict, required)

            JsonWork.save(Requestor.vk_filename_res, result_dict)
            print("Result for vk: {}.".format(result_dict))
        else:
            print("Error for vk: {}".format(req_dict))

    @staticmethod
    def get_git_repos(user_name='ArtemKorz1'):
        req_dict = []
        # Выполнение запроса и сохранение ответа в файл, чтобы не повторять запрос
        if not os.path.exists(Requestor.git_filename_temp):
            access_token = token_git

            req_body = 'https://api.github.com/search/repositories?q=user:{}'.format(user_name)
            req_dict = Requestor.json_get(req_body, {'Authorization': 'token {}'.format(access_token)}, Requestor.git_filename_temp)
        else:
            file = open('{}\\{}'.format(os.getcwd(), Requestor.git_filename_temp), 'r', encoding='utf-8')
            req_dict = json.load(file)

        # Формирование результирующего файла
        if len(req_dict) > 0 and "message" not in req_dict:
            required = ["id", "name", "full_name", "private"]
            result_dict = req_dict["items"]

            result_dict = JsonWork.choose(result_dict, required)

            JsonWork.save(Requestor.git_filename_res, result_dict)
            print("Result for git: {}.".format(result_dict))
        else:
            print("Error for git: {}".format(req_dict))
