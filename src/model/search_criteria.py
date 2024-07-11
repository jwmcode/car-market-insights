class SearchCriteria:
    """ Class to represent search criteria for specific vehicle. """

    def __init__(self, make, model, variant, min_year, max_year, gearbox, fuel, body, doors, drivetrain, keywords):
        """ Inits SearchCriteria with various criteria that could specify a vehicle.

        :param make: string, e.g. BMW
        :param model: string, e.g. 3 series
        :param variant: string, e.g. 320d
        :param min_year: int, model year from
        :param max_year: int, model year to
        :param gearbox: string
        :param fuel: string
        :param body: string
        :param doors: int
        :param drivetrain: string, e.g. Four Wheel Drive
        :param keywords: string, e.g. specific trim level
        """

        self.make = make
        self.model = model
        self.variant = variant
        self.min_year = min_year
        self.max_year = max_year
        self.gearbox = gearbox
        self.fuel = fuel
        self.body = body
        self.drivetrain = drivetrain
        self.doors = doors
        self.keywords = keywords

    @classmethod
    def from_db(cls, db_sc):
        """ Factory method creating equivalent model.SearchCriteria from SQLAlchemy model.

        :param db_sc: data.SearchCriteria object
        :return: model.SearchCriteria object
        """

        make = db_sc.make
        model = db_sc.model
        variant = db_sc.variant
        min_year = db_sc.min_year
        max_year = db_sc.max_year
        gearbox = db_sc.gearbox
        fuel = db_sc.fuel
        body = db_sc.body
        doors = db_sc.doors
        drivetrain = db_sc.drivetrain
        keywords = db_sc.keywords

        return cls(make, model, variant, min_year, max_year, gearbox, fuel, body, doors, drivetrain, keywords)


    def __str__(self):
        """ Formats SearchCriteria attributes into string.

        :return: string of SearchCritria attributes
        :rtype: str
        """

        string = f""
        if self.make:
            string += f"{self.make}"
        if self.model:
            string += f" {self.model}"
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
