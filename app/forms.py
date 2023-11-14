from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


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
