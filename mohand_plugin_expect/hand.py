from mohand.hand import hand

# print('HandDict@mohand_plugin_expect:', hand)
# print('HandDict@mohand_plugin_expect:', id(hand))


def expect(*dargs, **dkwargs):
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
    return wrapper
