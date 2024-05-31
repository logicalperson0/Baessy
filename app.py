from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('signIn'))
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if password != confirmPassword:
            flash('Password do not match!', 'error')
            return render_template('signup')
        
        response = requests.post('http://localhost:3000/signup', json={
            'firstName' : firstName,
            'lastName' : lastName,
            'email' : email,
            'password' : password
        })

        if response.status_code == 201:
            flash('Signup Successful!', 'success')
            return redirect(url_for('signIn'))
        else:
            flash(response.json().get('message', 'Signup failed!'), 'error')

    return render_template('signup.html')

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = request.post('http://localhost:3000/signIn', json={
            'username' : username,
            'password' : password
        })

        if response.status_code == 200:
            session['logged_in'] = True
            session['token'] = response.json()['token']
            flash('SignIn Successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(response.json().get('message', 'SignIn failed!'), 'error')

    return render_template('signIn.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

