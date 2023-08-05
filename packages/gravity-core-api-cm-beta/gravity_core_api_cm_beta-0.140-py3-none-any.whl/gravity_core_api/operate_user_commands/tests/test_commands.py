from gravity_core_api.tests.test_ar import TestAR


test_ar = TestAR()

all_test_commands = {'get_status':
                         {'test_command':
                              {'user_command': {'get_status': {}}},
                               'active': True},
                     'start_car_protocol': {'test_command':
                                                  {'user_command': {'start_car_protocol': {'info':
                                                                                               {'record_id': 2,
                                                                                                'carnum': 'А333АА333',
                                                                                                'carrier': 1,
                                                                                                'trash_cat': 5,
                                                                                                'trash_type': 4,
                                                                                                'comm': 'INITTED FROM API',
                                                                                                'course': 'IN',
                                                                                                'car_choose_mode': 'manual',
                                                                                                'dlinnomer': 0,
                                                                                                'polomka': 0,
                                                                                                'orup_mode': 'extended',
                                                                                                'operator': 1,
                                                                                                'carnum_was': 'А333АА333',
                                                                                                'polygon_object': 'ТКО-ТЕСТ'}
                                                                                           }
                                                                    }
                                                   },
                                            'active': True},

                     'operate_gate_manual_control': {'test_command':
                                                         {'user_command': {'operate_gate_manual_control': {'operation': 'close',
                                                                                                           'gate_name': 'entry'}}},
                                                     'active': True},

                     'change_opened_record': {'test_command':
                                                  {'user_command': {'change_opened_record': {'record_id': 2,
                                                                                             'car_number': 'А333АА333',
                                                                                             'carrier': 1,
                                                                                             'trash_cat': 5,
                                                                                             'trash_type': 4,
                                                                                             'comment': 'CHANGED FROM UT',}
                                                                    }},
                                              'active': True},

                     'close_opened_record': {'test_command':
                                                  {'user_command': {'close_opened_record': {'record_id': 3}
                                                                    }},
                                              'active': True},

                     'get_unfinished_records': {'test_command':
                                                 {'user_command': {'get_unfinished_records': {'record_id': 3}
                                                                   }},
                                             'active': True},

                     'get_health_monitor': {'test_command':
                                                    {'user_command': {'get_health_monitor': {'record_id': 3}
                                                                      }},
                                                'active': True},

                     'try_auth_user': {'test_command':
                                                {'user_command': {'try_auth_user': {'username': 'test_user_1',
                                                                                    'password': '123'}
                                                                  }},
                                            'active': True},

                     'capture_cm_terminated': {'test_command':
                                           {'user_command': {'capture_cm_terminated': {'username': 'test_user_1',
                                                                               'password': '123'}
                                                             }},
                                       'active': True},

                     'capture_cm_launched': {'test_command':
                                           {'user_command': {'capture_cm_launched': {'username': 'test_user_1',
                                                                               'password': '123'}
                                                             }},
                                       'active': True},
                     }