import json
from unittest.mock import patch

from chtools.perspective.cli import PerspectiveCliHandler
from chtools.perspective.data import Perspective


@patch('chtools.perspective.client.PerspectiveClient')
@patch('chtools.perspective.data.Perspective')
def test_create(mock_client, mock_perspective):
    mock_perspective.return_value.update_cloudhealth.return_value = True
    perspective = mock_perspective(None)
    perspective.name = 'tag_filter'
    perspective.id = '1234567890'

    mock_client.return_value.check_exists.return_value = False
    mock_client.return_value.create.return_value = perspective

    args = ['create', '--spec-file', 'tests/specs/tag_filter.yaml']
    handler = PerspectiveCliHandler(
        args,
        'fake_api_key',
        client=mock_client
    )
    handler.execute()
    assert handler._results == "Created Perspective tag_filter (https://apps.cloudhealthtech.com/perspectives/1234567890)"


@patch('chtools.perspective.client.PerspectiveClient')
def test_get_schema(mock_client):
    perspective = Perspective(None)
    perspective.schema = {'name': 'mocked'}

    mock_client.return_value.get.return_value = perspective

    args = ['get-schema', '--name', 'tag_filter']
    handler = PerspectiveCliHandler(
        args,
        'fake_api_key',
        client=mock_client
    )
    handler.execute()
    assert handler._results == json.dumps(perspective.schema, indent=4)
