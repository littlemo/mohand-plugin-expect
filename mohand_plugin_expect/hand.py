import sys
import logging
import pexpect
from mohand.hands import hand

LOG_FORMAT = "[%(asctime)s][%(name)s:%(lineno)s][%(levelname)s] %(message)s"
format_ = logging.Formatter(LOG_FORMAT)
sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(format_)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(sh)


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
            log.debug("decrator param: {} {}".format(dargs, dkwargs))
            log.debug("function param: {} {}".format(args, kwargs))
            kwargs.pop('cmd', None)
            kwargs.pop('timeout', None)
            return func(*args, **kwargs)
        return _wrapper
    return wrapper if not invoked else wrapper(func)


class Child(object):
    """
    pexpect实例创建后的返回子线程，支持一系列接口方法
    """
    def __init__(self, *args, **kwargs):
        _cmd = kwargs.get('cmd', None)
        if not _cmd:
            raise ValueError('cmd 值错误，不可为空')
        log.info(_cmd)
        self.timeout = kwargs.get('timeout', 30)
        self.child = pexpect.spawn(_cmd)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None:
            self.child.interact()
            return False
        elif exception_type is ValueError:
            # 返回 False 将异常抛出
            return False
        else:
            log.error('other error: {}\n{}'.format(exception_value, traceback))
            return False
