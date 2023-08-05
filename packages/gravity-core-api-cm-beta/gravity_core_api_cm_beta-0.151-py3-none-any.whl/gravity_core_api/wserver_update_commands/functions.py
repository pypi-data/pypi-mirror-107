""" Содержит функции-обработчики команд и их вспомогательные функции """
from gravity_core_api.wserver_update_commands import settings


def trash_cat_execute(sqlshell, cat_name, wserver_id, active, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о категории груза"""
    command = "INSERT INTO {} (cat_name, wserver_id, active) values ('{}', {}, {}) " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET cat_name='{}', active={}"
    command = command.format(settings.trash_cats_tablename, cat_name, wserver_id, active,
                             cat_name, active)
    response = sqlshell.try_execute(command)
    return response


def trash_type_execute(sqlshell, name, wserver_id, active, category, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о категории груза"""
    command = "INSERT INTO {} (name, wserver_id, active, category) values ('{}', {}, " \
              "{}, (SELECT id FROM {} WHERE wserver_id={})) " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET name='{}', active={}, category=(SELECT id FROM {} WHERE wserver_id={})"
    command = command.format(settings.trash_types_tablename, name, wserver_id,
                             active, settings.trash_cats_tablename, category,
                             name, active, settings.trash_cats_tablename, category)
    response = sqlshell.try_execute(command)
    return response


def auto_execute(sqlshell, car_number, car_protocol, rg_weight, auto_model, rfid, wserver_id, active, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о машине"""
    command = "INSERT INTO {} (car_number, rfid, id_type, rg_weight, wserver_id, auto_model, active) " \
              "values ('{}', '{}', '{}', {}, {}, {}, {}) " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET car_number='{}', rfid='{}', id_type='{}', rg_weight='{}', auto_model={}, active={}"
    command = command.format(settings.auto_tablename,
                             car_number, rfid, car_protocol, rg_weight, wserver_id, auto_model, active,
                             car_number, rfid, car_protocol, rg_weight, auto_model, active)
    response = sqlshell.try_execute(command)
    return response


def clients_execute(sqlshell, full_name, inn, kpp, id_1c, wserver_id, active, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о клиенте"""
    print("TAGER", locals())
    short_name = full_name
    active = bool(active)
    command = "INSERT INTO {} (full_name, short_name, inn, kpp, wserver_id, active, id_1c) " \
              "values ('{}', '{}', '{}', '{}', {}, {}, '{}') " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET full_name='{}', short_name='{}', inn='{}', kpp='{}', active={}, id_1c='{}'"
    command = command.format(settings.clients_tablename,
                             full_name, short_name, inn, kpp, wserver_id, active, id_1c,
                             full_name, short_name, inn, kpp, active, id_1c)
    response = sqlshell.try_execute(command)
    return response


def update_route(sqlshell, car_number, id, count, active, *args, **kwargs):
    """ Обновить маршруты от AR """
    command = "INSERT INTO {} (car_number, count_expected, wserver_id, active) values ('{}', {}, {}, {}) " \
              "ON CONFLICT (wserver_id) DO UPDATE SET car_number='{}', count_expected={}, active={}"
    command = command.format(settings.routes_tablename, car_number, count, id, active,
                             car_number, count, active)
    response = sqlshell.try_execute(command)
    # Добавляем в ответ wserver_id, который был при приеме
    response['wserver_id'] = id
    return response


def update_routes_execute(sqlshell, routes_list, *args, **kwargs):
    all_responses = []
    for route in routes_list:
        response = update_route(sqlshell, **route)
        all_responses.append(response)
    return all_responses


def operators_execute(sqlshell, username, password, wserver_id, active, full_name, role='usual', config=0, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи об операторе"""
    command = "INSERT INTO {} (username, password, role, config, full_name, wserver_id, active) " \
              "values ('{}', '{}', '{}', {}, '{}', {}, {}) " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET username='{}', password='{}', role='{}', config={}, full_name='{}', wserver_id={},active={}"
    command = command.format(settings.operators_tablename,
                             username, password, role, config, full_name, wserver_id, active,
                             username, password, role, config, full_name, wserver_id, active)
    response = sqlshell.try_execute(command)
    return response

