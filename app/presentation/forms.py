from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    query = StringField('Rechercher', validators=[DataRequired()], render_kw={"class": "fr-input", "placeholder": "Rechercher", "type": "search"})
