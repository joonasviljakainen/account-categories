from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CategoryForm(FlaskForm):

    name = StringField("name", validators=[validators.Length(min=1, max=50)])
