from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterForm(Form):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=1, max=60)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=1, max=60)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    description = StringField(
        "Description", validators=[DataRequired(), Length(min=0, max=256)]
    )


class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
 
 
class EditUser(Form):
    description = StringField(
        "Description", validators=[Length(min=0, max=256)]
    )
    
    
class WebsitesAdd(Form):
    name = StringField("Name", validators=[DataRequired()])
    url = StringField("Url", validators=[DataRequired()])
