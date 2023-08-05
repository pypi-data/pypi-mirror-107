""" Перспективный единый TCP API endpoint для Gravity core """
from witapi.main import WITServer
from gravity_core_api.wserver_update_commands.main import operate_update_record
from gravity_core_api.operate_user_commands.main import operate_user_command
from gravity_core_api import functions as general_functions


class GCSE(WITServer):
    """ Gravity Core Single Endpoint """

    def __init__(self, myip, myport, sqlshell, core, debug=False):
        super().__init__(myip, myport, sqlshell=sqlshell, without_auth=True, mark_disconnect=False, debug=debug)
        self.core = core
        self.sqlshell = sqlshell
        self.ar_support_methods = general_functions.extract_core_support_methods(core)


    def execute_command(self, comm, values):
        if comm == 'wserver_insert_command':
            response = operate_update_record(self.sqlshell, comm, values)
        elif comm == 'user_command':
            response = operate_user_command(self.sqlshell, self.ar_support_methods, comm, values)
        elif comm == 'get_methods':
            response = list(self.ar_support_methods.keys())
        else:
            response = {'status': 'failed', 'info': 'Для комманды {} не прописана логика.'.format(comm)}
        return response

