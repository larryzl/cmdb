import os
import tempfile
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class AnsibleHost:
    def __init__(self, host, port=None, connection=None, ssh_user=None, ssh_pass=None):
        self.host = host
        self.port = port
        self.ansible_connection = connection
        self.ansible_ssh_user = ssh_user
        self.ansible_ssh_pass = ssh_pass

    def __str__(self):
        result = 'ansible_ssh_host=' + str(self.host)
        if self.port:
            result += ' ansible_ssh_port=' + str(self.port)
        if self.ansible_connection:
            result += ' ansible_connection=' + str(self.ansible_connection)
        if self.ansible_ssh_user:
            result += ' ansible_ssh_user=' + str(self.ansible_ssh_user)
        if self.ansible_ssh_pass:
            result += ' ansible_ssh_pass=' + str(self.ansible_ssh_pass)
        return result


class AnsibleTaskResultCallback(CallbackBase):
    def __init__(self, display=None, option=None):
        super().__init__(display, option)
        self.result = None
        self.error_msg = None

    def v2_runner_on_ok(self, result):
        res = getattr(result, '_result')
        self.result = res
        self.error_msg = res.get('stderr')

    def v2_runner_on_failed(self, result, ignore_errors=None):
        if ignore_errors:
            return
        res = getattr(result, '_result')
        self.error_msg = res.get('stderr', '') + res.get('msg')

    def runner_on_unreachable(self, host, result):
        if result.get('unreachable'):
            self.error_msg = host + ':' + result.get('msg', '')

    def v2_runner_item_on_failed(self, result):
        res = getattr(result, '_result')
        self.error_msg = res.get('stderr', '') + res.get('msg')


class AnsibleTask:
    def __init__(self, hosts, extra_vars=None):
        self.hosts = hosts
        self._validate()
        self.hosts_file = None
        self._generate_hosts_file()
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                              'diff', 'host_key_checking', 'listhosts', 'listtasks', 'listtags', 'syntax'])

        self.options = Options(connection='ssh', module_path=None, forks=10,
                               become=None, become_method=None, become_user=None, check=False, diff=False,
                               host_key_checking=False, listhosts=None, listtasks=None, listtags=None, syntax=None)
        self.loader = DataLoader()
        self.passwords = dict(vault_pass='secret')

        self.inventory = InventoryManager(loader=self.loader, sources=[self.hosts_file])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        if extra_vars:
            self.variable_manager.extra_vars = extra_vars

    def _generate_hosts_file(self):
        self.hosts_file = tempfile.mktemp()
        with open(self.hosts_file, 'w+', encoding='utf-8') as file:
            hosts = []
            i_temp = 0
            for host in self.hosts:
                hosts.append('server' + str(i_temp) + ' ' + str(host))
                i_temp += 1
            file.write('\n'.join(hosts))

    def _validate(self):
        if not self.hosts:
            raise Exception('hosts不能为空')
        if not isinstance(self.hosts, list):
            raise Exception('hosts只能为list<AnsibleHost>数组')
        for host in self.hosts:
            if not isinstance(host, AnsibleHost):
                raise Exception('host类型必须为AnsibleHost')

    def exec_shell(self, command):
        source = {'hosts': 'all', 'gather_facts': 'no', 'tasks': [
            {'action': {'module': 'shell', 'args': command}, 'register': 'shell_out'}]}
        play = Play().load(source, variable_manager=self.variable_manager, loader=self.loader)
        results_callback = AnsibleTaskResultCallback()
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=results_callback
            )
            tqm.run(play)
            if results_callback.error_msg:
                raise Exception(results_callback.error_msg)
            return results_callback.result
        except:
            raise
        finally:
            if tqm is not None:
                tqm.cleanup()

    def exec_playbook(self, playbooks):
        results_callback = AnsibleTaskResultCallback()
        playbook = PlaybookExecutor(playbooks=playbooks, inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.options, passwords=self.passwords)
        setattr(getattr(playbook, '_tqm'), '_stdout_callback', results_callback)
        playbook.run()
        if results_callback.error_msg:
            raise Exception(results_callback.error_msg)
        return results_callback.result

    def __del__(self):
        if self.hosts_file:
            os.remove(self.hosts_file)

if __name__ == "__main__":
    task = AnsibleTask([AnsibleHost('10.9.97.188', 22, 'ssh', 'root', '')])
    # task.exec_playbook(['/install.yml', 'init.yml'])
    resault = task.exec_shell('ifconfig eth0')
    print(resault)
