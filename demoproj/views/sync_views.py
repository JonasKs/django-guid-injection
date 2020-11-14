import logging

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from demoproj.services.sync_services import useless_function

logger = logging.getLogger(__name__)


def index_view(request: HttpRequest) -> JsonResponse:
    """
    Example view that logs a log and calls a function that logs a log.

    :param request: HttpRequest
    :return: JsonResponse
    """
    logger.info('This log message should have a GUID')
    useless_response = useless_function()
    return JsonResponse({
                            'detail': f'It worked! Useless function response is {useless_response}'})


def no_guid(request: HttpRequest) -> JsonResponse:
    """
    Example view with a URL in the IGNORE_URLs list - no GUID will be in these logs
    """
    logger.info(
        'This log message should NOT have a GUID - the URL is in IGNORE_URLS')
    useless_response = useless_function()
    return JsonResponse({
                            'detail': f'It worked also! Useless function response is {useless_response}'})


@api_view(('GET',))
def rest_view(request: Request) -> Response:
    """
    Example DRF view that logs a log and calls a function that logs a log.

    :param request: Request
    :return: Response
    """
    logger.info('This is a DRF view log, and should have a GUID.')
    useless_response = useless_function()
    return Response(data={
        'detail': f'It worked! Useless function response is {useless_response}'})

@api_view(('GET',))
def celery_view(request: Request) -> Response:
    """
    Example view that triggers a Celery task.

    :param request: Req uest
    :return: Response
    """
    from demoproj.celery import debug_task
    logger.info('Celery view')
    debug_task.delay()
    return Response(status=HTTP_204_NO_CONTENT)
