from model.search_criteria import SearchCriteria
from autotrader.scraper import Scraper

scrapey = Scraper(driver='chrome', headless=False)


def test_constructor():
    assert scrapey._driver_type == 'chrome'
    assert scrapey._headless == False


def test_make_driver():
    scrapey._make_driver()
    assert scrapey._driver is not None
    scrapey.__del__()


def test_get_sale_vehicles():
    """ Tests the get_sale_vehicles() method of the Scraper class """

    # Keywords not included as may make search too specfiic to yield 10 results
    sc = SearchCriteria('Ford', 'Fiesta', 'Zetec S', 2011, 2011, 'Manual', 'Petrol', 'Hatchback', 3,
                        'Front Wheel Drive', None)
    scrapey = Scraper(driver='chrome', headless=False)
    vehicles = scrapey.get_sale_vehicles(sc, 10, postcode='NR22PP')

    assert len(vehicles) == 10
    for v in vehicles:
        # set from attributes of SearchCriteria sc used to create each sale vehicle
        assert v.make == 'Ford'
        assert v.model == 'Fiesta'
        assert v.variant == 'Zetec S'
        assert v.year == 2011
        assert v.gearbox == 'Manual'
        assert v.fuel == 'Petrol'
        assert v.body == 'Hatchback'
        assert v.doors == 3
        assert v.drivetrain == 'Front Wheel Drive'
        assert v.fuel == 'Petrol'
        # attributes scraped from autotrader. all vehicles on autotrader.com have these attributes so should not be none
        assert v.price is not None
        assert v.mileage is not None

    scrapey.__del__()
