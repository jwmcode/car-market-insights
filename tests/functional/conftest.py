import pytest

from web.app import db, app
from data.sale_vehicle import sale_vehicle as DBSaleVehicle
from data.search_criteria import search_criteria as DBSearchCriteria
from autotrader.autotrader import Autotrader
from model.search_criteria import SearchCriteria


@pytest.fixture
def client():
    """Pytest fixture setting up test Flask client."""

    app.config["TESTING"] = True
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():

        db.create_all()
        db.session.query(DBSearchCriteria).delete()
        db.session.query(DBSaleVehicle).delete()

        init_criteria = SearchCriteria(None, None, None, None, None, None, None, None, None, None, None)
        db_init_criteria = DBSearchCriteria(init_criteria)
        db.session.add(db_init_criteria)

        autotrader = Autotrader(False)
        svs = autotrader.get_vehicles(init_criteria, limit=25)
        for sv in svs:
            db_sale_vehicle = DBSaleVehicle(sv)  # covert sale vehicles to associated db models
            db_init_criteria.sale_vehicles.append(db_sale_vehicle)
            db.session.add(db_sale_vehicle)

        db.session.commit()

    yield client
