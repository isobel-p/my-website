from flask import Flask, render_template, abort, send_from_directory, redirect, make_response, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, MultipleFileField, BooleanField
from wtforms.validators import DataRequired
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.application import MIMEApplication
import datetime
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SECRET_KEY'] = "Hello123"

class Contact(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name')
    email = EmailField('Email')
    tel = TelField('Phone Number')
    social = StringField('Other - Platform: ')
    username = StringField('Other - Username/Tag/Alias: ')
    message = StringField('Message', validators=[DataRequired()])
    files = MultipleFileField('Attachments')
    news = BooleanField('I would like to receive newsletters and updates (if I ever send them)')

# Returns HTML 
@app.route('/')
def home():
    resp = make_response(render_template("index.html", message="Welcome back! It's great to see you again." if request.cookies.get("again") == "yes" else "Nice to meet you! Thanks for coming."))
    resp.set_cookie("again", "yes")
    return resp

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/playground')
def play():
    return render_template("playground.html")

@app.route('/418')
def tea():
    abort(418)
    # easter egg!

# Contact form and email handling
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Contact()
    if form.validate_on_submit():
        msg = MIMEMultipart() 
        msg['From'] = "isobel-p@hackclub.app"
        msg['To'] = "isobelpang@gmail.com"
        msg['Subject'] = f'{form.first.data} {form.last.data} - {datetime.datetime.now()}'
        body = f"""-----
NEW MESSAGE!
Sender: {form.first.data} {form.last.data}
{f'Email: {form.email.data}' if len(form.email.data) != 0 else "No email provided"}
{f'Tel: {form.tel.data}' if len(form.tel.data) != 0 else "No telephone num provided"}
{f'Other: {form.username.data} at {form.social.data}' if len(form.social.data) != 0 else "No other socials provided"}
Wants to receive mail: {form.news.data}
-----

{form.message.data}
"""
        msg.attach(MIMEText(body, 'plain')) 
        for file in form.files.data:
            if file and not type(str):
                file_content = file.read()
                attachment = MIMEApplication(file_content)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{file.filename}"'
                )
                msg.attach(attachment)
        try: 
            server = smtplib.SMTP("hackclub.app", 587) 
            server.ehlo() 
            server.starttls() 
            server.ehlo()
            server.login("isobel-p", ")WCAjW5W$rG7j6D-") 
            server.sendmail(msg["From"], msg["To"], msg.as_string()) 
            print("Email has been sent successfully!")
        except Exception as e: 
            print(f"Failed to send email: {e}")
        finally:
            server.quit()
        if len(form.email.data) > 0:
            receipt = MIMEMultipart()
            receipt['From'] = "isobel-p@hackclub.app"
            receipt['To'] = form.email.data
            receipt['Subject'] = f'Thanks for your message!'
            body = f"""Hi {form.first.data}!

Thanks for leaving a message! I'll write back ASAP.
            
Because you left your email in the contact form, you're receiving this email receipt.
            
This is an automated message from an unmonitored inbox - please don't reply to this email! I'll write to you soon.
            
Expect a reply in at most 1 business week.
            
Kind regards,
Isobel
<3
Sent at {datetime.datetime.now()} from sunny England"""
            receipt.attach(MIMEText(body, "plain"))
            try: 
                server = smtplib.SMTP("hackclub.app", 587) 
                server.ehlo() 
                server.starttls() 
                server.ehlo()
                server.login("isobel-p", ")WCAjW5W$rG7j6D-") 
                server.sendmail(receipt["From"], receipt["To"], receipt.as_string()) 
                print("Email has been sent successfully!")
            except Exception as e: 
                print(f"Failed to send email: {e}")
            finally:
                server.quit()
        return redirect('/success')
    return render_template("contact.html", form=form)

# File retrieval
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)
    # returns static files e.g. images, CSS or JS

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Error handling
@app.errorhandler(Exception)
def handle_error(e):
    code = 500                       # sets default error code of 500 (Internal Server Error)...
    if isinstance(e, HTTPException): # ...but checks if the exception is a valid HTTPException...
        code = e.code                # ...and changes the default error code if it is.
    ctitles = {404:"This is not the page you are looking for.", 418:"How did you get here? Spill the tea."} # custom titles
    title = ctitles[code] if code in ctitles else "Whoops, that's an error!"
    fault = "Looks like something broke here." if str(code)[0] == "5" else "Looks like something went wrong."
    fault = "Looks like Earl Grey, hot." if code == 418 else fault
    cat = f"https://http.cat/{code}.jpg"
    dog = f"https://http.dog/{code}.jpg"
    return render_template("error.html", cat=cat, dog=dog, title=title, fault=fault, error=e, code=code), code

# Runs the app in debug mode for testing!
if __name__ == '__main__':
    app.run(debug=True)