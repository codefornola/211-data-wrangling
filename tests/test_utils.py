from cleanup.utils import get_lat, get_lng


def test_get_lat():
    assert isinstance(get_lat("70471"), float)  # valid zip
    assert get_lat("00000") is None             # invalid zip
    assert get_lat(None) is None                # null zip


def test_get_lng():
    assert isinstance(get_lng("70471"), float)  # valid zip
    assert get_lng("00000") is None             # invalid zip
    assert get_lng(None) is None                # null zip
