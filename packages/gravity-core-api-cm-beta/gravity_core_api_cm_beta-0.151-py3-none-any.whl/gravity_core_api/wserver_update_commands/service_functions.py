from traceback import format_exc


def operate_command(sqlshell, all_keys, general_command, data, *args, **kwargs):
    """ Получает словарь с данными для работы.
      Далее, функция обращается к словарю all_keys, где содержатся все команды в виде ключей ('trash_cat', 'trash_type')
      а в виде значения этих ключей еще один словарь, с такими ключами как, например, 'execute_function', которая
      принимает данные и работает с ними согласно ключу.
      То есть имеем такую структуру - поступает команда в виде {'trash_cat': {'name': 'ТКО-4', 'wserver_id':17}}.
      operate_update_record (эта функция) берет ключ первого словаря ('trash_cat'), обращается с ним в словарь all_keys,
      если находит его там, возвращает его значение 'execute_function', и передает значение ключа ('name', 'wserver_id')
      этой функции, далее возращает ответ выполнения.
      """
    for key, values in data.items():
        try:
            response = all_keys[key]['execute_function'](sqlshell, **values)
        # Нет такого ключа в all_keys
        except KeyError:
            response = {'status': 'failed', 'info': 'Подкоманда {}. '
                                                    'Для комманды {} не прописана логика.'.format(general_command, key),
                        'details': format_exc()}
            print(format_exc())
        return response