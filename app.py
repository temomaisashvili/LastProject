from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, SmallInteger, BigInteger, DateTime, Date
from flask_migrate import Migrate
from flask import Flask, render_template, \
    request, redirect, url_for, flash, session
from faker import Faker
import datetime
from forms import LoginForm, RegistrationForm
from forms import TourForm
from functools import wraps
from bcrypt import checkpw, hashpw, gensalt

app = Flask(__name__)
faker = Faker('ka_GE')


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate(render_as_batch=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# initialize the app with the extension
db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect('login')
        return func(*args, **kwargs)

    return wrapper


def is_not_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return redirect('home')
        return func(*args, **kwargs)

    return wrapper


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]

    age: Mapped[int] = mapped_column(SmallInteger)
    address: Mapped[str]
    tours = db.relationship('Tour', backref='user', lazy='dynamic', cascade='all, delete')

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email, password=password).first()
        return user


class Tour(db.Model):
    __tablename__ = 'tours'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str]
    image: Mapped[str]
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))
#
#
# with app.app_context():
#     print('creating database...')
#     db.create_all()
#     print('database created!')


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
@is_not_authenticated
def login():
    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.authenticate(email, password)
            if not user and not checkpw(password.encode('utf-8'), user.password):
                flash('Incorrect, Try Again!')
                return redirect('login')
            session['user_id'] = user.id
            return redirect(url_for('home'))
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=["POST", "GET"])
@is_not_authenticated
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            age = form.age.data
            address = form.address.data

            user = User.query.filter_by(first_name=first_name).first()

            if user is not None:
                flash('User With This First Name Already Exists!')
                return render_template('register.html', form=form, user=user)
            hashed_password = hashpw(password.encode('utf-8'), gensalt())
            user = User(first_name=first_name, last_name=last_name,
                        email=email, password=hashed_password,
                        age=age, address=address)
            db.session.add(user)
            db.session.commit()
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Successfully Logged Out')
    return redirect('login')


@is_authenticated
@app.route('/tours', methods=['POST', 'GET'])
def tours():
    tour_data = Tour.query.all()
    user_data = User.query.all()
    return render_template('tours.html', tour_data=tour_data, user_data=user_data)


@app.route('/user_tours/<int:user_id>')
def user_tours(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('tours'))
    tours = user.tours
    return render_template('tours.html', tours=tours, user_id=user_id)


@is_authenticated
@app.route('/create_tours/<int:user_id>', methods=['POST', 'GET'])
def create_tours(user_id):
    form = TourForm
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('tours'))

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            tour = Tour(title=title, content=content, user_id=user.id)
            user.tours.append(tour)
            db.session.add(tour)
            db.session.commit()
            flash('Tour Successfuly Added')
            return redirect(url_for('user_tours', user_id=user_id))
        return render_template('create_tours.html', form=form)

    return render_template('create_tours.html', form=form, user_id=user_id)


app.secret_key = 'kandswhqoiehoqn2442ewjhrNDLJKD'
if __name__ == '__main__':
    app.run(debug=True)