
from time import sleep
import os

import paramiko


current_directory = os.getcwd()


class Remote_operation():
    def __init__(self,MACHINE_INFO):
        self.ip=MACHINE_INFO["ip"]
        self.port=MACHINE_INFO["port"]
        self.username=MACHINE_INFO["username"]
        self.password=MACHINE_INFO["password"]
        self.sshClient = paramiko.SSHClient()
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshClient.connect(self.ip, port=self.port, username=self.username, password=self.password, allow_agent=False)
        self.sftp = self.sshClient.open_sftp()

    def exec_remote_shell(self,cmd):
        '''
        ssh 登录到指定 ip 上,执行命令然后返回执行结果
        :param cmd:
        :param ip:
        :param port:
        :param username:
        :param password:
        :return:
        '''

        stdin, stdout, stderr = self.sshClient.exec_command(cmd, timeout=10000)
        ret = stdout.read()
        ret = bytes.decode(ret)
        return ret

    def setting_up_simulation_service(self,response_data):
        cmd = """echo """ + '"' + str(response_data) + '"' + "> /tmp/response_data.txt"
        self.exec_remote_shell(cmd)


    def get_requestdate_from_simulatio_service(self):
        request_date = self.exec_remote_shell("cat /tmp/request_data.txt")
        request_date=request_date[:-1]
        return eval(request_date)


    def empty_request_data(self):
        cmd = 'echo not_data > /tmp/request_data.txt'
        self.exec_remote_shell(cmd)

    def ssh_scp_put(self,local_file,remote_file):
        """

        :param local_file:
        :param remote_file:
        :return:

        example : remote.ssh_scp_put("D:\\toutiaolog\\find\\xigualog_4184087elog_20191113181723.txt","/root/core/xigualog_4184087elog_20191113181723.txt")
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip,self.port, self.username, self.password)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)


    def ssh_scp_get(self,local_file, remote_file):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, self.port, self.username, self.password)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.get(remote_file, local_file)

    def does_the_query_log_exist(self, log_string, log_path):
        string = self.exec_remote_shell("cat " + log_path + "| grep " + log_string)
        if string:
            return True
        else:
            return False

    def clear_log(self,log_path_list):
        cmd_string = ""
        for log_path in  log_path_list:
            cmd_string = cmd_string + "echo '' > " + log_path+";"
        self.exec_remote_shell(cmd_string)


    def read_remote_log(self,log_path):
        """

        :param log_path:
        :return:
        """


class MockServerClass:
    """
    创建模拟服务  使用例子：
    mockserver = MockServer(mock_server_machine={"ip":"192.168.3.67","port":"22","username":"root","password":"jiexijiexi@@"},mock_server_port=82)
    mockserver.add_route(route_path="/upgcxcode/18/62/48856218/48856218-1-30015.m4s",response_status='200',response_headers='{"test_key":"test_value"}'
                         ,response_date='{"ok":true,"nodes":["http://192.168.6.135/upgcxcode/29/58/124945829/124945829_nb2-1-30032.m4s"]}')
    mockserver.start_mock_server()

    在 192.168.3.67 启动 一个模拟服务，模拟服务的接口是 /upgcxcode/18/62/48856218/48856218-1-30015.m4s，监听端口是 82，响应状态码是200，响应头包含 "test_key":"test_value"
    响应 内容 是 {"ok":true,"nodes":["http://192.168.6.135/upgcxcode/29/58/124945829/124945829_nb2-1-30032.m4s"]}

    """

    def __init__(self,mock_server_port,mock_server_log_path="request_data.txt",mock_server_machine=None):
        """

        :param mock_server_machine:     模拟服务器的登录信息   字典类型 如 {"ip":"192.168.3.67","port":"22","username":"root","password":"jiexijiexi@@"}
        :param mock_server_port:        模拟 服务器的监听端口号， 整形
        """
        self.route_code_list = []
        self.mock_server_machine = mock_server_machine
        self.mock_server_port = mock_server_port
        self.mock_server_log_path = mock_server_log_path

    def add_route(self,route_path,response_date="{}",response_status='200',response_headers='{}',response_contenttype="text",processing_time = '0.01'):
        """

        :param route_path:    模拟接口的请求路径           字符串类型
        :param response_date:  模拟接口的响应数据          字符串类型
        :param response_status: 响应状态码               字符串类型
        :param response_headers: 模拟服务器的响应头        字符串类型，字符串里的内容是一个字典 比如 '{"test_key":"test_value"}'
        :param response_contenttype:
        :param processing_time:                         字符串类型 指模拟服务器 特意 sleep 固定的时间，再返回数据
        :return:
        """
        get_request_data_code= 'str({"request_url": request_url, "request_method": request_method, "request_body": request_body,"request_headers": request_headers})'

        route_code = f"""@app.route('{route_path}',methods=["POST","GET","PURGE"])
