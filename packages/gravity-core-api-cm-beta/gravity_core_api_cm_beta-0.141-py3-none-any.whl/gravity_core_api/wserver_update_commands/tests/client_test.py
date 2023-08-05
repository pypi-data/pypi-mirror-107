from gravity_core_api.tests.client_test import test_all_commands
from gravity_core_api.wserver_update_commands.tests import test_commands

print(test_commands.all_test_commands)
test_all_commands(test_commands.all_test_commands)
