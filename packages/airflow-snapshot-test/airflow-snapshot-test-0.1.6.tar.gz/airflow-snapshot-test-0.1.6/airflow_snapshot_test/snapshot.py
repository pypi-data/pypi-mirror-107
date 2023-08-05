import unittest
import json, os
from airflow import DAG


class AirflowSnapshotTest(unittest.TestCase):
    def assert_snapshot(self, dag: DAG):
        try:
            with open(AirflowSnapshot.snapshot_file_path(dag)) as json_file:
                snapshot = json.loads(json_file.read())
            if self._validate_snapshot(snapshot, dag):
                print(f"{dag.dag_id} snapshot validation passed!!!")
        except IOError:
            print(f'No snapshot file found for <{dag.dag_id}>')
            AirflowSnapshot.generate_snapshot(dag)
            print(f'Generated Snapshot file <{AirflowSnapshot.snapshot_file_path(dag)}>!!!')

    def _validate_snapshot(self, snapshot, actual_dag: DAG):
        self.assertEqual(snapshot['dag_id'], actual_dag.dag_id,
                         f"Dag id doesn't match for {AirflowSnapshot.snapshot_file_name(actual_dag)}")
        self.assertEqual(snapshot['task_count'], actual_dag.task_count, f"Count mismatch in dag {actual_dag.dag_id}")
        self._validate_downstream_exist(snapshot, actual_dag)
        self.assertFalse(self._validate_task_inter_dependency(snapshot))

    def _validate_task_inter_dependency(self, snapshot: json):
        for key, value in snapshot['tasks'].items():
            if key in value:
                return True
        return False

    def _validate_downstream_exist(self, snapshot, actual_dag):
        for task in snapshot['tasks'].keys():
            try:
                downstream = actual_dag.get_task(task).downstream_task_ids
                self.assertEqual(list(sorted(downstream)), sorted(snapshot['tasks'][task]),
                                 f" \n Dependency mismatch in dag <<<{actual_dag.dag_id}>>> for task {task}:"
                                 f"\n actual: {list(sorted(downstream))} \n expected: {sorted(snapshot['tasks'][task])} ")
            except:
                self.assertTrue(False, f"Task {task} not found in dag {actual_dag.dag_id}")


class AirflowSnapshot:
    __snapshot_base_path = os.getcwd() + "/__snapshot__"

    @classmethod
    def generate_snapshot(cls, dag: DAG):
        os.makedirs(cls.__snapshot_base_path, exist_ok=True)
        dag_snapshot_dict = {"dag_id": dag.dag_id, "task_count": len(dag.tasks), 'tasks': {}}
        task_list = list(map(lambda task: task, dag.tasks))
        for task in task_list:
            downstream_task_list = task.downstream_task_ids
            dag_snapshot_dict['tasks'][task.task_id] = sorted(downstream_task_list)
        f = open(cls.snapshot_file_path(dag), 'w+')
        f.write(json.dumps(dag_snapshot_dict, indent=2))
        f.close()
        return dag_snapshot_dict

    @classmethod
    def snapshot_file_name(cls, dag: DAG): return f"snapshot-{dag.dag_id}.json"

    @classmethod
    def snapshot_file_path(cls, dag: DAG): return f'{cls.__snapshot_base_path}/{cls.snapshot_file_name(dag)}'
