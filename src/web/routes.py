import time

from flask import render_template, redirect, url_for, Blueprint, flash, request, abort
import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
from json import dumps
from prophet import Prophet
from prophet.plot import plot_plotly
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

from autotrader.autotrader import Autotrader
from model.search_criteria import SearchCriteria
from web.forms import CreateSearchCriteria, CreatePrediction
from web.app import db
from data.search_criteria import search_criteria as DBSearchCriteria
from data.sale_vehicle import sale_vehicle as DBSaleVehicle

api = Blueprint('api', __name__)
pio.templates.default = "seaborn"  # Default plotly graph theme


@api.context_processor
def inject_tracking_vehicles():
    """ Injects all ongoing searches and their names (apart from search_criteria_id = 1, reserved for home page
    visualisations) into base template context

    :return: dictionary of search ids and search names
    """

    result = db.session.query(DBSearchCriteria.id).all()
    ongoing_searches = [id for id, in result]
    ongoing_searches.pop(0)

    search_names = []
    result = db.session.query(DBSearchCriteria).all()
    for res in range(1, len(result)):
        search_names.append(str(result[res]))

    return dict(searches=zip(ongoing_searches, search_names))


@api.route('/')
def index():
    """ Creates specific visualisations from the db, json encodes them and passes as context to home.html.

    :return: str, home.html template
    """

    df1 = pd.read_sql("SELECT * FROM sale_vehicle WHERE search_criteria_id = 1 AND body IS NOT NULL;", db.engine)
    fig1 = px.pie(df1, names='body', title='Vehicles On Sale By Body Type')
    json_fig1 = dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    df2 = pd.read_sql("SELECT year, power, engine_size FROM sale_vehicle WHERE search_criteria_id = 1 AND power IS "
                      "NOT NULL AND year IS NOT NULL and engine_size IS NOT NULL AND year >= 2005 AND year <= 2020;",
                      db.engine).groupby('year').mean().reset_index()
    fig2 = px.scatter(df2, x='year', y='power', size='engine_size', size_max=80,
                      title='Average Engine Capacity vs Average Engine Power vs Year Registered',
                      labels={"year": "Year of Registration", "power": "Average Engine Power (hp)",
                              "engine_size": "Average Engine Capacity (cc)"}).update_layout(plot_bgcolor="#f8f9fa")
    json_fig2 = dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    df3 = pd.read_sql("SELECT * FROM sale_vehicle WHERE search_criteria_id = 1 AND fuel IS NOT NULL;", db.engine)
    fig3 = px.pie(df3, names='fuel', title='Vehicles On Sale By Fuel')
    json_fig3 = dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    df4 = pd.read_sql("SELECT * FROM sale_vehicle WHERE search_criteria_id = 1 AND fuel IS NOT NULL AND power IS "
                      "NOT NULL AND engine_size IS NOT NULL;", db.engine)
    fig4 = px.scatter(df4, x='power', y='engine_size', size='price', color='fuel', size_max=30,
                      title='Price vs Engine Size vs Engine Power By Fuel Type',
                      labels={"power": "Engine Power (hp)", "engine_size": "Engine Capacity (cc)", "price": "Price",
                              "fuel": "Fuel Type"}).update_layout(plot_bgcolor="#f8f9fa")
    json_fig4 = dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', title='Home', fig1=json_fig1, fig2=json_fig2, fig3=json_fig3, fig4=json_fig4,
                           active='home')


@api.route('/createSearch', methods=['GET', 'POST'])
def create_search():
    """ Passes forms.CreateSearchCriteria as context to createSearch. On form validation, web-scrapes for vehicles
    matching user criteria and stores returned SaleVehicles in data if any are found.

    :return: str - createSearch.html template, or Response object - redirect to api.searchInfo
    """

    form = CreateSearchCriteria()
    if form.validate_on_submit():
        make = form.make.data.strip()
        model = form.model.data.strip()
        variant = form.variant.data
        min_year = form.minYear.data
        max_year = form.maxYear.data
        gearbox = form.gearbox.data
        fuel = form.fuel.data
        body = form.body.data
        doors = form.body.data
        drivetrain = form.drivetrain.data
        keywords = form.keywords.data

        # strip surrounding whitespace if variant specified
        if variant is not None:
            variant = variant.strip()
        # if form data is empty string then assign none
        if gearbox == "":
            gearbox = None
        if fuel == "":
            fuel = None
        if doors == "":
            doors = None
        if drivetrain == "":
            drivetrain = None
        if body == "":
            body = None

        if db.session.query(DBSearchCriteria).filter_by(make=make, model=model, variant=variant, min_year=min_year,
                                                        max_year=max_year, gearbox=gearbox, fuel=fuel, body=body,
                                                        doors=doors, drivetrain=drivetrain, keywords=keywords).first() \
                is not None:
            flash('Price tracking for this vehicle is already ongoing', 'danger')
            return render_template('createSearch.html', title='Create Search', form=form)

        search_criteria = SearchCriteria(make, model, variant, min_year, max_year, gearbox, fuel, body, doors,
                                         drivetrain, keywords)
        data_src = Autotrader(True)
        sale_vehicles = data_src.get_vehicles(search_criteria)
        del data_src  # to cleanup web driver

        if not sale_vehicles:
            flash('No vehicles found!', 'danger')
            return render_template('createSearch.html', title='Create Search', form=form, active='track')

        db_search_criteria = DBSearchCriteria(search_criteria)  # convert criteria to associated db model
        db.session.add(db_search_criteria)
        for s_v in sale_vehicles:
            db_sale_vehicle = DBSaleVehicle(s_v)  # covert sale vehicles to associated db models
            db_search_criteria.sale_vehicles.append(db_sale_vehicle)
            db.session.add(db_sale_vehicle)
        db.session.commit()

        return redirect(url_for('api.search_info', search_id=db_search_criteria.id))

    return render_template('createSearch.html', title='Create Search', form=form, active='track')


