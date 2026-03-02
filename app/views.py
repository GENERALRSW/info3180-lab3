from app import app, mail
from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message
from .forms import RegistrationForm, ContactForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the contact page and handle form submission."""
    form = ContactForm()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        msg = Message(
            subject=subject,
            sender=(name, email),
            recipients=[app.config['MAIL_USERNAME']]
        )
        msg.body = f'From: {name} <{email}>\n\n{message}'
        mail.send(msg)

        flash('Your message was successfully sent!', 'success')
        return redirect(url_for('home'))
    else:
        flash_errors(form)

    return render_template('contact.html', form=form)


###
# The functions below should be applicable to all Flask apps.
###

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404