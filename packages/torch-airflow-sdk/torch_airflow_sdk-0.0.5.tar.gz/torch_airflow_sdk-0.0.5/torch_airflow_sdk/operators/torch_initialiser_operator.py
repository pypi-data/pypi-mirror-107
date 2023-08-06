from datetime import datetime
from airflow.models.baseoperator import BaseOperator
from torch_airflow_sdk.utils.torch_client import TorchDAGClient


class TorchInitializer(BaseOperator):
    """
    In airflow 2.0 , you need to add task with given operator at the root of your dag. This will create new pipeline
    run for your dag run. In airflow 1.0, its not needed. We've taken care inside our code. But for 2.0, you need to
    add it as a root of the dag. This is because of DAG serialization in version 2.0. So, to fulfill that requirement
    we need add additional operator for 2.0.
    """
    def __init__(self, *, pipeline_uid, **kwargs):
        """
        You need to add extra parameter pipeline uid. Other parameters will be same as std airflow base operator's parameters
        :param pipeline_uid: uid of the pipeline
        """
        super().__init__(**kwargs)
        self.pipeline_uid = pipeline_uid

    def execute(self, context):
        client = TorchDAGClient()
        pipeline_res = client.get_pipeline(self.pipeline_uid)
        pipeline_run = pipeline_res.create_pipeline_run()
        pipeline_run.create_span(uid=f'{self.pipeline_uid}.span', context_data={'time': str(datetime.now())})
