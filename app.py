from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import os
import random
import string
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize the counter
counter_file = 'counter.txt'
if not os.path.exists(counter_file):
    with open(counter_file, 'w') as f:
        f.write('0')

def increment_counter():
    with open(counter_file, 'r+') as f:
        count = int(f.read()) + 1
        f.seek(0)
        f.write(str(count))
        f.truncate()
    return count

# Define image links
IMAGE_LINKS = [
    '/static/images/pet_adoption.jpg',
    '/static/images/pet_care.jpg',
    '/static/images/pet_health.jpg'
]

# Define pet information
PET_INFO = [
    {
        'name': 'Buddy',
        'image': '/static/images/pet1.jpg',
        'health': 'Healthy',
        'age': '3 years',
        'gender': 'Male',
        'price': '$500'
    },
    {
        'name': 'Molly',
        'image': '/static/images/pet2.jpg',
        'health': 'Healthy',
        'age': '2 years',
        'gender': 'Female',
        'price': '$450'
    },
    {
        'name': 'Charlie',
        'image': '/static/images/pet3.jpg',
        'health': 'Healthy',
        'age': '1 year',
        'gender': 'Male',
        'price': '$600'
    }
]

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    captcha = StringField('Captcha', validators=[DataRequired()])
    submit = SubmitField('Send Message')

def generate_captcha():
    # Generate a random string of letters and digits
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session['captcha'] = captcha_text

    # Create an image with the captcha text
    img = Image.new('RGB', (200, 50), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), captcha_text, fill=(0, 0, 0), font=font)

    # Save the image to a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route('/')
def index():
    count = increment_counter()
    return render_template('index.html', images=IMAGE_LINKS, count=count, pets=PET_INFO)

@app.route('/about')
def about():
    return render_template('about.html', images=IMAGE_LINKS)

@app.route('/services')
def services():
    return render_template('services.html', images=IMAGE_LINKS)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.captcha.data.lower() == session.get('captcha', '').lower():
                flash('Thank you for your message!', 'success')
                return redirect(url_for('contact_success'))
            else:
                flash('Invalid captcha. Please try again.', 'error')
    generate_captcha()
    return render_template('contact.html', images=IMAGE_LINKS, form=form)

@app.route('/contact/success')
def contact_success():
    return render_template('contact_success.html')

@app.route('/robots.txt')
def robots_txt():
    return app.send_static_file('robots.txt')

@app.route('/captcha')
def captcha():
    img_io = generate_captcha()
    return img_io.getvalue(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(debug=True)