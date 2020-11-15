from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured

import pytest

from django_guid.config import Settings


def test_invalid_guid(monkeypatch):
    monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'VALIDATE_GUID': 'string'})
    with pytest.raises(ImproperlyConfigured, match='VALIDATE_GUID must be a boolean'):
        Settings().validate()


def test_invalid_header_name(monkeypatch):
    monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'GUID_HEADER_NAME': True})
    with pytest.raises(ImproperlyConfigured, match='GUID_HEADER_NAME must be a string'):
        Settings().validate()


def test_invalid_return_header_setting(monkeypatch):
    monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'RETURN_HEADER': 'string'})
    with pytest.raises(ImproperlyConfigured, match='RETURN_HEADER must be a boolean'):
        Settings().validate()


def test_invalid_expose_header_setting(monkeypatch):
    monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'EXPOSE_HEADER': 'string'})
    with pytest.raises(ImproperlyConfigured, match='EXPOSE_HEADER must be a boolean'):
        Settings().validate()


def test_valid_settings(monkeypatch):
    monkeypatch.setattr(
        django_settings,
        'DJANGO_GUID',
        {
            'VALIDATE_GUID': False,
            'GUID_HEADER_NAME': 'Correlation-ID-TEST',
            'RETURN_HEADER': False,
            'EXPOSE_HEADER': False,
        },
    )
    assert not Settings().validate_guid
    assert Settings().guid_header_name == 'Correlation-ID-TEST'
    assert not Settings().return_header


def test_bad_integrations_type(monkeypatch):
    for setting in [{}, '', 2, None, -2]:
        monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'INTEGRATIONS': setting})
        with pytest.raises(ImproperlyConfigured, match='INTEGRATIONS must be an array'):
            Settings().validate()


def test_not_array_ignore_urls(monkeypatch):
    for setting in [{}, '', 2, None, -2]:
        monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'IGNORE_URLS': setting})
        with pytest.raises(ImproperlyConfigured, match='IGNORE_URLS must be an array'):
            Settings().validate()


def test_not_string_in_igore_urls(monkeypatch):
    for setting in (['api/v1/test', 'api/v1/othertest', True], [1, 2, 'yup']):
        monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'IGNORE_URLS': setting})
        with pytest.raises(ImproperlyConfigured, match='IGNORE_URLS must be an array of strings'):
            Settings().validate()


def test_converts_correctly(monkeypatch):
    monkeypatch.setattr(django_settings, 'DJANGO_GUID', {'IGNORE_URLS': ['/no-guid', '/my/api/path/']})
    assert 'my/api/path' in Settings().ignore_urls
    assert 'no-guid' in Settings().ignore_urls
