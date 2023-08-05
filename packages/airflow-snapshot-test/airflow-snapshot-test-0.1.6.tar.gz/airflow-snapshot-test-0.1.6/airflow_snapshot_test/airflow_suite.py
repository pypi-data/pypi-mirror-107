import os
import unittest

from airflow.models import DagBag
from dotenv import load_dotenv

from airflow_snapshot_test.snapshot import AirflowSnapshotTest


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AirflowSuite(unittest.TestSuite, metaclass=SingletonMeta):

    def initializeAirflow(self):
        print("Initializing", self.env_path, self.variable_path)
        print(os.getcwd())
        load_dotenv(self.env_path)
        os.system("env")
        os.system("airflow initdb")
        print("Airflow init done")
        os.system(f"airflow variables -i {self.variable_path}")
        print("Variable imported")
        self._dagbag = DagBag(dag_folder=self.dag_bag, include_examples=False)
        print(self._dagbag.dag_ids)
        print("Successful Initialized")

    def __init__(self, *args, **kwargs):
        self.dag_bag = kwargs['dag_bag']
        self.env_path = kwargs['env_path']
        self.variable_path = kwargs['variable_path']
        self.initializeAirflow()
        kwargs.pop('env_path')
        kwargs.pop('dag_bag')
        kwargs.pop('variable_path')
        super(AirflowSuite, self).__init__(*args, **kwargs)

    def reset_tests(self):
        for index in range(len(self._tests)):
            self._tests.pop()

    @property
    def dagbag(self):
        print("return dagbag", self._dagbag.dag_ids)
        return self._dagbag

    @dagbag.setter
    def dagbag(self, value):
        self._dagbag = value


def airflow_test_runner(*args, **kwargs):
    dag_bag = kwargs.get('dag_bag', '')
    env_path = kwargs.get('env_path', '')
    variable_path = kwargs.get('variable_path', '')
    dag_id = kwargs.get('dag_id', '')
    airflow_suite = AirflowSuite(dag_bag=dag_bag, env_path=env_path, variable_path=variable_path)
    airflow_suite.reset_tests()

    def airflow_test_executor(Cls):
        Cls.dagbag = airflow_suite.dagbag
        if dag_id:
            _generate_snapshot(Cls, dag_id)
        airflow_suite.addTest(unittest.makeSuite(Cls))
        runner = unittest.TextTestRunner()
        runner.run(airflow_suite)

        class EmptyClass(unittest.TestCase):
            pass

        return EmptyClass

    def _generate_snapshot(Cls: AirflowSnapshotTest, dag_id):
        setattr(Cls, f"test_match_snapshot_{dag_id}", lambda Cls: Cls.assert_snapshot(Cls.dagbag.get_dag(dag_id)))

    return airflow_test_executor
