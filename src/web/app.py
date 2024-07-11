from flask import Flask
import datetime

app = Flask(__name__)

from web.config import Config
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/autos.sqlite"
app.config["TEMPLATES_AUTO_RELOAD"] = True

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

INITIAL_STATE = False


if db:
    from data.search_criteria import search_criteria as db_search_criteria
    from data.sale_vehicle import sale_vehicle as db_sale_vehicle

    # db.session.query(db_sale_vehicle).delete()
    # db.session.query(db_search_criteria).delete()
    # db.session.commit()
    #
    # from model.search_criteria import SearchCriteria
    #
    # # criteria yields vehicles for home page visuals and vehicle valuation
    # init_criteria = SearchCriteria(None, None, None, None, None, None, None, None, None, None, None)
    # db_init_criteria = db_search_criteria(init_criteria)
    # db.session.add(db_init_criteria)
    #
    # # below criteria are to demo the price tracking feature
    # demo_criteria_1 = SearchCriteria('Ford', 'Fiesta', 'Zetec S', 2011, 2011, 'Manual', 'Petrol', None, 3, None, None)
    # db_demo_criteria_1 = db_search_criteria(demo_criteria_1)
    # db.session.add(db_demo_criteria_1)
    #
    # demo_criteria_2 = SearchCriteria('Tesla', 'Model 3', None, None, None, None, None, None, None, None, None)
    # db_demo_criteria_2 = db_search_criteria(demo_criteria_2)
    # db.session.add(db_demo_criteria_2)
    #
    # demo_criteria_3 = SearchCriteria('Audi', 'S3', None, 1999, 2003, None, None, None, None, None, None)
    # db_demo_criteria_3 = db_search_criteria(demo_criteria_3)
    # db.session.add(db_demo_criteria_3)
    #
    # demo_criteria_4 = SearchCriteria('BMW', 'M4', None, 2021, None, None, None, None, None, None, None)
    # db_demo_criteria_4 = db_search_criteria(demo_criteria_4)
    # db.session.add(db_demo_criteria_4)
    #
    # db.session.commit()

# from data.scheduler import Scheduler
# startAt = datetime.datetime.now().replace(hour=0, minute=1, second=0)  # do it at 1am every day
# s = Scheduler(startAt)
# s.start()  # scheduler runs queries immediately
#
# print('\nCollecting current autotrader.com vehicles for app visualisations. This will take a few minutes.')
# print('The app will not launch successfully until this process is finished. Attempts to do so will result in an error.')
# print('The end of this process will be signified by a "Scheduler finished." message.\n')

from web.routes import api
app.register_blueprint(api)
