import sched
import time
import datetime
from threading import Thread

from data.search_criteria import search_criteria as DBSearchCriteria
from data.sale_vehicle import sale_vehicle as DBSaleVehicle
from model.search_criteria import SearchCriteria
from autotrader.autotrader import Autotrader
from web.app import db


class Scheduler(Thread):
    """ Class to represent scheduler that updates autos data. """

    def __init__(self, tempus):
        """
        inits Scheduler with time to perform updates

        :param tempus: datetime object
        """

        Thread.__init__(self)
        self._sched = sched.scheduler(time.time, time.sleep)
        self.event_time = tempus
        self._sched.enterabs(tempus.timestamp(), 0, self.do_search)

    def run(self):
        """ Runs scheduler. """
        self._sched.run()

    def do_search(self):
        """ Performs data retrieval from autotrader.com. """

        print('\nScheduler working... ')

        # for criteria id =1 (data for home pages visualisation, and price prediction)
        # delete sale vehicles where criteria id = 1, then repopulate with new
        db.session.execute('DELETE FROM sale_vehicle WHERE search_criteria_id = 1')
        db_sc1 = db.session.query(DBSearchCriteria).filter_by(id=1).first()
        sc_1 = SearchCriteria.from_db(db_sc1)

        data_src = Autotrader(True)
        sale_vehicles = data_src.get_vehicles(sc_1, limit=1287)
        del data_src  # to cleanup web driver

        # add stuff to data
        for s_v in sale_vehicles:
            db_s_v = DBSaleVehicle(s_v)
            db_sc1.sale_vehicles.append(db_s_v)
            db.session.add(db_s_v)

        # for rest of the search criterias, dont delete just update with more
        db_criterias = db.session.query(DBSearchCriteria).filter(DBSearchCriteria.id != 1)
        for db_sc in db_criterias:
            criteria = SearchCriteria.from_db(db_sc)

            data_src = Autotrader(True)
            sale_vehicles = data_src.get_vehicles(criteria)
            del data_src  # to cleanup web driver

            # add stuff to data
            for s_v in sale_vehicles:
                db_s_v = DBSaleVehicle(s_v)
                db_sc.sale_vehicles.append(db_s_v)
                db.session.add(db_s_v)

        db.session.commit()

        print('\nScheduler finished.\n')

        # do it again tomorrow
        self.event_time = self.event_time + datetime.timedelta(days=1)
        self._sched.enterabs(self.event_time.timestamp(), 0, self.do_search)
