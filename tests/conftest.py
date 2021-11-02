from unittest.mock import MagicMock

import pytest

pytest_plugins = "fw_http_testserver"


# Alias for http_testserver
@pytest.fixture
def api(http_testserver):
    return http_testserver


@pytest.fixture
def context_with_key(api):
    gear_context = MagicMock()
    gear_context.config_json = {"inputs": {"api-key": {"key": f"{api.url}:user"}}}

    return gear_context
