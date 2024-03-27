
# Import the necessary modules.
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app.
app = Flask(__name__)

# Configure the database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define the Pension model.
class Pension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Float, nullable=False)
    years_of_service = db.Column(db.Integer, nullable=False)

# Create the database tables.
db.create_all()

# Define the home page route.
@app.route('/')
def home():
    return render_template('home.html')

# Define the dashboard route.
@app.route('/dashboard')
def dashboard():
    # Get the current user.
    user = User.query.get(1)

    # Get the user's pensions.
    pensions = Pension.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', user=user, pensions=pensions)

# Define the login route.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form.
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are correct.
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Log the user in.
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))
        else:
            # Display an error message.
            flash('Invalid username or password.')

    return render_template('login.html')

# Define the registration route.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the username and password from the form.
        username = request.form['username']
        password = request.form['password']

        # Create a new user.
        user = User(username=username, password=password)

        # Add the user to the database.
        db.session.add(user)
        db.session.commit()

        # Log the user in.
        flash('Registered successfully.')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

# Define the contact route.
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get the name and email address from the form.
        name = request.form['name']
        email = request.form['email']

        # Send an email to the agency.
        mailgun = Mailgun('my-api-key', 'my-domain')
        mailgun.send_email(
            'no-reply@my-domain',
            'info@my-domain',
            'New message from ' + name,
            email
        )

        # Display a success message.
        flash('Message sent.')

    return render_template('contact.html')

# Run the app.
if __name__ == '__main__':
    app.run()
