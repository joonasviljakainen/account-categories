from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, HiddenField, validators

class CategoryForm(FlaskForm):

    name = StringField("name", validators=[validators.DataRequired(), validators.InputRequired(True),validators.Length(min=1, max=50)])

class CategoryUpdateForm(FlaskForm):

    category = SelectField("Category")
    account = HiddenField("account", default="0")
    submit = SubmitField("Set new category")