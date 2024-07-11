from sqlalchemy.orm import relationship

from web.app import db


class search_criteria(db.Model):
    """ SQLAlchemy model class for search_criteria data table. Class name not PascalCase as must match table name

    :param db.Model: baseclass for all SQLAlchemy model classes
    """

    id = db.Column(db.INTEGER, primary_key=True)
    make = db.Column(db.VARCHAR(32))
    model = db.Column(db.VARCHAR(32))
    variant = db.Column(db.VARCHAR(32))
    min_year = db.Column(db.INTEGER)
    max_year = db.Column(db.INTEGER)
    gearbox = db.Column(db.VARCHAR(32))
    fuel = db.Column(db.VARCHAR(32))
    body = db.Column(db.VARCHAR(32))
    doors = db.Column(db.INTEGER)
    drivetrain = db.Column(db.VARCHAR(32))
    keywords = db.Column(db.VARCHAR(32))
    sale_vehicles = relationship("sale_vehicle")

    def __init__(self, sc):
        """ Inits search_criteria object from model.SearchCriteria object.

        :param sc: model.SearchCriteria object
        """
        self.make = sc.make
        self.model = sc.model
        self.variant = sc.variant
        self.min_year = sc.min_year
        self.max_year = sc.max_year
        self.gearbox = sc.gearbox
        self.fuel = sc.fuel
        self.body = sc.body
        self.doors = sc.doors
        self.drivetrain = sc.drivetrain
        self.keywords = sc.keywords

    def __str__(self):
        """ Formats search_criteria properties into string.

        :return: string of search_criteria properties
        :rtype: str
        """
        string = f"{self.make} {self.model}"
        if self.variant:
            string += f" {self.variant}"
        if self.min_year:
            string += f", from {self.min_year}"
        if self.max_year:
            string += f", up to {self.max_year}"
        if self.gearbox:
            string += f", {self.gearbox}"
        if self.fuel:
            string += f", {self.fuel}"
        if self.body:
            string += f", {self.body}"
        if self.drivetrain:
            string += f", {self.drivetrain}"
        if self.doors:
            string += f", {self.doors} doors"
        if self.keywords:
            string += f", keywords: {self.keywords}"

        return f'{string}'
