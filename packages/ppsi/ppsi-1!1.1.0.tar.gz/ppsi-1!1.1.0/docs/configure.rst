###################
USER-CONFIGURATION
###################

Configuration file is in `yaml <https://yaml.org/spec/>`__
format.

- Copy `ppsi.yml <ppsi/server/config/ppsi.yml>`__ to ``${HOME}/.config/sway/ppsi.yml``

.. note::

   pip generally installs packages in /home/.local/lib

.. code:: sh

   cp "${HOME}/.local/lib/python$(python --version | awk '{print $2}' | cut -d '.' -f 1,2)/site-packages/ppsi/server/config/ppsi.yml" "${HOME}/.config/sway/ppsi.yml"

- If ppsi somehow got installed system-wide **this is strongly discouraged**, use the following instead

.. code:: sh

   cp "/usr/local/lib/python$(python --version | awk '{print $2}' | cut -d '.' -f 1,2)/site-packages/ppsi/server/config/ppsi.yml" "${HOME}/.config/sway/ppsi.yml"

- modify it suitably

********************************
Location of configuration file
********************************

User (XDG_CONFIG_HOME):
========================

This variable is generally set to ``$HOME/.config/sway/ppsi.yml`` on unix-like
systems. Even if unset, we will still try the ``$HOME/.config``
directory.

``$XFG_CONFIG_HOME/sway/ppsi.yml``

.. note::

   Optionally,
     - configuration file may be submitted using the command line flag `-f`
     - custom sway-root location may be supplied using command line flag `-r`
     - SWAYROOT variable must be set in the environment.

*********************
Configuration format
*********************


3 yaml objects
================
1. primary keybinding:

   .. code:: yaml

      key-primary: $mod+Shift+Return

2. workspaces:

   .. code:: yaml

      workspaces:
      - index:
        - 1
        name: WWW
        primary: firefox
        bind:
        - key: $mod+Shift+g
          exec: google-chrome
        assignments:
          ^Firefox$: wayland

      - index:
        - 2
        name: GNU
        primary: emacsclient -c -a=""
        assignments:
          ^Emacs$: xorg
        bind: []

      - index:
        - F1
        - F2
        - F3
        - F4
        - F5
        name: REMOTE
        primary: ppsi remote
        bind: []
        assignments: {}

3. remote:

   .. code:: yaml

      remote:
        hosts:
        - localhost
        - www.example.com

        users:
        - root
        - guest
