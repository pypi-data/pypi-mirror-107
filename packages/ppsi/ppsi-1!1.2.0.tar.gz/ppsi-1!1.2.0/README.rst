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

  - workspace's default app: triggered by ``$mod+Shift+Return``
  - workspace-specific customizable apps

- remote [ssh/waypipe]
- password-manager [pass]
- wifi [nmcli]
- bluetooth [bluez]
- reboot [systemd]
- poweroff [systemd]
- volume [pactl] with feedback
- brightness [ light] with feedback

- a customizable pspbar (an info-bar) showing:

  - Workload (only if heavy)
  - OS Name
  - Network Speeds
  - Current IP (interactive)
  - RAM Usage
  - CPU Usage
  - Core Temperature
  - Battery (interactive)
  - Time (interactive)


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
