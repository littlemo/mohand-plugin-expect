.. _intro-overview:

====
概览
====

`MoHand`_ 插件，用以提供可自动控制连接应用的任务支持，可用于自动化登录堡垒机完成跳转选择、
账户密码输入等操作。

基于 `pexpect`_ 包做的封装实现，并提供了一个增强的 :meth:`.action` 接口，
支持基于正则的 ``sendline`` 发送。

其使用原理同 **shell** 下的 ``expect`` ，建议您提前了解下，以便更好的理解接下来的样例。

.. note::

    值得一提的是，通过 shell 脚本使用 ``expect`` 登录后，改变窗口尺寸会出现 ``stty size``
    并没有根据窗口变换而变换的问题。而这种问题在纯手工登录时不会发生。

    在开发本插件时，也遇到了同样的问题，但强迫症实在不能忍，实在太膈应了，于是通过额外监听
    ``SIGWINCH`` 系统信号，来针对变更自动设置窗口的 ``stty`` 大小

安装方法
========

您可以通过 ``pip`` 进行安装，本包仅在 ``Python 3.X`` 下测试通过::

    pip3 install mohand-plugin-expect

.. hint::

    从 ``v1.0.1`` 版本开始，增加了对 ``Python 2.X`` 的支持，但由于我主要在 **Py3**
    环境下使用，所以强烈建议您在 **Py3** 下使用。如果您在 **Py2** 环境下遇到任何异常，
    可以及时提 `Issues`_ 给我，我会努力在搬砖的间隙进行修复。。。

.. attention::

    本插件已被添加进 ``mohand`` 的 ``install_requires`` 中，故已无需单独安装

.. note::

    建议使用 `virtualenv`_ 来安装，避免与其他包产生依赖冲突。

    如果您感兴趣的话，可以了解下 `virtualenvwrapper`_ ，用其来管理虚拟环境可谓丝般顺滑！

使用说明
========

接下来我们将模拟一个堡垒机登录场景，并通过本包提供的 :func:`.expect` 装饰器来实现自动化登录，
场景如下::

    ssh -o PreferredAuthentications=password moore@bastion -p 22
    moore@bastion's password:
    ********************************************************************************
    *                      Shterm Interactive Terminal v3.2.4                      *
    * Copyright (c) 2006-2018 Zhejiang Qizhi Tech. Co., Ltd.  All rights reserved. *
    ********************************************************************************


    System List
      No: System
       0: All Systems
       1: idc-arch
       2: idc-dev
       3: idc-web
    Please select system:2

    Connecting to any@dev-moore.idc1(10.10.2.213) ...
    login: moore
    moore@10.10.2.213's password:
    Last login: Tue May 15 10:06:23 2018 from bastion
    moore@dev-moore.idc1:~$

为实现该登录流程，我们可以在当前路径下的 ``handfile.py`` 中编写如下::

    import re
    from mohand.hands import hand

    ACCOUNT_USERNAME = 'moore'
    ACCOUNT_PASSWORD = 'xxooxxooyo~~'

    @hand.expect(
        cmd='ssh -o PreferredAuthentications=password moore@bastion -p 22')
    def test(o):
        """自动登录测试"""
        o.action(
            expect=re.compile(r'[Pp]assword:'),
            sendline=ACCOUNT_PASSWORD)
        o.action(
            expect='Please select system:',
            sendline=re.compile(r'(\d+):\s+idc-dev'),
            before='System List')
        o.action(
            expect='login:',
            sendline=ACCOUNT_USERNAME,
            before='Connecting to')
        o.action(
            expect='password:',
            sendline=ACCOUNT_PASSWORD)

以上即为一个最小可用登录命令，注意此处分别在第一个 action 的 expect 参数与第二个 action
的 sendline 中使用了正则表达式，主要为了演示可以这样使用，而非必须，但为了更好地鲁棒性，
建议多使用正则来实现。

.. note::

    如果您不善于书写正则表达式的话，可以尝试我修改&部署的一个 `正则验证工具`_

将其保存到当前路径下，然后执行 ``mohand`` 命令::

    $ mohand
    Usage: mohand [OPTIONS] COMMAND [ARGS]...

      通用自动化处理工具

      详情参考 `GitHub <https://github.com/littlemo/mohand>`_

    Options:
      --author   作者信息
      --version  版本信息
      --help     Show this message and exit.

    Commands:
      test  自动登录测试

我们可以看到刚刚编写的 ``test`` 函数已经被注册成为了一个子命令，
通过执行该子命令我们就可以实现自动化登录到目标主机了::

    $ mohand test

由于在 ``mohand.hands.hand`` 中封装了 `click`_ 库，故我们还可以根据实际需求来添加额外的传参，
具体可以参考其官方文档，以下提供一种思路::

    FUNC_DICT = {
        'project': 'cd path/to/project',
        'mongo': 'mongo xxoo:2000/db_name',
    }

    @hand._click.option(
        '--workspace', '-w',
        type=hand._click.Choice(FUNC_DICT.keys()),
        help='工作空间')
    @hand.expect(
        cmd='ssh -o PreferredAuthentications=password moore@bastion -p 22')
    def test(o, workspace):
        """自动登录测试"""
        ...

        if workspace:
            o.action(
                expect=re.compile(r'.*@.*:.*~.*\$'),
                sendline=FUNC_DICT.get(workspace))

以上，提供了一个可选的关键字参数 ``--workspace`` ，可通过在调用时传入此参数，
来达到额外进入工作空间的目的，调用命令如下::

    $ mohand test -w project  # 自动登录，并进入项目所在路径
    $ mohand test -w mongo    # 自动登录，并进入指定mongo数据库


.. _MoHand: http://mohand.rtfd.io/
.. _pexpect: http://pexpect.rtfd.io/
.. _virtualenv: http://virtualenv.pypa.io/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _正则验证工具: https://tool.moorehy.com/regex/
.. _click: http://click.pocoo.org/6/
.. _Issues: https://github.com/littlemo/mohand-plugin-expect/issues
