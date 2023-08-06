简介
============
"rnxcovpy" 是对GNSS标准数据格式RINEX(The Receiver Independent Exchange Format)格式的观测值文件部分版本之间进行相互转换的工具。

当前版本支持的转换
==================
- RINEX OBSERVATION DATA FILE Version 2.11-->3.02
- RINEX OBSERVATION DATA FILE Version 2.11-->3.04
- RINEX OBSERVATION DATA FILE Version 2.11-->3.05
- RINEX OBSERVATION DATA FILE Version 3.02-->2.11
- RINEX OBSERVATION DATA FILE Version 3.04-->2.11
- RINEX OBSERVATION DATA FILE Version 3.05-->2.11
- RINEX OBSERVATION DATA FILE Version 3.02-->3.04
- RINEX OBSERVATION DATA FILE Version 3.02-->3.05
- RINEX OBSERVATION DATA FILE Version 3.04-->3.05

注意事项
============
- 此版本为测试版本，可能存在未发现的错误！
- 由于RINEX版本的不同，应充分考虑到转换后部分信息丢失的情况！

安装
============

从 `PyPI`_ 使用 `pip installer`_ 进行安装

    pip install rnxcovpy


.. _PyPI: http://pypi.python.org/pypi/ngram
.. _pip installer: http://www.pip-installer.org