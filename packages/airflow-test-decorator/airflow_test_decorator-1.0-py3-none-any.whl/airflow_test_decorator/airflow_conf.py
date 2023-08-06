class AirflowConf:
    def __init__(self, dag_bag, env_path, variable_path):
        self.dag_bag = dag_bag
        self.env_path = env_path
        self.variable_path = variable_path