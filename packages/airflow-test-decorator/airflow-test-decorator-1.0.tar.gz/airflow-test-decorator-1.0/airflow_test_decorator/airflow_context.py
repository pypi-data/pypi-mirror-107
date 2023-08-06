import os

from airflow.models import DagBag
from dotenv import load_dotenv

from airflow_test_decorator.airflow_conf import AirflowConf


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class AirflowContext(metaclass=SingletonMeta):

    def __init__(self, conf: AirflowConf, *args, **kwargs):
        load_dotenv(conf.env_path)
        os.system("airflow initdb")
        os.system(f"airflow variables -i {conf.variable_path}")
        self._dagbag = DagBag(dag_folder=conf.dag_bag, include_examples=False)

    @property
    def dagbag(self):
        return self._dagbag

    @dagbag.setter
    def dagbag(self, dagbag):
        self._dagbag = dagbag