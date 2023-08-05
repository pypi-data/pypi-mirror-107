def extract_core_support_methods(gravity_engine, *args, **kwargs):
    try:
        methods = gravity_engine.get_api_support_methods()
        return methods
    except AttributeError:
        return {}