@api.route('/searchInfo/<search_id>')
def search_info(search_id):
    """ Creates two visualisations, one a simple time series with multiple dimensions, and the other a time series
    forecast, both for entries in sale_vehicle table where search_criteria_id = id. These plots are enncoded and passed
    to searchInfo.html as context.

    :param search_id: int, the search_criteria_id in the sale_vehicle table that visualisations are made from
    :return: Response object
    """

    if search_id == '1':
        abort(404)

    if db.session.query(DBSearchCriteria).filter_by(id=search_id).first() is None:
        abort(404)

    criteria_name = str(db.session.query(DBSearchCriteria).filter_by(id=search_id).first())

    all_data = pd.read_sql("SELECT price, mileage, year, date FROM sale_vehicle WHERE search_criteria_id = (?);",
                           db.engine, params=[search_id]).dropna()

    fig1 = px.scatter(all_data, x='date', y='price', color='mileage',  hover_data=["year"], labels={
        "date": "Date", "price": "Price (£)", "mileage": "Mileage", "year": "Model Year"}).update_layout(
        plot_bgcolor="#f8f9fa")
    json_fig1 = dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    dataframe = all_data[['date', 'price']].groupby('date').mean().reset_index()  # Average price on per date
    nunique_dates = dataframe['date'].nunique()

    # cannot predict with less than 2 data points
    if nunique_dates >= 2:

        dataframe.rename(columns={'date': 'ds', 'price': 'y'}, inplace=True)  # rename as per Prophet instructions
        model = Prophet(growth='logistic', daily_seasonality=False)
        dataframe['cap'] = 10000000  # highest autotrader price
        dataframe['floor'] = 75  # lowest
        model.fit(dataframe)
        future = model.make_future_dataframe(periods=nunique_dates, freq='D')  # predict as long as been tracking for
        future['cap'] = 10000000
        future['floor'] = 75
        df_forecast = model.predict(future).drop(columns=['cap', 'floor'])  # stops cap and floor markers from plotting

        fig = plot_plotly(model, df_forecast, xlabel='Date', ylabel='Average Price (£)', figsize=(1152, 450))\
            .update_layout(plot_bgcolor="#f8f9fa")
        json_forecast = dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('searchInfo.html', title='Search Info', search_name=criteria_name,
                               fig1=json_fig1, fig2=json_forecast, active=search_id)
    else:
        message = 'There is not enough data yet to forecast. Check back in 24 hours when more has been collected'
        return render_template('searchInfo.html', title='Search Info',
                               fig1=json_fig1, fig2=None, message=message, active=search_id)


# predict valuation of vehicle using blank search criteria data (search_criteria_id=1)
# Compare KNN and decision tree regression (on recommendation of supervisor)
@api.route('/valuation', methods=['GET', 'POST'])
def valuation():
    """ Renders forms.CreatePrediction form. On validate, redirects to api.valuation_info, passing form data as context.

    :return: str - valuation.html, or Response - redirect to api.valuation_info
    """
    form = CreatePrediction()
    if form.validate_on_submit():
        make = form.make.data
        year = form.year.data
        mileage = form.mileage.data
        body = form.body.data
        owners = form.owners.data
        engine_size = form.engine_size.data
        power = form.power.data
        gearbox = form.gearbox.data
        fuel = form.fuel.data

        if form.gearbox.data == "":
            gearbox = None
        if form.fuel.data == "":
            fuel = None
        if form.body.data == "":
            body = None

        return redirect(url_for('api.valuation_info', make=make, year=year, mileage=mileage, body=body, owners=owners,
                                engine_size=engine_size, power=power, gearbox=gearbox, fuel=fuel))
    return render_template('valuation.html', title='Valuation', form=form, active='valuation')


