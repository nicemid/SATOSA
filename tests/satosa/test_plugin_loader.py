import json

import pytest
import yaml

from satosa.backends.base import BackendModule
from satosa.exception import SATOSAConfigurationError
from satosa.frontends.base import FrontendModule
from satosa.micro_services.base import RequestMicroService, ResponseMicroService
from satosa.plugin_loader import backend_filter, frontend_filter, _request_micro_service_filter, _response_micro_service_filter, _load_plugin_config


class TestFilters(object):
    class BackendTestPluginModule(BackendModule):
        pass

    class FrontendTestPluginModule(FrontendModule):
        pass

    class RequestTestMicroService(RequestMicroService):
        pass

    class ResponseTestMicroService(ResponseMicroService):
        pass

    def test_backend_filter_rejects_base_class(self):
        assert not backend_filter(BackendModule)

    def test_backend_filter_rejects_frontend_plugin(self):
        assert not backend_filter(TestFilters.FrontendTestPluginModule)

    def test_backend_filter_accepts_backend_plugin(self):
        assert backend_filter(TestFilters.BackendTestPluginModule)

    def test_frontend_filter_rejects_base_class(self):
        assert not frontend_filter(FrontendModule)

    def test_frontend_filter_rejects_backend_plugin(self):
        assert not frontend_filter(TestFilters.BackendTestPluginModule)

    def test_frontend_filter_accepts_backend_plugin(self):
        assert frontend_filter(TestFilters.FrontendTestPluginModule)

    def test_request_micro_service_filter_rejects_base_class(self):
        assert not _request_micro_service_filter(RequestMicroService)

    def test_request_micro_service_filter_rejects_response_micro_service(self):
        assert not _request_micro_service_filter(TestFilters.ResponseTestMicroService)

    def test_request_micro_service_filter_accepts_request_micro_service(self):
        assert _request_micro_service_filter(TestFilters.RequestTestMicroService)

    def test_response_micro_service_filter_rejects_base_class(self):
        assert not _response_micro_service_filter(ResponseMicroService)

    def test_response_micro_service_filter_rejects_request_micro_service(self):
        assert not _response_micro_service_filter(TestFilters.RequestTestMicroService)

    def test_response_micro_service_filter_accepts_response_micro_service(self):
        assert _response_micro_service_filter(TestFilters.ResponseTestMicroService)


class TestLoadPluginConfig(object):
    def test_load_json(self):
        data = {"foo": "bar"}
        config = _load_plugin_config(json.dumps(data))
        assert config == data

    def test_can_load_yaml(self):
        data = {"foo": "bar"}
        config = _load_plugin_config(yaml.dump(data, default_flow_style=False))
        assert config == data

    def test_handles_malformed_data(self):
        data = """{foo: bar"""  # missing closing bracket
        with pytest.raises(SATOSAConfigurationError):
            _load_plugin_config(data)
