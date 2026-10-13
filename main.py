import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime
import smtplib
from email.message import EmailMessage
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tshepo'

app.config['COMPANY_EMAIL'] = os.environ.get("COMPANY_EMAIL")
app.config['MY_EMAIL'] = os.environ.get("MY_EMAIL")
app.config['EMAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")

# Initialize Flask-Limiter to restrict repeated requests by IP address
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)


@app.route('/')
def home_page():
    current_year = datetime.now().year
    return render_template('index.html', year=current_year)


@app.route('/download', methods=['GET', 'POST'])
@limiter.limit("5 per minute", methods=["POST"])  # Limits form POST spam per IP
def download_page():
    if request.method == 'POST':
        # --- HONEYPOT CHECK ---
        # If a bot fills out this hidden field, silently fake a success response 
        # and do NOT send an email or log anything.
        if request.form.get('hp_website'):
            flash('Thank you! We will let you know very soon', 'success')
            return redirect(url_for('download_page', submitted=True))

        name = request.form.get('download_name')
        email = request.form.get('download_email')

        # Send email only when they fill out and submit the waitlist form
        send_email(
            name=name,
            email=email,
            subject='Fake Door - User Interested',
            message='A user is interested in downloading the tool')

        flash('Thank you! We will let you know very soon', 'success')
        return redirect(url_for('download_page', submitted=True))

    # Check if they just submitted the form (via the ?submitted=true query parameter)
    if request.args.get('submitted') != 'True':
        send_email(
            name='No name',
            email='No user email',
            subject='Fake Door - Download Button Clicked',
            message='A user just clicked the download button from the home page', )

    return render_template('download.html')


@app.route('/contact-us', methods=['GET', 'POST'])
@limiter.limit("5 per minute", methods=["POST"])  # Limits contact form spam per IP
def contact_page():
    if request.method == 'POST':
        # --- HONEYPOT CHECK ---
        if request.form.get('hp_website'):
            flash('Thank you! Your message has been sent successfully.', 'success')
            return redirect(url_for('contact_page'))

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        send_email(
            name=name,
            email=email,
            subject="New Form Submission (Fake Door)",
            message=message)

        flash('Thank you! Your message has been sent successfully.', 'success')
        return redirect(url_for('contact_page'))

    return render_template('contact.html')


def send_email(subject, name, email, message):
    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = app.config['MY_EMAIL']
    msg["To"] = app.config['COMPANY_EMAIL']

    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")

    with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as connection:
        connection.login(app.config['MY_EMAIL'], app.config['EMAIL_PASSWORD'])
        connection.send_message(msg)


# Optional: Custom error handler if someone hits the rate limit
@app.errorhandler(429)
def ratelimit_handler(e):
    flash('Too many requests. Please try again later.', 'danger')
    return redirect(url_for('home_page'))


if __name__ == "__main__":
    app.run(debug=True)