# display the predictions and their error and accuracy information
@api.route('/valuationInfo')
def valuation_info():
    """Using request.args arguments received, predicts vehicle valuations using 2 different regressors. Generates
    enhanced error analysis plots for these predictions, and encodes them and passes them as context to
    valuationInfo.html

    :return: str, valuationInfo.html template
    """
    make = request.args.get('make')
    year = request.args.get('year')
    mileage = request.args.get('mileage')
    body = request.args.get('body')
    owners = request.args.get('owners')
    engine_size = request.args.get('engine_size')
    power = request.args.get('power')
    gearbox = request.args.get('gearbox')
    fuel = request.args.get('fuel')

    # read in prediction data, establish categorical and non-categorical features as columns
    dataframe = pd.read_sql("SELECT * FROM sale_vehicle WHERE search_criteria_id = 1;", db.engine)
    all_columns = ['make', 'year', 'mileage', 'price']
    features = ['make', 'year', 'mileage']
    non_categorical_features = ['year', 'mileage']
    categorical_features = ['make']
    predict_args = [make, year, mileage]

    # assign column names etc. from arguments
    if body:
        categorical_features.append('body')
        all_columns.append('body')
        features.append('body')
        predict_args.append(body)
    if owners:
        non_categorical_features.append('owners')
        features.append('owners')
        all_columns.append('owners')
        predict_args.append(owners)
    if engine_size:
        non_categorical_features.append('engine_size')
        features.append('engine_size')
        all_columns.append('engine_size')
        predict_args.append(engine_size)
    if power:
        non_categorical_features.append('power')
        features.append('power')
        all_columns.append('power')
        predict_args.append(power)
    if gearbox:
        categorical_features.append('gearbox')
        all_columns.append('gearbox')
        features.append('gearbox')
        predict_args.append(gearbox)
    if fuel:
        categorical_features.append('fuel')
        all_columns.append('fuel')
        features.append('fuel')
        predict_args.append(fuel)

    dataframe = dataframe[all_columns].dropna()
    x = dataframe[features]
    y = dataframe['price']

    predict_args_df = pd.DataFrame([predict_args], columns=features)  # Need to make predict args into dataframe too

    # encode categorical features, scale non-categorical features for knn. Make individual prediction
    column_trans_knn = make_column_transformer((OneHotEncoder(handle_unknown='ignore'), categorical_features),
                                               (StandardScaler(), non_categorical_features), remainder='passthrough')
    knn_model = KNeighborsRegressor(n_neighbors=3)
    knn_pipe = make_pipeline(column_trans_knn, knn_model)
    knn_pipe.fit(x, y)
    unformatted_prediction_knn = knn_pipe.predict(predict_args_df)
    knn_prediction = int(unformatted_prediction_knn[0].round())

    # test/train split for accuracy and error analyses. Procedure adapted from https://plotly.com/python/ml-regression/
    train_idx, test_idx = train_test_split(dataframe.index, test_size=.20, random_state=1)
    dataframe['split'] = 'train'
    dataframe.loc[test_idx, 'split'] = 'test'
    x_train = dataframe.loc[train_idx, features]
    y_train = dataframe.loc[train_idx, 'price']

    # KNN accuracy and error analysis
    knn_pipe.fit(x_train, y_train)
    dataframe['prediction'] = knn_pipe.predict(x)
    print(dataframe.head)
    knn_r2 = round(r2_score(y, dataframe['prediction'], sample_weight=None, multioutput='uniform_average'), 3)
    knn_fig = px.scatter(dataframe, x='price', y='prediction', marginal_x='histogram', color_discrete_map=
        {'test': '#dd8452', 'train': '#4c72b1'}, template='plotly', marginal_y='histogram', color='split',
        trendline='ols', labels={"price": "Actual Vehicle Price (£)", "prediction": "Predicted Vehicle Price (£)"})
    knn_fig.update_layout(plot_bgcolor="#f8f9fa", font_color='#242425')
    knn_fig.update_traces(histnorm='probability', selector={'type': 'histogram'})
    knn_fig.add_shape(
        type="line", line=dict(dash='dash'),
        x0=y.min(), y0=y.min(),
        x1=y.max(), y1=y.max()
    )
    json_fig_knn = dumps(knn_fig, cls=plotly.utils.PlotlyJSONEncoder)

    # residual plot
    dataframe['residual'] = dataframe['prediction'] - dataframe['price']

    knn_fig_2 = px.scatter(
        dataframe, x='prediction', y='residual',
        marginal_y='violin', trendline='ols', color_discrete_map={'test': '#d68386', 'train': '#88c296'},
        template='plotly',
        labels={"residual": "Residual Vehicle Price (£)", "prediction": "Predicted Vehicle Price (£)"},
        color='split'
    )
    knn_fig_2.update_layout(plot_bgcolor="#f8f9fa", font_color='#242425')
    json_fig_knn_2 = dumps(knn_fig_2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('valuationInfo.html', title='Your Valuation', pred1=knn_prediction,
                           fig1=json_fig_knn, fig2=json_fig_knn_2, r2_1=knn_r2)


@api.errorhandler(404)
def not_found_error(e):
    """ 404 Not Found Error handler

    :return: str, 404.html template
    """

    return render_template('404.html'), 404


@api.errorhandler(500)
def internal_error(e):
    """ 500 Internal Server Error handler

    :return: str, 500.html template
    """

    return render_template('500.html'), 500
