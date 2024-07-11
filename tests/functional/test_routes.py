def test_home(client):
    """Tests whether home page loads correctly."""

    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Auto Trends" in response.data


def test_create_search(client):
    """Tests whether /createSearch loads correctly."""

    response = client.get("/createSearch")
    assert response.status_code == 200
    assert b"Track and forecast vehicle prices" in response.data

    response = client.get("/createSearch")
    assert response.status_code == 200
    assert b"Track and forecast vehicle prices" in response.data


def test_search_info(client):
    """Tests invalid search_ids in /searchInfo route."""

    response = client.get("/searchInfo/1")  # id used for home pages visualisations and prediction so should 404
    assert response.status_code == 404

    response = client.get("/searchInfo/2")  # does not exist so 404
    assert response.status_code == 404


def test_valuation_info(client):
    """Tests whether /valuationInfo loads correctly."""

    response = client.get("/valuationInfo?year=2015&mileage=30000")  # valid params
    assert response.status_code == 200
    assert b"Decision tree" in response.data


def test_valuation(client):
    """Tests whether /valuationInfo loads correctly."""

    response = client.get("/valuation")
    assert response.status_code == 200
    assert b"Get a vehicle valuation" in response.data
