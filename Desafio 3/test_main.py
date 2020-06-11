from main import get_temperature
import pytest
from mock import patch


@pytest.mark.parametrize("lag, lng, expected", [(-14.235004, -51.92528, 16)])
def test_get_temperature_by_lat_lng(lag, lng, expected):
    temp_json = {"currently": {"temperature": 62}}
    mock_patch = patch("main.requests.get")
    mock_value = mock_patch.start()
    mock_value.return_value.json.return_value = temp_json
    temp = get_temperature(lag, lng)
    mock_patch.stop()
    assert temp == expected, "Temperature was {}".format(temp)