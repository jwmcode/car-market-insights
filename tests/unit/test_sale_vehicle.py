from model.sale_vehicle import SaleVehicle
from model.search_criteria import SearchCriteria

sc = SearchCriteria('Ford', 'Fiesta', 'Zetec S', 2011, 2011, 'Manual', 'Petrol', 'Hatchback', 3,
                    'Front Wheel Drive', None)
sv = SaleVehicle(sc)


def test_constructor():
    """ Tests model.Salevehicle.__init()__. """

    assert sv.make == 'Ford'
    assert sv.model == 'Fiesta'
    assert sv.variant == 'Zetec S'
    assert sv.gearbox == 'Manual'
    assert sv.fuel == 'Petrol'
    assert sv.body == 'Hatchback'
    assert sv.drivetrain == 'Front Wheel Drive'
    assert sv.doors == 3
    assert sv.year is None
    assert sv.cc is None
    assert sv.mileage is None
    assert sv.owners is None


def test_str():
    """ Tests model.SaleVehicle.__str()__ """
    print(str(sv))
    assert str(sv) == ' Ford Fiesta Zetec S, Manual gearbox, Petrol, Hatchback, Front Wheel Drive, 3 doors'
