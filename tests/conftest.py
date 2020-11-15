import uuid
from copy import deepcopy

from django.conf import settings as django_settings

import pytest


@pytest.fixture
def mock_uuid(monkeypatch):
    class MockUUid:
        hex = '704ae5472cae4f8daa8f2cc5a5a8mock'

    monkeypatch.setattr('django_guid.utils.uuid.uuid4', MockUUid)


@pytest.fixture
def two_unique_uuid4():
    return ['704ae5472cae4f8daa8f2cc5a5a8mock', 'c494886651cd4baaa8654e4d24a8mock']


@pytest.fixture
def mock_uuid_two_unique(monkeypatch, mocker, two_unique_uuid4):
    mocker.patch.object(
        uuid.UUID,
        'hex',
        new_callable=mocker.PropertyMock,
        side_effect=two_unique_uuid4,
    )


def override(name, value):
    s = django_settings.DJANGO_GUID
    s[name] = value
    return s
