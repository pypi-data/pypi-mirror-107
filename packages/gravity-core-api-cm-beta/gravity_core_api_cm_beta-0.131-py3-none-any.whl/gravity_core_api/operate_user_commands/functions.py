def if_method_supported(ar_support_methods, command):
    for method_name, method_values in ar_support_methods.items():
            if command == method_name:
                return method_values['method']


def add_ar_method_to_data(data, ar_method):
    for command, info in data.items():
        info['ar_method'] = ar_method
    return data


def get_success_response(status='success', info=None):
    response = {'status': status, 'info': info}
    return response


def get_fail_response(status='failed', info=None):
    response = {'status': status, 'info': info}
    return response


def excecute_core_function(*args, **kwargs):
    """ Исполняет команду из Core, возвращает его ответ """
    return kwargs['ar_method'](**kwargs)
