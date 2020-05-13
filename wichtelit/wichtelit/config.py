import environ


def string_none_converter(value):
    if value is None:
        return None
    return str(value)


@environ.config
class User:
    name = environ.var(
        converter=str,
        help="The Username to use."
    )
    password = environ.var(
        default=None,
        converter=string_none_converter,
        help="The Password for the user to use.",
    )


@environ.config
class Contact:
    dsb_email = environ.var(
        default="dsb@example.com",
        converter=str,
        help="The Email Address for the DSB."
    )
    email = environ.var(
        default="admin@example.com",
        converter=str,
        help="The Email Address for contact."
    )
    zip_code = environ.var(
        default="12345",
        converter=str,
        help="The ZIP Code for the address."
    )
    city = environ.var(
        default="Musterstadt",
        converter=str,
        help="The City of the address."
    )
    street = environ.var(
        default="Musterstraße 1",
        converter=str,
        help="The Street of the address."
    )
    name = environ.var(
        default="Wichtelit Admin",
        converter=str,
        help="The Name of the Responsible Site Owner."
    )


@environ.config
class Email:
    host = environ.var(
        default='mxf9a9.netcup.net',
        converter=str,
        help="The SMTP Hostname to use to send emails through."
    )
    port = environ.var(
        default=587,
        converter=int,
        help="The SMTP Port to use to send emails through."
    )
    tls = environ.bool_var(
        default=True,
        help="SMTP use TLS or not.")
    timeout = environ.var(
        default=60,
        converter=int,
        help="The Default Timeout for SMTP Connection establishment."
    )
    backend = environ.var(
        default='django.core.mail.backends.smtp.EmailBackend',
        converter=str,
        help="The EMAIL Backend to use for django."
    )
    user = environ.group(User)


@environ.config
class Database:
    engine = environ.var(
        default='django.db.backends.postgresql',
        converter=str,
        help="The Database Engine to use."
    )
    host = environ.var(
        default='127.0.0.1',
        converter=str,
        help="The RDBMS Hostname to use to connect to."
    )
    port = environ.var(
        default='5432',
        converter=int,
        help="The RDBMS Port to use to connect to."
    )
    name = environ.var(
        default='wichtelit',
        converter=str,
        help="The Name of the RDBMS Database to use to connect to."
    )
    user = environ.group(User)


@environ.config
class Captcha:
    score = environ.var(
        default=0.85,
        converter=float,
        help="Captcha required score to reach for human users." +
        " (higher more complicated captcha)"
    )
    private_key = environ.var(
        default='6LfUFukUAAAAANboVLwQASuXQrw6ayFsfwFFQtRq',
        converter=str,
        help="A private captcha key (https://www.google.com/recaptcha/intro/v3.html)"
    )
    public_key = environ.var(
        default='6LfUFukUAAAAAASAapQwhYeERyh532DDYQHHHER7',
        converter=str,
        help="A public captcha key (https://www.google.com/recaptcha/intro/v3.html)"
    )


@environ.config(prefix="WICHTELIT")
class WichtelitConfig:
    secret_key = environ.var(
        default='---cjz#uz(&br66^fis#p+(x1!wpqt&%nr#ny_!@-09#*jwk+m',
        converter=str,
        help="The Secret Key of the Django Application. (Default is development Key," +
        " https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/"
    )
    captcha = environ.group(Captcha)
    database = environ.group(Database)
    email = environ.group(Email)
    contact = environ.group(Contact)
