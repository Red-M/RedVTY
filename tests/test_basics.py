import os
import time
import socket
import unittest
import threading
import multiprocessing
import paramiko
import redvty

from .servers import paramiko_server as ssh_server


class SSHSession(object):
    def __init__(self,hostname='127.0.0.1',port=2200,class_init={},connect_args={}):
        self.rs = redvty.RedVTY(**class_init)
        connect_args_extra = {
            'username':'redm',
            'password':'foobar!'
        }
        connect_args_extra.update(connect_args)
        self.rs.login(hostname, port, **connect_args_extra)

    def wait_for(self, wait_string):
        if isinstance(wait_string,type('')):
            wait_string = wait_string.encode('utf8')
        read_data = b''
        while not wait_string in read_data:
            for data in self.rs.read():
                read_data += data
        return(read_data)

    def sendline(self, line):
        self.rs.send(line+'\r\n')



class RedSSHUnitTest(unittest.TestCase):

    def setUp(self):
        self.key_path = os.path.join(os.path.join(os.getcwd(),'tests'),'ssh_host_key_paramiko')
        self.bad_key_path = os.path.join(os.path.join(os.getcwd(),'tests'),'ssh_host_key')
        self.ssh_servers = []
        self.ssh_sessions = []
        self.server_hostname = '127.0.0.1'

    def start_ssh_server(self):
        q = multiprocessing.Queue()
        server = multiprocessing.Process(target=ssh_server.start_server,args=(q,))
        server.start()
        self.ssh_servers.append(server)
        server_port = q.get()
        return(server_port)

    def start_ssh_session(self,server_port=None,class_init={},connect_args={}):
        server_hostname = '127.0.0.1'
        if server_port==None:
            server_port = self.start_ssh_server()
        sshs = SSHSession(self.server_hostname,server_port,class_init,connect_args)
        self.ssh_sessions.append(sshs)
        return(sshs)

    def end_ssh_session(self,sshs):
        sshs.sendline('exit')
        sshs.wait_for('TEST')
        sshs.rs.exit()

    def tearDown(self):
        for session in self.ssh_sessions:
            self.end_ssh_session(session)
        for server in self.ssh_servers:
            server.kill()


    def test_basic_read_write(self):
        sshs = self.start_ssh_session()
        result = sshs.rs.command('reply',remove_newline=True)
        assert result=='PONG!'



if __name__ == '__main__':
    unittest.main()

