from top_five import app, db, mail, Message
from flask import render_template, request, redirect, url_for
from top_five.forms import PhoneNumberForm, RegisterForm, LoginForm
from top_five.models import AvengerInformation, User, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user

@app.route('/')
def home():
    avengers = AvengerInformation.query.all()
    return render_template("home.html", avengers=avengers)
    
@app.route('/topfive', methods=['GET', 'POST'])
def topfive():
    athlete_dict = {1:"Kirby Puckett", 2:"Torii Hunter", 3:"Lindsay Whalen", 4:"Mia Hamm", 5:"Kevin Garnett"}
    return render_template('topfive.html', athlete_dict=athlete_dict)
    
@app.route('/phonebookentry', methods=['GET', 'POST'])
@login_required
def phonebookentry():
    form = PhoneNumberForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = current_user.email
        phone_number = form.phone_number.data
        user_id = current_user.id
        print("\n", name, phone_number)
        avenger = AvengerInformation(name,email, phone_number,user_id)
        db.session.add(avenger)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('phonebookentry.html', form=form)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n", username, password, email)
        user = User(username,email,password)
        db.session.add(user)
        db.session.commit()

        msg = Message(f"Thanks for signing up for the Avengers phonebook,{email}!", recipients=[email])
        msg.body = ("Avengers, assemble your phone numbers!")
        msg.html = ("<h1>Welcome to the Avengers Phonebook!</h1>" "<p>Avengers Assemble!</p>")
        mail.send(msg)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/directory_update/<int:avenger_id>', methods=['GET','POST'])
@login_required
def directory_update(avenger_id):
    avenger = AvengerInformation.query.get_or_404(avenger_id)
    update_form = PhoneNumberForm()

    if request.method == 'POST' and update_form.validate():
        name = update_form.name.data
        phone_number = update_form.phone_number.data
        user_id = current_user.id
        print(name, phone_number, user_id)
        
        avenger.name = name
        avenger.phone_number = phone_number
        avenger.user_id = user_id
        db.session.commit()
        return redirect(url_for('home'))  
    return render_template('directory_update.html', update_form=update_form,avenger=avenger)

@app.route('/directory_update/delete/<int:avenger_id>', methods=['POST'])
@login_required
def avenger_delete(avenger_id):
    avenger = AvengerInformation.query.get_or_404(avenger_id)
    db.session.delete(avenger)
    db.session.commit()
    return redirect(url_for('home'))


    
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for ('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

