import functools
import logging
from datetime import datetime
from torch_airflow_sdk.utils.torch_client import TorchDAGClient
from torch_sdk.events.generic_event import GenericEvent

LOGGER = logging.getLogger("airflow.task")


def span(span_uid, pipeline_uid):
    """
    Description:
        Used to decorate function for which you need span in side your pipeline. Just decorate your function with `span`
    :param span_uid: uid of the span
    :param pipeline_uid: uid of the pipeline

    Example:

    @span(span_uid='customer.orders.datagen.span', pipeline_uid='customer.orders.monthly.agg.demo' )
    def function(**context)

    """
    def decorator_span(func):
        @functools.wraps(func)
        def wrapper_span(*args, **kwargs):
            span_context = None
            try:
                LOGGER.info("Sending Span Start Event")
                task_instance = kwargs['ti']
                parent_span_context = task_instance.xcom_pull(key='parent_span_context')
                if parent_span_context is None:
                    LOGGER.debug('sending new request to catalog to get parent span context')
                    client = TorchDAGClient()
                    parent_span_context = client.get_parent_span(pipeline_uid=pipeline_uid,
                                                                 parent_span_uid=f'{pipeline_uid}.span')
                    task_instance.xcom_push(key="parent_span_context", value=parent_span_context)
                else:
                    LOGGER.debug('using xcom to get parent span context to send span event')

                span_context = parent_span_context.create_child_span(uid=span_uid,
                                                                     context_data={'time': str(datetime.now())})
                kwargs['span_context_parent'] = span_context
                func(*args, **kwargs)
            except Exception as e:
                LOGGER.error("Sending Span End Event With Status Failure")
                exception = e.__dict__
                LOGGER.error(exception)
                span_context.send_event(
                    GenericEvent(context_data={'status': 'error', 'error_data': str(e), 'time': str(datetime.now()),
                                               'exception_type': str(type(e).__name__)},
                                 event_uid=f'{span_uid}.error.event'))
                span_context.abort(
                    context_data={'span_status': 'error', 'time': str(datetime.now())})
                raise e
            else:
                LOGGER.info("Sending Span End Event With Status Success")
                span_context.end(context_data={'span_status': 'success', 'time': str(datetime.now())})

        return wrapper_span

    return decorator_span
