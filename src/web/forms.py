from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional
from data.makes import MAKES


GEARBOXES = ['', 'Automatic', 'Manual']
FUELS = ['', 'Petrol', 'Diesel', 'Bi Fuel', 'Electric', 'Hybrid - Diesel/Electric', 'Hybrid – Diesel/Electric Plug-in',
         'Hybrid – Petrol/Electric', 'Hybrid – Petrol/Electric Plug-in']
DOORS = ['', 0, 2, 3, 4, 5, 6]
DRIVETRAINS = ['', 'Four Wheel Drive', 'Front Wheel Drive', 'Rear Wheel Drive']
BODIES = ['', 'Camper', 'Convertible', 'Coupe', 'Estate', 'Hatchback', 'MPV', 'Other', 'Panel Van', 'Pickup', 'SUV',
          'Saloon']
MAKES.insert(0,'')


class CreateSearchCriteria(FlaskForm):
    """ Class to represent the form on the /createSearch page.

    :param FlaskForm: base class for Flask forms
    """

    make = SelectField('Make *', choices=[(make, make) for make in MAKES], validators=[DataRequired()])
    model = StringField('Model *', validators=[DataRequired()])
    variant = StringField('Variant', filters=[lambda x: x or None],
                          render_kw={"placeholder": "Requires exact autotrader.com input"})
    minYear = IntegerField('Year From', validators=[Optional()])
    maxYear = IntegerField('Year To', validators=[Optional()])
    gearbox = SelectField('Gearbox', choices=[(gearbox, gearbox) for gearbox in GEARBOXES], validators=[Optional()])
    fuel = SelectField('Fuel', choices=[(fuel, fuel) for fuel in FUELS], validators=[Optional()])
    doors = SelectField('Doors', choices=[(doors, doors) for doors in DOORS], validators=[Optional()])
    drivetrain = SelectField('Drivetrain', choices=[(drivetrain, drivetrain) for drivetrain in DRIVETRAINS],
                             validators=[Optional()])
    body = SelectField('Body Type', choices=[(body, body) for body in BODIES], validators=[Optional()])
    keywords = StringField('Keywords', filters=[lambda x: x or None],
                           render_kw={"placeholder": "E.g. specific trim level"})
    search = SubmitField('Search')


class CreatePrediction(FlaskForm):
    """ Class to represent the form on the /valuation page.

    :param FlaskForm: base class for Flask forms
    """

    make = SelectField('Make *', choices=[(make, make) for make in MAKES], validators=[DataRequired()])
    year = IntegerField('Year *', validators=[DataRequired()])
    mileage = IntegerField('Mileage *', validators=[DataRequired()])
    body = SelectField('Body Type', choices=[(body, body) for body in BODIES], validators=[Optional()])
    owners = IntegerField('Owners', validators=[Optional()])
    engine_size = IntegerField('Engine Size (cc)', validators=[Optional()],
                               render_kw={"placeholder":"e.g. 1.6L = 1600cc"})
    power = IntegerField('Power (BHP)', validators=[Optional()])
    gearbox = SelectField('Gearbox', choices=[(gearbox, gearbox) for gearbox in GEARBOXES], validators=[Optional()])
    fuel = SelectField('Fuel', choices=[(fuel, fuel) for fuel in FUELS], validators=[Optional()])

    search = SubmitField('Search')
