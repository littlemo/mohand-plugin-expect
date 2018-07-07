# encoding=utf8
from __future__ import unicode_literals

import re
import sys
import logging
import struct
import fcntl
import termios
import signal

import pexpect

from mohand.hands import hand

if sys.version > '3':
    PY3 = True
else:
    PY3 = False

LOG_FORMAT = "[%(asctime)s][%(name)s:%(lineno)s][%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.WARN,
    format=LOG_FORMAT,
    stream=sys.stdout,
)
log = logging.getLogger(__name__)


def expect(*dargs, **dkwargs):
    """
    将被装饰函数封装为一个 :class:`click.core.Command` 类，成为 ``mohand`` 的子命令

    该装饰器可能被作为一个简单无参数的装饰器使用（如： ``@hand.expect`` ）
    或者包含定制其行为的含参数装饰器使用（如： ``@hand.expect(timeout=30)`` ）

    .. note::

        该装饰器最终会通过插件系统被注册到 :data:`.hands.hand` 中。

        此处的 ``expect`` 装饰器本身是应该不支持无参数装饰的，但考虑到其作为样例实现，
        故将其实现为兼容两种传参的装饰器

    :param int log_level: 当前子命令的日志输出等级，默认为： ``logging.INFO``
    :param str cmd: 用于构造上下文环境的终端命令，将传入 pexpect.spawn
    :param str encoding: 可选，spawn命令执行时的指定编码，默认为 ``utf-8``
    :param int timeout: 可选，执行 spawn 的超时时间，默认为 ``30`` 秒
    :return: 被封装后的函数
    :rtype: function
    """
    invoked = bool(len(dargs) == 1 and not dkwargs and callable(dargs[0]))
    if invoked:
        func = dargs[0]

    def wrapper(func):
        @hand._click.command(
            name=func.__name__.lower(),
            help=func.__doc__)
        def _wrapper(*args, **kwargs):
            log_level = dkwargs.pop('log_level', logging.INFO)
            log.setLevel(log_level)

            log.debug("decrator param: {} {}".format(dargs, dkwargs))
            log.debug("function param: {} {}".format(args, kwargs))

            with Child(*dargs, **dkwargs) as c:
                func(c, *args, **kwargs)
        return _wrapper
    return wrapper if not invoked else wrapper(func)


class Child(object):
    """
    pexpect实例创建后的返回子线程，支持一系列接口方法
    """
    child = None

    def __init__(self, *args, **kwargs):
        _cmd = kwargs.get('cmd', None)
        if not _cmd:
            raise ValueError('cmd 值错误，不可为空')
        hand._click.echo(_cmd)
        _timeout = kwargs.get('timeout', 30)
        log.debug('spawn执行的超时时间: {}s'.format(_timeout))
        _encodeing = kwargs.get('encoding', 'utf-8')
        self.child = Child.child = pexpect.spawn(
            _cmd, timeout=_timeout, encoding=_encodeing)
        self.child.logfile_read = sys.stdout
        signal.signal(signal.SIGWINCH, Child.sigwinch_passthrough)

    def __enter__(self):
        # 进入 spawn 后，强制触发窗口尺寸变化信号，初始化窗口大小设置
        self.sigwinch_passthrough(None, None)
        return self

    @staticmethod
    def sigwinch_passthrough(sig, data):
        """
        处理窗口尺寸变化信号，并相应更新 tty 窗口大小设置
        """
        log.debug('Received signal: {}, {}'.format(sig, data))
        s = struct.pack("HHHH", 0, 0, 0, 0)
        a = struct.unpack(
            'hhhh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
        if Child.child and not Child.child.closed:
            Child.child.setwinsize(a[0], a[1])
            log.debug('重设窗口大小为: {} 行 | {} 列'.format(a[0], a[1]))

    def __print_stdout(self, before, after, newline=False):
        """
        打印终端标准输出

        :param str before: 前文
        :param str after: 后文
        :param bool newline: 行尾换行，默认为 False
        """
        sys.stdout.write('{before}{after}{newline}'.format(
            before=before,
            after=after,
            newline='\n' if newline else ''))

    def action(
            self, expect, sendline, before='',
            retry=3, timeout=5, expect_callback=None, **kwargs):
        """
        执行一个action，当检测到符合指定 ``before`` 的 ``expect`` 后，
        发送 ``sendline``

        :param str expect: 期望的输入匹配行，支持多对象的列表，以及正则表达式对象
            如：['good', 'bad', re.compile(r'\\\d'),
            pexpect.EOF, pexpect.TIMEOUT]
        :param sendline: 发送一行字串，若为正则表达式，则发送匹配到的结果字串
        :type sendline: str or regex
        :param str before: 可选，用来辅助判定期望的输入匹配行，默认为 ``''``
        :param int retry: (已弃用)可选，默认为 ``3`` ，重试次数
        :param int timeout: 可选，单位秒，默认为 ``5`` ，
            单条动作中 ``expect`` 的超时时间
        :param expect_callback: expect 的回调函数，传入 expect 列表中匹配到的对象的索引，
            可在其中执行定制的处理逻辑
        :type expect_callback: function(index)
        """
        if not PY3:
            if not isinstance(expect, list):
                expect = [expect]
            for i, e in enumerate(expect):
                if isinstance(e, str):
                    expect[i] = unicode(e)
        try:
            _index = self.child.expect(expect, timeout=timeout)
        except pexpect.exceptions.TIMEOUT as e:
            log.error('执行超时，未遇到期望的匹配字串：{}'.format(
                [getattr(e, 'pattern', e) for e in expect]))
            log.debug('异常堆栈信息：{}'.format(e))
            return
        if expect_callback and callable(expect_callback):
            expect_callback(_index)
        _before = self.child.before
        if before not in _before:
            return
        if isinstance(sendline, type(re.compile(''))):
            # 如果入参是正则对象，则尝试在 before 中匹配到真正的 sendline 字串
            match = sendline.search(_before)
            if not match:
                log.error(
                    '未从传入的sendline正则({sendline})中匹配到字串'.format(
                        sendline=sendline.pattern))
                return
            sendline = match.groups()[0]
        log.debug('待发送字串: {}'.format(sendline))
        self.child.sendline(sendline)

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None:
            self.child.logfile_read = None
            self.child.interact()
            return False
        elif exception_type is ValueError:
            # 返回 False 将异常抛出
            return False
        else:
            log.error('other error: {}\n{}'.format(exception_value, traceback))
            return False
