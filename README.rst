Introduction
============

Wrapper script for starting a command line tool with bash completion. It uses
a highly flexible configuration file so it can be used for different tools.

I'm using this to start mysql/mysqladmin/mysqldump/mycli with (optional) SSH
tunnels.

.. image:: wrapc.gif

Installation
============

Install wrapc in a virtualenv using the following command:

::

 python3 -m venv ~/venv/wrapc
 . ~/venv/wrapc/bin/activate
 pip install git+https://github.com/meeuw/wrapc
 cd ~/venv/wrapc/bin
 ln -s wrapc myclic
 ln -s wrapc mysqlc

Create the configuration file ``~/.wrapcrc`` with the following contents:

::

 [myclic]
 command = mycli --defaults-file /home/user/mysql/{server} {database} --prompt "{server} \d > "
 complete0_command = ls ~/mysql
 complete0 = server
 complete1_command = mysqlc {server} mysql -NBe "show databases"
 complete1 = database
 pre_hook = ~/bin/sshtunnel.py {server}

 [mysqlc]
 command = mysql --defaults-file=/home/user/mysql/{server} {database}
 complete0_command = ls ~/mysql
 complete0 = server
 complete1_command = mysqlc {server} mysql -NBe "show databases"
 complete1 = database
 pre_hook = ~/bin/sshtunnel.py {server}

Create the ``~/bin/sshtunnel.py`` script:

::

 #!/usr/bin/env python3
 import os
 import sys
 sshtunnel = None
 with open(os.path.expanduser('~/mysql/' + sys.argv[1])) as f:
     s = f.read()
     if len(s) > 0 and s[0] == '#':
         sshtunnel = s[1:].split('\n')[0]
 if sshtunnel and os.system('ssh -O check {}-controlmaster &>/dev/null'.format(sshtunnel)) != 0:
     os.system('ssh -f {}-controlmaster sleep 60 &>/dev/null'.format(sshtunnel))

And change the permissions ``chod a+x ~/bin/sshtunnel.py``

Now a configuration files for ``server`` is defined in ``~/mysql/server``
(notice the first comment, which should match the control-master for the
SSH configuration, you should also match the port):

::

 # server
 [client]
 user = root
 host = localhost
 port = 3307


Create the following entry in ``~/.ssh/config``, replace ``server`` with the
server name which you've used for ``~/mysql/server``:

::

 Host server-controlmaster
     HostName remoteserver
     Port 2189
     ControlPath /home/meeuw/.ssh/server-control
     ControlMaster auto
     LocalForward 3307 localhost:3306


Make sure you've configured SSH keys to allow non-interactive logins. You
should try to connect using ``ssh server-controlmaster``.

Now add the following to your ``.bashrc``

::

 eval "$(register-python-argcomplete mysqlc)"
 eval "$(register-python-argcomplete myclic)"
