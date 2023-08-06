from airflow_test_decorator.airflow_conf import AirflowConf
from airflow_test_decorator.airflow_context import AirflowContext
from airflow_test_decorator.snapshot import AirflowSnapshotTest


def airflow_test_context(conf: AirflowConf, snapshot_test_dag_id=None):
    airflow_context = AirflowContext(conf)

    def _add_snapshot_test_to_class(Cls: AirflowSnapshotTest, dag_id):
        setattr(Cls, f"test_airflow_snapshot_for_{dag_id}",
                lambda snapshot_test: snapshot_test.assert_snapshot(Cls.dagbag.get_dag(dag_id)))

    def add_dag_bag_to_test(test_class):
        test_class.dagbag = airflow_context.dagbag
        if snapshot_test_dag_id:
            _add_snapshot_test_to_class(test_class, snapshot_test_dag_id)
        return test_class

    return add_dag_bag_to_test
