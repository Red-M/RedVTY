#!/usr/bin/env python3
# RedVTY
# Copyright (C) 2019  Red_M ( http://bitbucket.com/Red_M )

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import getpass
import redvty

def main():
    username = input('Username: ')
    hostname = input('Hostname: ')
    passwd = getpass.getpass()

    rt = redvty.RedVTY()
    rt.login(hostname,username=username,password=passwd,allow_agent=True)
    hostname = rt.command('hostname',remove_newline=True)
    rt.sendline('tmux -u a || tmux -u')
    expect = rt.prompt('"'+hostname+'"')
    print('\n'.join(rt.screen.display))
    rt.command('exit')
    rt.exit()


if __name__=='__main__':
    main()
