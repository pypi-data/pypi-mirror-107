import os
import unittest

from airflow.models import DagBag
from dotenv import load_dotenv

from airflow_snapshot_test.snapshot import AirflowSnapshotTest


class AirflowConf:
    def __init__(self, dag_bag, env_path, variable_path):
        self.dag_bag = dag_bag
        self.env_path = env_path
        self.variable_path = variable_path


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AirflowSuite(unittest.TestSuite, metaclass=SingletonMeta):

    def initializeAirflow(self, conf: AirflowConf):
        load_dotenv(conf.env_path)
        os.system("airflow initdb")
        os.system(f"airflow variables -i {conf.variable_path}")
        self._dagbag = DagBag(dag_folder=conf.dag_bag, include_examples=False)
        print("Successful Initialized")

    def __init__(self, conf: AirflowConf, *args, **kwargs):
        self.initializeAirflow(conf)
        super(AirflowSuite, self).__init__(*args, **kwargs)

    def reset_tests(self):
        for index in range(len(self._tests)):
            self._tests.pop()

    @property
    def dagbag(self):
        return self._dagbag

    @dagbag.setter
    def dagbag(self, value):
        self._dagbag = value


def airflow_test_runner(conf: AirflowConf, *args, **kwargs):
    dag_id = kwargs.get('dag_id', '')
    airflow_suite = AirflowSuite(conf)
    airflow_suite.reset_tests()

    def airflow_test_executor(Cls):
        Cls.dagbag = airflow_suite.dagbag
        if dag_id:
            _generate_snapshot(Cls, dag_id)
        airflow_suite.addTest(unittest.makeSuite(Cls))
        return Cls

    def _generate_snapshot(Cls: AirflowSnapshotTest, dag_id):
        setattr(Cls, f"test_match_snapshot_{dag_id}", lambda Cls: Cls.assert_snapshot(Cls.dagbag.get_dag(dag_id)))

    return airflow_test_executor
