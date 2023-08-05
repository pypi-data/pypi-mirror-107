""" Модуль для обработки комманд типа update_record """
from gravity_core_api.wserver_update_commands import settings
from gravity_core_api.wserver_update_commands.service_functions import operate_command


def operate_update_record(sqlshell, general_command, data, *args, **kwargs):
    response = operate_command(sqlshell, settings.all_keys, general_command, data)
    return response


def add_sqlshell(sqlshell, data):
    if type(data) == dict:
        data = add_sqlshell_to_values(sqlshell, data)
    elif type(data) == list:
        new_data = []
        for el in data:
            el = add_sqlshell_to_values(sqlshell, el)
            new_data.append(el)
        data = new_data
    return data


def add_sqlshell_to_values(sqlshell, data):
    for sub_command, values in data.items():
        values['sqlshell'] = sqlshell
    return data
