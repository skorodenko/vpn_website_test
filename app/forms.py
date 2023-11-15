from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL


class RegisterForm(Form):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=60)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )


class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    
    
class WebsitesAdd(Form):
    url = StringField("Url", validators=[DataRequired(), URL()])
