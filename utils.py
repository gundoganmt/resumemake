import os
from functools import wraps
from flask_mail import Message
from threading import Thread
from flask import request, current_app, abort
from flask_mail import Mail
mail = Mail()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(name, email, subject, message):
    app = current_app._get_current_object()
    msg = Message(subject='Webpaget Contact',
        sender="admin@webpaget.com",
        recipients=["mahmut_gundogan@hotmail.com"])
    msg.body = "name: {}, email: {}, subject: {}, message: {}".format(name, email, subject, message)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def send_confirmation_email(user):
    app = current_app._get_current_object()
    token = user.get_confirmation_token()
    msg = Message(subject='Confirmation email',
        sender="support@jobby.net",
        recipients=[user.email])
    msg.html = render_template('account/email_confirmation.html', token=token, name=user.name)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

ALLOWED_IMG_EXTENSIONS = {'jpeg', 'jpg', 'png'}
UPLOAD_PROFILE_FOLDER = os.path.join(os.getcwd(), 'resumemake/static/images/profiles')
UPLOAD_SERVICE_FOLDER = os.path.join(os.getcwd(), 'resumemake/static/images/services')
UPLOAD_TESTI_FOLDER = os.path.join(os.getcwd(), 'resumemake/static/images/testimonials')
UPLOAD_PORT_FOLDER = os.path.join(os.getcwd(), 'resumemake/static/images/portfolios')

RESUME_SITES_NAMES = ['sunshine', 'ronaldo', 'elegence']

def allowed_img_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

def get_extension(filename):
    return '.'+ filename.rsplit('.', 1)[1].lower()

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def only_main():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if request.host == 'webpaget.com' or request.host == 'www.webpaget.com':
                return fn(*args, **kwargs)
            else:
                abort(404), 404
        return decorator
    return wrapper
