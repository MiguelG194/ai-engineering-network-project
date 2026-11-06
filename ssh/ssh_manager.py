import paramiko

class SSHManager:
    def __init__(self, configs):
        self.configs = configs
        self.connections = {}

    def connect(self, name):
        config = self.configs[name]

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname=config.host,
            username=config.username,
            password=config.password
        )

        self.connections[name] = client

    def get_connection(self, name):
        return self.connections[name]

    def run_command(self, name, command):
        if name not in self.connections:
            raise ConnectionError(f"{name} is not connected")

        client = self.connections[name]

        stdin, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()
        exit_code = stdout.channel.recv_exit_status()

        return {
            "output": output,
            "error": error,
            "exit_code": exit_code
        }

    def disconnect(self, name):
        if name in self.connections:
            self.connections[name].close()
            del self.connections[name]

    def disconnect_all(self):
        for name in list(self.connections):
            self.disconnect(name)