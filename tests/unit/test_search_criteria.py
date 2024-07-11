from model.search_criteria import SearchCriteria

sc = SearchCriteria('Ford', 'Fiesta', 'Zetec S', 2011, 2011, 'Manual', 'Petrol', 'Hatchback', 3,
                        'Front Wheel Drive', None)


def test_constructor():
    """ Tests model.SearchCriteria constructor """

    assert sc.make == 'Ford'
    assert sc.model == 'Fiesta'
    assert sc.variant == 'Zetec S'
    assert sc.min_year == 2011
    assert sc.max_year == 2011
    assert sc.gearbox == 'Manual'
    assert sc.fuel == 'Petrol'
    assert sc.body == 'Hatchback'
    assert sc.drivetrain == 'FWD'
    assert sc.doors == 3
    assert sc.keywords is None


def test_str():
    """ Tests model.SearchCriteria.__str()__"""

    assert str(sc) == 'Ford Fiesta Zetec S, from 2011, up to 2011, Manual, Petrol, Hatchback, FWD, 3 doors'


