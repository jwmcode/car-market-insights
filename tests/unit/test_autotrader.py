from model.search_criteria import SearchCriteria
from autotrader.autotrader import Autotrader

sc = SearchCriteria('Ford', 'Fiesta', 'Zetec S', 2011, 2011, 'Manual', 'Petrol', 'Hatchback', 3,
                    'Front Wheel Drive', None)


def test_constructor():
    """ Tests Autorader constructor. """

    at1 = Autotrader(headless=True)
    assert at1._scraper._headless is True

    at2 = Autotrader(headless=False)
    assert at2._scraper._headless is False


def test_getvehicles():
    """ Tests Autotrader.get_vehicles() """

    datasrc = Autotrader(False)
    vehicles = datasrc.get_vehicles(sc)

    assert vehicles[0].make == 'Ford'
    assert vehicles[1].model == 'Fiesta'
    assert vehicles[2].variant == 'Zetec S'
    assert vehicles[3].year == 2011
    assert vehicles[4].gearbox == 'Manual'
    assert vehicles[5].fuel == 'Petrol'
    assert vehicles[6].body == 'Hatchback'
    assert vehicles[7].doors == 3
    assert vehicles[8].drivetrain == 'Front Wheel Drive'
    assert vehicles[9].fuel == 'Petrol'

    del datasrc
