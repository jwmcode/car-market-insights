from datetime import date
from sqlalchemy import ForeignKey

from web.app import db


class sale_vehicle(db.Model):

    """ SQLAlchemy model class for sale_vehicle data table.

    :param db.Model: baseclass for all SQLAlchemy model classes
    """

    id = db.Column(db.INTEGER, primary_key=True)
    search_criteria_id = db.Column(db.INTEGER, ForeignKey('search_criteria.id'))
    date = db.Column(db.DATE, nullable=False)
    make = db.Column(db.VARCHAR(32))
    price = db.Column(db.INTEGER, nullable=False)
    year = db.Column(db.INTEGER)
    body = db.Column(db.VARCHAR(32))
    mileage = db.Column(db.INTEGER)
    engine_size = db.Column(db.INTEGER)
    power = db.Column(db.INTEGER)
    gearbox = db.Column(db.VARCHAR(32))
    fuel = db.Column(db.VARCHAR(32))
    owners = db.Column(db.INTEGER)

    def __init__(self, sv):
        """ Inits sale_vehicle object from model.sale_vehicle.

        :param sv: model.SaleVehicle object
        """
        self.date = date.today()
        self.make = sv.make
        self.price = sv.price
        self.year = sv.year
        self.body = sv.body
        self.mileage = sv.mileage
        self.engine_size = sv.cc
        self.power = sv.power
        self.gearbox = sv.gearbox
        self.fuel = sv.fuel
        self.owners = sv.owners
