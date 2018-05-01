import click

from mohand.main import main
from mohand.decrator import register


@register
def expect(*dargs, **dkwargs):
    def wrapper(func):
        @main.command(
            name=func.__name__.lower(),
            help=func.__doc__)
        @click.option(
            '--cmd',
            default=dkwargs.get('cmd'),
            help='用于构造上下文环境的终端命令，将传入 pexpect.spawn')
        @click.option(
            '--timeout', '-t',
            type=click.INT,
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
