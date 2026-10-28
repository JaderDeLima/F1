import responses

from f1.cli import main
from f1.config import BASE_URL

URL = f"{BASE_URL}/car_data"
RECORD = {
    "date": "2023-09-15T13:08:19.923000+00:00",
    "session_key": 9159,
    "meeting_key": 1219,
    "driver_number": 55,
    "n_gear": 8,
    "speed": 315,
    "rpm": 11141,
    "throttle": 99,
    "brake": 0,
    "drs": 12,
}


@responses.activate
def test_main_ok(capsys):
    responses.get(URL, json=[RECORD])
    code = main(["--driver", "55", "--session", "9159", "--min-speed", "315"])
    assert code == 0
    assert "1 registros; velocidade máxima: 315" in capsys.readouterr().out


@responses.activate
def test_main_error(capsys):
    responses.get(URL, status=500)
    assert main(["--driver", "55", "--session", "9159"]) == 1
    assert "Erro" in capsys.readouterr().err
