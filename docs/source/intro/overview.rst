.. _intro-overview:

====
概览
====

`MoHand`_ 插件，用以提供可自动控制连接应用的任务支持，可用于自动化登录堡垒机完成跳转选择、
账户密码输入等操作。

基于 `pexpect`_ 包做的封装实现，并提供了一个增强的 :method:`.action` 接口，
支持基于正则的 ``sendline`` 发送。

其使用原理同 **shell** 下的 ``expect`` ，建议您提前了解下，以便更好的理解接下来的样例。


.. _MoHand: http://mohand.rtfd.io/
.. _pexpect: http://pexpect.rtfd.io/
