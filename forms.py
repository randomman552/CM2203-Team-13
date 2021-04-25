from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class InputStockForm(FlaskForm):
    data1 = StringField('Data1', validators=[DataRequired(), Length(min=2, max = 50)])
    data2 = StringField('Data2', validators=[Length(min=2, max = 50)])

    submit= SubmitField('Load Data')
