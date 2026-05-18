from xybook_common.config import ServiceSettings


def test_default_settings():
    s = ServiceSettings()
    assert s.service_name == "xybook"
    assert s.service_port == 8000


def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("XYBOOK_SERVICE_NAME", "test-svc")
    monkeypatch.setenv("XYBOOK_SERVICE_PORT", "9999")
    s = ServiceSettings()
    assert s.service_name == "test-svc"
    assert s.service_port == 9999
