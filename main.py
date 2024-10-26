import requests, json, os.path

vk_filename_temp = 'temp_vk.json'
vk_filename_res = 'vk_groups.json'
git_filename_temp = 'temp_git.json'
git_filename_res = 'git_repos.json'
token_vk = '<Мой access token>'
token_git = '<Мой classic token>'

def json_save(filename, json_dict):
    file = open(filename, 'w', encoding='utf-8')
    json_object = json.dumps(json_dict, indent=4, ensure_ascii=False)
    file.write(json_object)

def json_get(request, headers, filename):
    if (len(headers) > 0):
        req = requests.get(request, headers=headers)
    else:
        req = requests.get(request)

    req_dict = req.json()
    json_save(filename, req_dict)
    print("Request sent: ", request)
    return req_dict

def choose_from_json(dict, required):
    i = 0
    for elem in dict:
        elem = {item: elem.get(item) for item in required}
        dict[i] = elem
        i += 1
    return dict

def get_vk_groups():
    req_dict = {}
    #Выполнение запроса и сохранение ответа в файл, чтобы не повторять запрос
    if (not os.path.exists(vk_filename_temp)):
        access_token = token_vk
        method_name = 'groups.get'
        user_id = 'emperorar'

        req_body = 'https://api.vk.com/method/{}?user_ids={}&extended=1&access_token={}&v=5.199'.format(
            method_name, user_id, access_token)
        req_dict = json_get(req_body, {}, vk_filename_temp)
    else:
        file = open('{}\\{}'.format(os.getcwd(), vk_filename_temp), 'r', encoding='utf-8')
        req_dict = json.load(file)

    #Формирование результирующего файла
    if ("response" in req_dict):
        required = ["id", "name", "screen_name"]
        result_dict = req_dict["response"]["items"]

        choose_from_json(result_dict, required)

        json_save(vk_filename_res, result_dict)
        print("Result for vk: {}.".format(result_dict))
    else:
        print("Error for vk: {}".format(req_dict))

def get_git_repos():
    req_dict = []
    #Выполнение запроса и сохранение ответа в файл, чтобы не повторять запрос
    if (not os.path.exists(git_filename_temp)):
        access_token = token_git
        user_name = 'ArtemKorz1'

        req_body = 'https://api.github.com/search/repositories?q=user:{}'.format(user_name)
        req_dict = json_get(req_body, {'Authorization': 'token {}'.format(access_token)}, git_filename_temp)
    else:
        file = open('{}\\{}'.format(os.getcwd(), git_filename_temp), 'r', encoding='utf-8')
        req_dict = json.load(file)

    #Формирование результирующего файла
    if (len(req_dict) > 0 and "message" not in req_dict):
        required = ["id", "name", "full_name", "private"]
        result_dict = req_dict["items"]

        result_dict = choose_from_json(result_dict, required)

        json_save(git_filename_res, result_dict)
        print("Result for git: {}.".format(result_dict))
    else:
        print("Error for git: {}".format(req_dict))

get_vk_groups()
get_git_repos()


