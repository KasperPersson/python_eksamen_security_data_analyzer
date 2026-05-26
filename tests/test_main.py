from unittest.mock import patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2024-01-01 00:00:00",
                    "2024-01-01 01:00:00",
                    "2024-01-01 01:30:00",
                    "2024-01-01 02:00:00",
                    "2024-01-02 00:00:00",
                    "2024-01-02 12:00:00",
                ]
            ),
            "source_ip": [
                "10.0.0.1",
                "10.0.0.2",
                "10.0.0.1",
                "10.0.0.3",
                "10.0.0.1",
                "10.0.0.2",
            ],  # noqa: E501
            "dest_ip": ["192.168.1.1"] * 6,
            "protocol": pd.Categorical(["TCP", "UDP", "TCP", "HTTP", "TCP", "UDP"]),
            "action": pd.Categorical(
                ["allowed", "blocked", "allowed", "blocked", "allowed", "allowed"]
            ),  # noqa: E501
            "threat_label": pd.Categorical(
                ["benign", "malicious", "benign", "suspicious", "benign", "malicious"]
            ),  # noqa: E501
            "log_type": pd.Categorical(["firewall"] * 6),
            "bytes_transferred": [100, 200, 150, 300, 50, 400],
            "user_agent": ["curl"] * 6,
            "request_path": ["/"] * 6,
        }
    )


@pytest.fixture
def client(sample_df):
    # Patch read_csv so the lifespan gets sample_df instead of the real CSV
    with patch("main.pd.read_csv", return_value=sample_df):
        with TestClient(app) as c:
            yield c


# parametrized: all GET endpoints return 200


@pytest.mark.parametrize(
    "url",
    [
        "/health",
        "/analysis/overview",
        "/analysis/top-ips",
        "/analysis/attack-distribution",
        "/analysis/timeline",
    ],
)
def test_endpoints_return_200(client, url):
    assert client.get(url).status_code == 200


# parametrized: invalid timeline interval returns 422


@pytest.mark.parametrize("interval", ["week", "minute", "abc"])
def test_timeline_rejects_invalid_interval(client, interval):
    assert client.get(f"/analysis/timeline?interval={interval}").status_code == 422


# structure assertions


def test_overview_total_rows_is_int(client):
    data = client.get("/analysis/overview").json()
    assert isinstance(data["total_rows"], int)
    assert data["total_rows"] == 6


def test_top_ips_n_param_limits_results(client):
    items = client.get("/analysis/top-ips?n=2").json()["items"]
    assert len(items) == 2


def test_attack_distribution_items_have_required_keys(client):
    items = client.get("/analysis/attack-distribution").json()["items"]
    assert isinstance(items, list)
    for item in items:
        assert "label" in item
        assert "count" in item
        assert "bytes_mean" in item


def test_timeline_interval_echoed_in_response(client):
    data = client.get("/analysis/timeline?interval=day").json()
    assert data["interval"] == "day"
    assert isinstance(data["items"], list)
