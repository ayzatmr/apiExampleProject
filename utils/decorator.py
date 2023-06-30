"""A decorator that runs a function only once."""


def func_once(func):
    def decorated(*args, **kwargs):
        try:
            if 'email' in kwargs:
                if decorated._once_kwargs['email'] == kwargs['email']:
                    return decorated._once_result
            decorated._once_result = func(*args, **kwargs)
            decorated._once_kwargs = kwargs
            return decorated._once_result
        except Exception:
            decorated._once_kwargs = kwargs
            decorated._once_result = func(*args, **kwargs)
            return decorated._once_result

    return decorated
