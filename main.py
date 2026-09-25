import os
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
import smtplib

app = Flask(__name__)
# Make sure your app has a secret key configured for flashing messages:
app.config['SECRET_KEY'] = 'tshepo'

app.config['COMPANY_EMAIL'] = os.environ.get("COMPANY_EMAIL")
app.config['MY_EMAIL'] = os.environ.get("MY_EMAIL")
app.config['EMAIL_PASSWORD'] = os.environ.get("EMAIL_PASSWORD")


@app.route('/')
def home_page():
    current_year = datetime.now().year
    return render_template('index.html', year=current_year)


@app.route('/download', methods=["GET", "POST"])
def download_page():
    send_email(name='No name', email='No user email', message=" A user just clicked download button")
    if request.method == 'POST':
        name = request.form.get("download_name")
        email = request.form.get("download_email")

        send_email(name, email, message=" A user is interested in downloading the tool")
        flash('Thank you! We will let you know very soon', 'success')
        return redirect(url_for('download_page'))
    return render_template('download.html')


@app.route('/contact-us', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        send_email(name, email, message)
        flash('Thank you! Your message has been sent successfully.', 'success')
        return redirect(url_for('contact_page'))
    return render_template('contact.html')


def send_email(name, email, message):
    email_message = f"Subject:New Message (Fake door)\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(app.config['MY_EMAIL'], app.config['EMAIL_PASSWORD'])
        connection.sendmail(app.config['MY_EMAIL'], app.config['MY_EMAIL'], email_message)


if __name__ == "__main__":
    app.run(debug=False)
