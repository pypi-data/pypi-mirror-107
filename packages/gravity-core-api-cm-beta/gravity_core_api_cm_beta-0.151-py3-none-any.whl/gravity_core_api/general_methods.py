from gravity_core_api.wserver_update_commands.main import operate_update_record
from gravity_core_api.operate_user_commands.main import operate_user_command
from gravity_core_api.functions import extract_core_support_methods

methods_dict = {'wserver_sql_command': {'subcommand_operator': ...},
                'wserver_insert_command': {'subcommand_operator': operate_update_record},
                'user_command': {'subcommand_operator': operate_user_command},
                'get_methods': {'subcommand_operator': extract_core_support_methods}
                }