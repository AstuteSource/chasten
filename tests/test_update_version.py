import update_version


def test_updated_version() -> None:
    """Test case for update_version function"""
    assert update_version.updated_version("0.0.9") == "0.1.0"
    assert update_version.updated_version("0.9.9") == "1.0.0"
    assert update_version.updated_version("0.1.0") == "0.1.1"
