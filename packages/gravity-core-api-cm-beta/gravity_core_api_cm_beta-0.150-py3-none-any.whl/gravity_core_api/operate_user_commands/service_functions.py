from traceback import format_exc
from gravity_core_api.operate_user_commands.functions import excecute_core_function


def operate_command(sqlshell, general_command, data, *args, **kwargs):
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
        values['sql_shell'] = sqlshell
        try:
            response = excecute_core_function(**values)
        except:
            response = {'status': 'failed', 'info': 'Ошибка выполнения команды {}!'.format(key), 'details': format_exc()}
        return response


