import functools


class ObjectProxy(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__name__ = wrapped.__name__
        except AttributeError:
            pass

    @property
    def __class__(self):
        return self.wrapped.__class__

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


class BoundFunctionWrapper(ObjectProxy):

    def __init__(self, wrapped, instance, wrapper):
        super().__init__(wrapped)
        self.instance = instance
        self.wrapper = wrapper

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            instance, args = args[0], args[1:]
            wrapped = functools.partial(self.wrapped, instance)
            return self.wrapper(wrapped, instance, args, kwargs)
        return self.wrapper(self.wrapped, self.instance, args, kwargs)


class FunctionWrapper(ObjectProxy):

    def __init__(self, wrapped, wrapper):
        super().__init__(wrapped)
        self.wrapper = wrapper

    def __get__(self, instance, owner):  # instance is automatically provided as __get__ is used for method calls.
        wrapped = self.wrapped.__get__(instance, owner)
        return BoundFunctionWrapper(wrapped, instance, self.wrapper)

    def __call__(self, *args, **kwargs):  # __call__ is used for functions, not methods.
        return self.wrapper(self.wrapped, None, args, kwargs)  # passes in "None" for the instance


def decorator(wrapper):
    @functools.wraps(wrapper)
    def _decorator(wrapped):
        return FunctionWrapper(wrapped, wrapper)
    return _decorator


@decorator
def my_function_wrapper(wrapped, instance, args, kwargs):
    print('INSTANCE', instance)
    print('ARGS', args)
    return wrapped(*args, **kwargs)


@my_function_wrapper
def function(a, b):
    pass


class MyClass:
    def __init__(self, my_name):
        self.my_name = my_name

    @my_function_wrapper
    def function_im(self, a, b):
        print('instance: ' + self.my_name)