*************************
PPSI
*************************

Gist
==========

Source Code Repository
---------------------------

|source| `Repository <https://github.com/pradyparanjpe/ppsi.git>`__


Badges
---------

|Documentation Status|  |Coverage|  |PyPi Version|  |PyPi Format|  |PyPi Pyversion|


Description
==============

A person-python-sway interface

===============================================================

What it does
--------------------

provides a python interface for:

- workspace-specific keybindings for
  - workspace-default code: triggered by ``$mod+Shift+Return``
  - workspace-specific customizable code

- remote [ssh/waypipe]
- password-manager [pass]
- wifi [nmcli]
- bluetooth [bluez]
- reboot [systemd]
- poweroff [systemd]
- volume [pulseaudio] with feedback
- brightness [ light] with feedback

- bar (a simple info-bar) showing:

  - Workload
  - OS Name
  - Network Speeds
  - Current IP
  - RAM Usage
  - CPU Usage
  - Core Temperature
  - Battery
  - Time


.. |Documentation Status| image:: https://readthedocs.org/projects/ppsi/badge/?version=latest
   :target: https://ppsi.readthedocs.io/?badge=latest

.. |source| image:: https://github.githubassets.com/favicons/favicon.png
   :target: https://github.com/pradyparanjpe/ppsi.git

.. |PyPi Version| image:: https://img.shields.io/pypi/v/ppsi
   :target: https://pypi.org/project/ppsi/
   :alt: PyPI - version

.. |PyPi Format| image:: https://img.shields.io/pypi/format/ppsi
   :target: https://pypi.org/project/ppsi/
   :alt: PyPI - format

.. |PyPi Pyversion| image:: https://img.shields.io/pypi/pyversions/ppsi
   :target: https://pypi.org/project/ppsi/
   :alt: PyPi - pyversion

.. |Coverage| image:: docs/coverage.svg
   :alt: tests coverage
   :target: tests/htmlcov/index.html
