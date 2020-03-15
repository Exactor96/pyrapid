import hashlib
import os


class Executor:
    def __init__(self, func, global_vars, local_vars, requirements='None'):
        self.func = func
        self.local_vars = local_vars
        self.global_vars = global_vars
        self.venvs_dir = 'venvs'
        for each in self.global_vars.items():
            setattr(self, each[0], each[1])
        self.result = None
        self.req = requirements
        self.env_name = hashlib.sha512(''.join(self.req).encode('utf-8')).hexdigest()

    def install_req(self):
        import subprocess
        for each in self.req:
            subprocess.run(self.env + f'-m pip3 install {each}')

    def change_env(self):
        env = os.path.join(self.venvs_dir, self.env_name, 'bin/activate')
        if os.path.exists(env):
            setattr(self, 'env', env)
        else:
            self.create_venv(self.env_name)
            setattr(self, 'env', env)

    def create_venv(self):
        import venv
        print(os.path.join(self.venvs_dir, self.env_name))
        venv.create(os.path.join(self.venvs_dir, self.env_name), with_pip=True)

    def run(self):
        self.result = self.func(*self.local_vars.get('args'), **self.local_vars.get('kwargs'))
