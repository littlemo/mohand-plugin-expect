# encoding=utf8
from __future__ import unicode_literals

from mohand import hands
from mohand_plugin_expect.hand import expect
from mohand_plugin_expect.version import get_cli_version


class ExpectHand(hands.HandBase):
    '''可用于自动化登录堡垒机完成跳转选择、账户密码输入等操作'''

    def register(self):
        return expect

    def version(self):
        return 'mohand-plugin-expect', get_cli_version()
