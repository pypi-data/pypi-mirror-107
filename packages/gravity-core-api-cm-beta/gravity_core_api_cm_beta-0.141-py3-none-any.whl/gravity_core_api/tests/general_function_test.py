from gravity_core_api import functions
from gravity_core_api.tests import test_ar


engine = test_ar.TestAR()


def extract_api_methods_test(engine):
    response = functions.extract_core_support_methods(engine)
    print('response:', response)
    return response

extract_api_methods_test(engine)