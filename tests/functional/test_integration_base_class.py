from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

import pytest
from tests.conftest import override

from django_guid.config import Settings


def test_missing_identifier(monkeypatch):
    """
    Tests that an exception is raised when identifier is missing.
    """
    from django_guid.integrations import SentryIntegration

    monkeypatch.setattr(SentryIntegration, 'identifier', None)
    with pytest.raises(ImproperlyConfigured, match='`identifier` cannot be None'):
        SentryIntegration()


def test_run_method_not_accepting_kwargs(monkeypatch, client):
    """
    Tests that an exception is raised when the run method doesn't accept kwargs.
    """
    from django.conf import settings

    from django_guid.config import Settings
    from django_guid.integrations import SentryIntegration

    class BadIntegration(SentryIntegration):
        def run(self, guid):
            pass

    monkeypatch.setattr(settings, 'DJANGO_GUID', {'INTEGRATIONS': [BadIntegration()]})
    with pytest.raises(ImproperlyConfigured, match='Integration method `run` must accept keyword arguments '):
        Settings().validate()


def test_cleanup_method_not_accepting_kwargs(monkeypatch, client):
    """
    Tests that an exception is raised when the run method doesn't accept kwargs.
    """
    from django_guid.config import Settings
    from django_guid.integrations import SentryIntegration

    class BadIntegration(SentryIntegration):
        def cleanup(self, guid):
            pass

    with override_settings(**override('INTEGRATIONS', [BadIntegration()])):
        with pytest.raises(ImproperlyConfigured, match='Integration method `cleanup` must accept keyword arguments '):
            Settings().validate()


def test_non_callable_methods(monkeypatch, subtests):
    """
    Tests that an exception is raised when any of the integration base methods are non-callable.
    """
    from django.conf import settings

    from django_guid.config import Settings
    from django_guid.integrations import SentryIntegration

    mock_integration = SentryIntegration()

    to_test = [
        {
            'function_name': 'cleanup',
            'error': 'Integration method `cleanup` needs to be made callable for `SentryIntegration`.',
        },
        {
            'function_name': 'run',
            'error': 'Integration method `run` needs to be made callable for `SentryIntegration`.',
        },
        {
            'function_name': 'setup',
            'error': 'Integration method `setup` needs to be made callable for `SentryIntegration`.',
        },
    ]

    for test in to_test:
        setattr(mock_integration, test.get('function_name'), 'test')
        monkeypatch.setattr(settings, 'DJANGO_GUID', {'INTEGRATIONS': [mock_integration]})
        with subtests.test(msg=f'Testing function {test.get("function_name")}'):
            with pytest.raises(ImproperlyConfigured, match=test.get('error')):
                Settings().validate()


def test_base_class():
    """
    Test that a basic implementation of an integration works as expected.
    """
    from django_guid.integrations import Integration

    class MyCustomIntegration(Integration):
        identifier = 'My custom integration'

        def run(self, guid, **kwargs):
            pass

        def cleanup(self, **kwargs):
            pass

    stub_integration = MyCustomIntegration()
    assert stub_integration.setup() is None
    assert stub_integration.run('test') is None
    assert stub_integration.cleanup() is None
