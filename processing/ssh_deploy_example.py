"""
manage.py

created by dromakin as 18.11.2020
Project iBeacon
"""

__author__ = 'dromakin'
__maintainer__ = 'dromakin'
__credits__ = ['dromakin', ]
__status__ = 'Development'
__version__ = '20201118'

import fabric
from fabric import Connection
from invoke import run

# from config.settings import PI_SSH_CONNECTION_PROPERTIES
# PI_SSH_CONNECTION_PROPERTIES = {
#     "host": "192.168.31.97",
#     "user": "pi",
#     "connect_kwargs": {
#         "password": "Romakin1594"
#     }
# }


# send settings.json
# def send_settings():


    # c = Connection(**PI_SSH_CONNECTION_PROPERTIES)
    # command = "cd ~/Documents/display/settings && echo 'Hello, world.' >foo.txt"
    # return c.run(command, hide=True).stdout.strip()


# Start program
# update data.json
# update settings.json

# Stop program

# Update program

#
# if __name__ == '__main__':
#     send_settings()


if __name__ == '__main__':
    # command = "which nginx"
    # command = "nginx -c /Users/romakindmitriy/PycharmProjects/iBeacon/config/nginx.conf"
    # command = "nginx -s reload -c /Users/romakindmitriy/PycharmProjects/iBeacon/config/nginx.conf"
    # command = "nginx -s stop"
    command = "ps aux | grep 'nginx'"
    result = run(command, hide=True, warn=True)
    print(result)



