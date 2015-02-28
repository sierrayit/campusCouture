#Campus Couture


from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, url_for, redirect, \
	render_template, abort, g, flash, _app_ctx_stack


#configuration
DATABASE = '/tmp/campuscouture.db'


#create app
app = Flask(__name__)
app.config.from_object(__name__)

#establishes database connection
def get_db():
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
		top.sqlite_db.row_factory = sqlite3.row
	return top.sqlite_db

#initializes db
def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f: db.cursor().executescript(f.read())
	db.commit()

#returns list of dicts from db
def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	return (rv[0] if rv else None) if one else rv

#pull specific things from db
def get_user_id(username):
	rv = query_db('select user_id from user where username = ?', [username], one=True)

def go_home():
	if not g.user:
		return redirect(url_for('home'))
	return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user(): 
	if g.user:
		return redirect(url_for('home'))
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'Please enter your username.'
		elif not request.form['email'] or \
		'@' not in request.form['email']:
			error = 'Please enter a valid email address.'
	elif not request.form['password']:
		error = 'Please enter a valid password.'
	elif request.form['password'] != request.form['password2']:
		error = 'The two passwords you have entered do not match.'
	elif get_user_id(request.form['username']) is not None: 
		error = 'That username is already taken.'
	else:
		db = get_db()
		db.execute('''insert into user (username, email, pw_hash) values (?, ?, ?)''', [request.form['username'], request.form['email'], request.form['password']])
		db.commit()
		flash('You were successfully registered. Please log in.')
		return redirect(url_for('login'))
	return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        else:
            flash('You have successfully logged in.')
            session['user_id'] = user['user_id']
            return redirect(url_for('timeline'))
    return render_template('login.html', error=error)

@app.route('/')
def displayHome():
	return render_template('index.html')

@app.route('/share/')
def displayShare():
	return render_template('share.html')

@app.route('/login/')
def displayLogin():
	return render_template('login.html')

@app.route('/about/')
def displayAbout():
	return render_template('about.html')

@app.route('/register/')
def displayRegister():
	return render_template('register.html')

@app.route('/about/')
def displayAbout():
	return render_template('about.html')

#@app.route('/dress_template/')
#def displayRegister():
#	return render_template('dress_template.html')

@app.teardown_appcontext
def close_db(exception):
	top = _app_ctx_stack.top
	if hasattr(top, 'sqlite_db'):
		top.sqlite_db.close()

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