def processing_requests(**args):
    request_method = request.method
    request_url = request.url
    request_headers = dict(request.headers)
    request_contenttype=request_headers.get("Content-Type","noexit")
    if request_method == "GET":
        request_body=request.args.to_dict()
    elif request_method=="POST":
        if request_contenttype.find("json")!=-1:
            request_body = request.json
        else:
            request_body = request.values.to_dict()

    request_data = {get_request_data_code}

    f=open('{self.mock_server_log_path}',"a")
    f.write((request_data))
    f.close()

    sleep_time = {processing_time}
    response_contenttype = "application/json"
    sleep(sleep_time)

    response_date = '''{response_date}'''
    response_status = {response_status}
    response_headers = {response_headers}

    resp = make_response(response_date,response_status)
    for key, values in response_headers.items():
        resp.headers[key] = values
    resp.headers["Content-Type"] = '{response_contenttype}'

    return resp
    """
        self.route_code_list.append(route_code)

    #立刻启动模拟服务
    def start_mock_server(self):
        route_code_string = "\n".join(self.route_code_list)
        flask_code = f"""
from flask import request,app,Flask,make_response
import logging
import json
from time import sleep
app=Flask(__name__)
{route_code_string}
if __name__=="__main__":
        f=open('{self.mock_server_log_path}',"w")
        f.close()
        app.run(host='0.0.0.0',port={self.mock_server_port})
        """
        with open("mock_server_code.py","w") as fp:
            fp.write(flask_code)

        if self.mock_server_machine:
            self.remote_operation = Remote_operation(self.mock_server_machine)
            self.remote_operation.ssh_scp_put("mock_server_code.py", "mock_server_code.py")
            self.stop_port_process()
            self.remote_operation.exec_remote_shell("nohup python mock_server_code.py > /dev/null   2>&1 &")
        else:
            os.system("python mock_server_code.py")
        sleep(4)

    #此函数用于,启动模拟服务之前,先把特定端口号的进程kill调
    def stop_port_process(self):
        stop_port_process_cmd = "netstat -ntlp | grep ':"+str(self.mock_server_port)+" '  |  awk '{print $7}' |  awk -F '/' '{print $1}' | xargs kill -9"
        self.remote_operation.exec_remote_shell(stop_port_process_cmd)

    def stop_mock_server(self):
        self.remote_operation.exec_remote_shell("ps -ef | grep mock_server_code.py | grep -v grep | awk '{print $2}' | xargs kill -9")

    #返回 模拟服务接收到的请求日志
    def get_mock_server_log_list(self):
        class Mock_server_log:
            def __init__(self, log_content):
                log_content_dict = eval(log_content)
                self.request_url = log_content_dict["request_url"]
                self.request_method = log_content_dict["request_method"]
                self.request_body = log_content_dict["request_body"]
                self.request_headers = log_content_dict["request_headers"]
        mock_server_log_list = []
        try:
            self.remote_operation.ssh_scp_get(local_file="request_data.txt", remote_file=self.mock_server_log_path)
        except FileNotFoundError:
            return []
        with  open("request_data.txt","r") as fp:
            for log in fp:
                if log in ['\n', '\r\n']:
                    continue
                mock_server_log = Mock_server_log(log)
                mock_server_log_list.append(mock_server_log)
        return mock_server_log_list


    def clear_mock_server_log(self):
        clear_log_cmd = f"echo '' > {self.mock_server_log_path}"
        self.remote_operation.exec_remote_shell(clear_log_cmd)



if __name__ == "__main__":
    mock_server_machine = {"ip": "192.168.3.61", "port": "22", "username": "root", "password": "jiexijiexi@@"}

    mockserver = MockServerClass(mock_server_port=8001)
    mockserver.add_route(route_path="/<path:path>", response_status='206',
                         response_headers='{"test_key":"test_value"}',
                         response_date='{"ok":true,"nodes":["http://192.168.6.135/upgcxcode/29/58/124945829/124945829_nb2-1-30032.m4s"]}')
    mockserver.start_mock_server()



