# Copyright (c) 2010-2013, oDesk http://www.odesk.com
# All rights reserved.
import re


VERSION = (0, 5, 0, 'beta', 3)


def get_version():
    version = '{0}.{1}'.format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '{0}.{1}'.format(version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '{0} pre-alpha'.format(version)
    else:
        if VERSION[3] != 'final':
            version = "{0} {1}".format(version, VERSION[3])
            if VERSION[4] != 0:
                version = '{0} {1}'.format(version, VERSION[4])
    return version


def update_init(version):
    print 'Updating ``odesk/__init__.py`` to version "{0}"'.format(version)
    # Update 'VERSION' variable in ``odesk/__init__.py``
    with open('odesk/__init__.py', 'r') as f:
        init_contents = f.read()

    new_init = re.sub(
        '(VERSION = \'[.]*\')', 'VERSION = \'{0}\''.format(version),
        init_contents)

    # Write backup
    with open('odesk/__init__.py.back', 'w') as f:
        f.write(init_contents)

    # Write new init
    with open('odesk/__init__.py', 'w') as f:
        f.write(new_init)

    print 'OK'


if __name__ == '__main__':
    update_init(get_version())
