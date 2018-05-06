from mohand.hands import hand


def expect(*dargs, **dkwargs):
    """
    将被装饰函数封装为一个 :class:`click.core.Command` 类，成为 ``mohand`` 的子命令

    该装饰器可能被作为一个简单无参数的装饰器使用（如： ``@hand.expect`` ）
    或者包含定制其行为的含参数装饰器使用（如： ``@hand.expect(timeout=30)`` ）

    .. note::

        该装饰器最终会通过插件系统被注册到 :data:`.hands.hand` 中。

        此处的 ``expect`` 装饰器本身是应该不支持无参数装饰的，但考虑到其作为样例实现，
        故将其实现为兼容两种传参的装饰器

    """
    invoked = bool(len(dargs) == 1 and not dkwargs and callable(dargs[0]))
    if invoked:
        func = dargs[0]

    def wrapper(func):
        @hand._click.command(
            name=func.__name__.lower(),
            help=func.__doc__)
        @hand._click.option(
            '--cmd',
            default=dkwargs.get('cmd'),
            help='用于构造上下文环境的终端命令，将传入 pexpect.spawn')
        @hand._click.option(
            '--timeout', '-t',
            type=hand._click.INT,
            default=dkwargs.get('timeout'),
            help='expect 的超时时间')
        def _wrapper(*args, **kwargs):
            print("decrator param:", dargs, dkwargs)
            print("function param:", args, kwargs)
            kwargs.pop('cmd', None)
            kwargs.pop('timeout', None)
            return func(*args, **kwargs)
        return _wrapper
    return wrapper if not invoked else wrapper(func)
