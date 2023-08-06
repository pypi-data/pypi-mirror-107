# pylint: disable=super-with-arguments
# pylint: disable=redefined-builtin
# pylint: disable=invalid-name

"""
    ATHENA TASK CODE
        - these are used in pythonOperator steps as a way \
            to flexibly call boto3 and perform any special requirements
"""
import logging

import boto3
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

logger = logging.getLogger(None)


class StartQueryExecution(BaseOperator):
    """Runs athena query against feature store."""
    template_fields = ('config',)

    @apply_defaults
    def __init__(self, config, *args, **kwargs):
        super(StartQueryExecution, self).__init__(*args, **kwargs)
        self.config = config

    def execute(self, context):
        """
            https://sagemaker.readthedocs.io/en/stable/api/\
                prep_data/feature_store.html#sagemaker.feature_store.feature_group.AthenaQuery
        """
        # init boto session and sagemaker
        BOTO_SESSION = boto3.Session()
        ATHENA_CLIENT = BOTO_SESSION.client('athena')

        try:
            response = ATHENA_CLIENT.start_query_execution(
                QueryString=self.config['query'],
                QueryExecutionContext=self.config.get('query_execution_context', {}),
                ResultConfiguration=self.config['result_configuration'],
                WorkGroup=self.config['workgroup']
            )

            context['task_instance'].xcom_push(
                key='athena_query_execution_id',
                value=response['QueryExecutionId']
            )

        except Exception as err:
            raise err


class GetQueryExecution(BaseOperator):
    """Runs athena query against feature store."""
    template_fields = ('config', 'xcom_tasks',)

    @apply_defaults
    def __init__(self, config, xcom_tasks=None, *args, **kwargs):
        super(GetQueryExecution, self).__init__(*args, **kwargs)

        self.config = config
        self.xcom_tasks = xcom_tasks

    def execute(self, context):
        """
            https://sagemaker.readthedocs.io/en/stable/api/\
                prep_data/feature_store.html#sagemaker.feature_store.feature_group.AthenaQuery
        """
        # init boto session and sagemaker
        BOTO_SESSION = boto3.Session()
        ATHENA_CLIENT = BOTO_SESSION.client('athena')

        try:

            query_execution_id = self.config.get('query_execution_id', None)
            task_ids = self.xcom_tasks['query_execution_id']['task_id']

            if query_execution_id is None:
                query_execution_id = context['task_instance'].xcom_pull(
                    task_ids=task_ids,
                    key=self.xcom_tasks['query_execution_id']['key']
                )

            logging.info("With query_id = {}\n".format(query_execution_id))

            # loop while results completing
            # on complete, do training next
            response = ATHENA_CLIENT.get_query_execution(
                QueryExecutionId=query_execution_id
            )
            query_execution_response = response.get('QueryExecution', {})
            job_state = query_execution_response.get('Status', {}).get('State', None)
            reason = query_execution_response.get('Status', {}).get('StateChangeReason', None)
            output_location = query_execution_response.get(
                'ResultConfiguration', {}).get('OutputLocation', None)
            # push response up
            context['task_instance'].xcom_push(
                key='output_location',
                value=output_location
            )

            if job_state == 'SUCCEEDED':
                return True
            elif job_state in ['QUEUED', 'RUNNING']:
                return False
            else:
                # retry on failure
                raise Exception(
                    "query status == {job_state} with reason = {reason}".format(
                        job_state=job_state, reason=reason
                    )
                )

        except Exception as err:
            raise err
