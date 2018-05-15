.. _intro-overview:

====
概览
====

`MoHand`_ 插件，用以提供可自动控制连接应用的任务支持，可用于自动化登录堡垒机完成跳转选择、
账户密码输入等操作。

基于 `pexpect`_ 包做的封装实现，并提供了一个增强的 :method:`.action` 接口，
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

.. attention::

    本插件已被添加进 ``mohand`` 的 ``install_requires`` 中，故已无需单独安装

.. note::

    建议使用 `virtualenv`_ 来安装，避免与其他包产生依赖冲突。

    如果您感兴趣的话，可以了解下 `virtualenvwrapper`_ ，用其来管理虚拟环境可谓丝般顺滑！

使用说明
========

接下来我们将模拟一个堡垒机登录场景，并通过本包提供的 ``expect`` 装饰器来实现自动化登录，
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


.. _MoHand: http://mohand.rtfd.io/
.. _pexpect: http://pexpect.rtfd.io/
.. _virtualenv: http://virtualenv.pypa.io/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
