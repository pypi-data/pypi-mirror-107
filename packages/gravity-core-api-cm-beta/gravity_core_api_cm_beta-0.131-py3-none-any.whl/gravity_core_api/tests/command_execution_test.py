from gravity_core_api.main import GCSE
from wsqluse.wsqluse import Wsqluse
from gravity_core_api.tests import test_settings as s
from gravity_core_api.tests.test_ar import TestAR

engine = TestAR()


sqlshell = Wsqluse('wdb', 'watchman', 'hect0r1337', '192.168.100.109')
gcse = GCSE(s.api_ip, s.api_port, sqlshell, debug=True, gravity_engine=engine)
gcse.launch_mainloop()