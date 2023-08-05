from gravity_core_api.operate_user_commands import settings
from gravity_core_api.operate_user_commands.service_functions import operate_command
from gravity_core_api.operate_user_commands import functions


def operate_user_command(sqlshell, ar_support_methods, general_command, data, *args, **kwargs):
    for command, values in data.items():
        ar_method = functions.if_method_supported(ar_support_methods, command)
        if ar_method:
            data = functions.add_ar_method_to_data(data, ar_method)
            new_response = {}
            response = operate_command(sqlshell, general_command, data)
            new_response['response'] = response
            new_response['ar_method'] = command
            response = new_response
        else:
            response = {'status': 'failed',
                        'info': 'Подкоманда {}. Исполнение команды {} не поддерживается GCore.'.format(general_command,
                                                                                                       command)}
    return response