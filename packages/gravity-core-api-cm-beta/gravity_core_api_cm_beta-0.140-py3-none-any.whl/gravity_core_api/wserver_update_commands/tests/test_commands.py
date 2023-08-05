from gravity_core_api.wserver_update_commands import settings


all_test_commands = {'trash_cats': {'test_command': {settings.BASE_METHOD: {'trash_cats': {'cat_name': 'test123',
                                                                                           'wserver_id': 1488,
                                                                                           'active': True}}}},

            'trash_types': {'test_command': {settings.BASE_METHOD: {'trash_types': {'name': 'TEST123',
                                                                                     'wserver_id': 99,
                                                                                     'category': 12 ,
                                                                                     'active': True}}}},

            'auto': {'test_command': {settings.BASE_METHOD: {'auto': {'car_number': 'Х079АС102',
                                                                     'car_protocol': 'rfid',
                                                                     'rg_weight': 0,
                                                                     'auto_model': 0,
                                                                     'wserver_id': 634888,
                                                                     'active': True,
                                                                     'rfid': 'FFFF000140'}}}},

            'companies': {'test_command': {settings.BASE_METHOD: {'companies': {'wserver_id': 34197,
                                                                                    'full_name': 'ООО "Вториндустрия"',
                                                                                    'short_name': 'ООО "Вториндустрия"',
                                                                                    'inn': '0268058847',
                                                                                    'kpp': None,
                                                                                    'active': True,
                                                                                    'id_1c': '000000006'}}}},

            'update_routes': {'test_command': {settings.BASE_METHOD: {'update_routes': {'routes_list':[{'id': 63,
                                                                                             'car_number': 'А049МС702',
                                                                                             'count': 1,
                                                                                             'active': True},

                                                                                            {'id': 65,
                                                                                             'car_number': 'У431УМ102',
                                                                                             'count': 1,
                                                                                             'active': True}]}}}},

            'operators': {'test_command': {settings.BASE_METHOD: {'operators': {'wserver_id': 101,
                                                                                    'username': 'Эльверт',
                                                                                    'password': '$1$vymmxcZg$Qr3v4mnCgzRxzO4.ApW/P1',
                                                                                    'full_name': 'Эльверт',
                                                                                    'active': True}}}}
                     }
