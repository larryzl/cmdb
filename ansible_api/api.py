import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
import ansible.constants as C
import tempfile
import os,sys,stat



class AnsibleHost:
    def __init__(self, host, port=None, connection=None, ssh_user=None, ssh_pass=None,ssh_key=None):
        self.host = host
        self.port = port

        self.ansible_connection = connection
        self.ansible_ssh_user = ssh_user
        self.ansible_ssh_pass = ssh_pass
        self.ssh_key = ssh_key

    def __str__(self):
        result = str(self.host) + ' ansible_ssh_host=' + str(self.host)
        if self.port:
            result += ' ansible_ssh_port=' + str(self.port)
        if self.ansible_connection:
            result += ' ansible_connection=' + str(self.ansible_connection)
        if self.ansible_ssh_user:
            result += ' ansible_ssh_user=' + str(self.ansible_ssh_user)
        if self.ansible_ssh_pass:
            result += ' ansible_ssh_pass=' + str(self.ansible_ssh_pass)
        if self.ssh_key:
            result += ' ansible_ssh_private_key_file=' + str(self.ssh_key)
        return result

class ResultsCollector(CallbackBase):

    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.result = None
        self.error_msg = None
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result,  *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result,  *args, **kwargs):
        self.host_failed[result._host.get_name()] = result

class AnsibleRunner(object):
    def __init__(self,hosts):
        self.hosts = hosts

        self.hosts_file = None
        self._generate_hosts_file()

        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = ResultsCollector()
        self.__initializeData()
        self.results_raw = {}

    def __initializeData(self):
        '''
        初始化ansible
        :return:
        '''
        # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                              'diff', 'host_key_checking', 'listhosts', 'listtasks', 'listtags', 'syntax'])

        self.options = Options(connection='ssh', module_path=None, forks=10,
                               become=None, become_method=None, become_user=None, check=False, diff=False,
                               host_key_checking=False, listhosts=None, listtasks=None, listtags=None, syntax=None)

        PlaybookOptions = namedtuple('PlaybookOptions',['connection','listhosts','listtasks','listtags','syntax','module_path','become','become_method','become_user', 'check', 'diff','forks','host_key_checking'])

        self.playbookOptions = PlaybookOptions(connection='ssh',listhosts=None,listtasks=None,listtags=None,syntax=None,module_path=None,become=None,become_method=None,become_user=None, check=False, diff=False,forks=10,host_key_checking=False)


        # initialize needed objects
        self.loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
        self.passwords = dict(vault_pass='secret')

        # create inventory, use path to host config file as source or hosts in a comma separated string
        self.inventory = InventoryManager(loader=self.loader, sources=[self.hosts_file])
        # variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
        self.variable_manager = VariableManager(loader=self.loader,inventory=self.inventory)

    def _generate_hosts_file(self):
        self.hosts_file = tempfile.mktemp()
        # print(self.hosts_file)
        with open(self.hosts_file, 'w+', encoding='utf-8') as file:
            hosts = []
            i_temp = 0
            for host in self.hosts:
                hosts.append(str(host))
                i_temp += 1
            # print(hosts)
            file.write('\n'.join(hosts))
        # print(self.hosts_file)


    def exec_playbook(self, playbooks,args=None):
        playbook = PlaybookExecutor(playbooks=playbooks,inventory=self.inventory,
                                    variable_manager=self.variable_manager,loader=self.loader,options=self.playbookOptions,passwords=self.passwords)
        playbook.run()




    def run(self,module_name,module_args=''):
        play_source = {'hosts': 'all', 'gather_facts': 'no', 'tasks': [
            {'action': {'module': module_name, 'args': module_args}, 'register': 'shell_out'}]}

        # play_source = dict(
        #         name = "Ansible Play",
        #         hosts = "all",
        #         gather_facts = 'no',
        #         tasks = [
        #             dict(action=dict(module=module_name, args=module_args), register='shell_out')
        #          ]
        #     )

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=self.inventory,
                      variable_manager=self.variable_manager,
                      loader=self.loader,
                      options=self.options,
                      passwords=self.passwords,
                      stdout_callback=self.callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
                  )
            # tqm._stdout_callback = self.callback
            result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
        finally:
            # we always need to cleanup child procs and the structres we use to communicate with them
            if tqm is not None:
                tqm.cleanup()

            # Remove ansible tmpdir
            # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def get_result(self):
        self.results_raw = {'success':{}, 'failed':{}, 'unreachable':{}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result
        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result
        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host]= result._result['msg']

        #print "Ansible执行结果集:%s"%self.results_raw
        return self.results_raw

    def __del__(self):
        if self.hosts_file:
            os.remove(self.hosts_file)

def ansible_run(user_key,server_id,obj,module,args=None,playbook=None):
    host_list = []
    #- 创建临时ssh 秘钥文件
    ssh_keyfile = tempfile.mktemp()
    with open(ssh_keyfile, 'w+', encoding='utf-8') as file:file.write(user_key)
    os.chmod(ssh_keyfile,stat.S_IRUSR|stat.S_IWUSR)

    #- 通过uid获取服务器信息
    for uid in server_id.split(','):
        # print(uid)
        server_obj = obj.get(uuid=uid)
        host_list.append(
                AnsibleHost(host=server_obj.ip,port=server_obj.ssh_port,connection='ssh',ssh_user=server_obj.ssh_user,ssh_key=ssh_keyfile)
        )

    task = AnsibleRunner(host_list)
    if module == 'playbook':
        print(playbook)
        task.exec_playbook(playbook,args=args)
        result = {'unreachable': {}, 'failed': {}, 'success': {}}
    else:
        if not args:
            task.run(module)
        else:
            task.run(module,args)
        result = task.get_result()
        print(result)
    os.remove(ssh_keyfile)
    return result



if __name__ == "__main__":

    ssh_key = "/Users/lei/.ssh/id_rsa"
    host_dict = [
        {
            'host':'10.9.97.188',
            'port':22,
            'method':'ssh',
            'user':'root',
            'ssh_key':ssh_key
         },
    ]
    host_list = []

    for i in host_dict:
        host_list.append(AnsibleHost(host=i['host'],port=i['port'],connection=i['method'],ssh_user=i['user'],ssh_key=i['ssh_key']))

    task = AnsibleRunner(host_list)
    task.exec_playbook(["/Users/lei/ops/github/cmdb/ansible_api/test1.yaml"])
    # task.run('shell','w')
    # result = task.get_result()

    # a = AnsibleRunner()
    # 获取服务器磁盘信息
    # a.run('10.9.97.188', 'shell', "ifconfig eth0")
    #结果
    # result=a.get_result()
    #成功
    # succ = result['success']
    #失败
    # failed = result['failed']
    #不可到达
    # unreachable = result['unreachable']

    # print(succ)