from wtforms.validators import DataRequired
from wtforms.validators import EqualTo
from wtforms.validators import Email
from wtforms import SubmitField
from wtforms import StringField
from wtforms import validators
from wtforms.fields.html5 import EmailField

from flask_wtf import RecaptchaField
from flask_wtf import Recaptcha
from flask_wtf import Form


class MailingList(Form):

    message = "Email must match."

    first    = StringField("first-name", validators = [DataRequired()])

    last     = StringField("last-name",  validators = [DataRequired()])

    email    = EmailField("email", validators = [DataRequired(), Email()])

    confirm  = EmailField("confirm", validators = [DataRequired(), Email(),
                    EqualTo("email", message = message)])

    recaptcha = RecaptchaField(validators=[Recaptcha(
            message="Please make sure you are not a robot!")])

    submit   = SubmitField("Sign Up!", 
                    validators = [DataRequired()])
