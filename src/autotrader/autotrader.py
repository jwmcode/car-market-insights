from autotrader.scraper import Scraper
from model.search_criteria import SearchCriteria


class Autotrader:
    """ Class to represent AutoTrader data source. """

    def __init__(self, headless=False):
        """ Constructor for AutoTrader, inits with new Scraper.

        :param headless: bool, whether Scraper will run in headless browser or not
        """
        self._scraper = Scraper(headless=headless)

    def get_vehicles(self, criteria, limit=250):
        """ Retrieves list of SaleVehicles from autotrader.com based on input SearchCriteria.

        :param criteria: SearchCriteria object
        :param limit: int, the maximum number of SaleVehicles to be returned in a list
        :return: SaleVehicles retrieved by the Scraper
        :rtype: List[SaleVehicle]
        """

        return self._scraper.get_sale_vehicles(criteria, limit)


if __name__ == '__main__':
    data_src = Autotrader(False)

    MAKE = 'Ford'
    MODEL = 'Fiesta'
    VARIANT = None
    MIN_YEAR = None
    MAX_YEAR = None
    GEARBOX = None # Manual or Automatic
    # Fuel = Petrol, Diesel, Bi Fuel, Electric, Hybrid-Diesel/Electric, Hybrid – Diesel/Electric Plug-in,
    # Hybrid – Petrol/Electric, Hybrid – Petrol/Electric Plug-in
    FUEL = None
    DOORS = None  # 0, 2, 3, 4, 5 or 6
    DRIVETRAIN = None  # Front Wheel Drive, Rear Wheel Drive, Four Wheel Drive
    BODY = None  # Camper, Convertible, Coupe, Estate, Hatchback, MPV, Other, Panel Van, Pickup, SUV, Saloon
    KEYWORDS = None

    vehicles = data_src.get_vehicles(SearchCriteria(MAKE, MODEL, VARIANT, MIN_YEAR, MAX_YEAR, GEARBOX, FUEL, BODY,
                                                    DOORS, DRIVETRAIN, KEYWORDS), limit=25)

    del data_src  # to cleanup web driver

    for v in vehicles:
        print(str(v))
