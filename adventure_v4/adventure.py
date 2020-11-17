from flask import flash, render_template, request, url_for, redirect, session, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from app import app, db
from app.models import User, Story, PassageForm, Passage, PassageLink, StoryForm, RegisterForm, LoginForm, PassageLinkForm

Bootstrap(app)

db.create_all()

@app.context_processor
def get_current_user():
  return {"user": session.get('user')}

@app.route('/populate_db')
def populate():
	u = User(username="Test", email="test@test.com")
	db.session.add(u)
	db.session.commit()
	print('Added user')
	
	# Mostrar todos los usuarios
	users = User.query.all()
	
	return ''
	
@app.route('/')
def index():
	passages = Passage.query.all()
	stories = Story.query.all()
	users = User.query.all()
	#data = session.get('user') 
	#print(data["id"])

	#db.session.query(PassageLink).delete()
	#db.session.query(Passage).delete()
	#db.session.query(Story).delete()
	#db.session.query(User).delete()
	#db.session.commit()

	storiesWithAuthors = []

	for story in stories:
		for user in users:
			if(user.id == story.user_id):
				temp = {
					"story": story,
					"author": user.username
				}
				storiesWithAuthors.append(temp)



	return render_template("index.html", passages=passages, stories=storiesWithAuthors)

@app.route('/register', methods=['GET', 'POST'])
def register():
	userForm = RegisterForm()
	if userForm.validate_on_submit():

		isEmailRegister = User.query.filter(User.email == userForm.email.data).first()
		isUsernameRegister = User.query.filter(User.username == userForm.username.data).first()
		#or User.username == userForm.username.data
		

		if isEmailRegister == None and isUsernameRegister == None:
			new_user = User()
			new_user.username = userForm.username.data
			new_user.email = userForm.email.data

			new_user.set_password(userForm.password.data)

			db.session.add(new_user)
			db.session.commit()	

			return redirect(url_for('login'))

		flash("Email o Nombre de usuario ya resgitrado", 'info')

		
	
	return render_template('register.html', form=userForm)

@app.route('/login', methods=['GET', 'POST'])
def login(email=None, password=None):
	loginForm = LoginForm()
	if loginForm.validate_on_submit():
		
		email = loginForm.email.data
		password = loginForm.password.data
		
		user = User.query.filter(User.email == email).first()
		
		if user != None: 
			user_password = user.password_hash
			print(user_password)
			print(password)
			if user.check_password(password):
				
				#session['user'] = email
				session['user'] = {
					'email': email,
					'username': user.username,
					'id': user.id
				}
					
				return redirect(url_for('index'))
			else:
				flash("Email o Contraseña invalido", 'info')
				
		flash("Email o Contraseña invalido", 'info')
					
	
	return render_template('login.html', form=loginForm)
	

@app.route('/account', methods=['GET'])	
def account():
	data = session.get('user') 
	userEmail = data["email"]
	user = User.query.filter(User.email == userEmail).first()
	stories = Story.query.filter(Story.user_id == user.id)
	passages = Passage.query.all()
	
	return render_template('account.html', user=user, stories=stories, passages=passages)

@app.route('/createStory', methods=['GET', 'POST'])
def createStory():
	story = StoryForm()
	if story.validate_on_submit():
		new_story = Story()
		#new_story.id = story.id.data
		new_story.title = story.title.data
		
		#ACA
		data = session.get('user') 
		userEmail = data["email"]
		user = User.query.filter(User.email == userEmail).first()

		new_story.user_id = user.id
		
		db.session.add(new_story)
		db.session.commit()

		return redirect(url_for('account'))

	
	stories = Story.query.all()

	return render_template('storyForm.html', form=story, stories=stories)

@app.route('/story/<int:story_id>')
def show_story(story_id):	
	
	story = Story.query.get(story_id)
	passage = Passage.query.filter(Passage.story_id == story_id).first()
	#PassageLink.origin_paragraph_id == passage.id
	links = PassageLink.query.filter(PassageLink.origin_paragraph_id == passage.id)
	
	return render_template("story.html", story=story, passage=passage, links=links)





@app.route('/story/<int:story_id>/<int:passage_id>')
def change_passage(story_id, passage_id):	
	
	story = Story.query.get(story_id)
	passage = Passage.query.get(passage_id)
	links = PassageLink.query.filter(PassageLink.origin_paragraph_id == passage_id)
	
	return render_template("story.html", story=story, passage=passage, links=links)



@app.route('/passage/<int:passage_id>')
def show_passage(passage_id):
	passages = Passage.query.all()
	return render_template("passage.html", passages=passages, passage_id=passage_id)



@app.route('/story/addPassage', methods=['GET', 'POST'])
def edit():
	
	form = PassageForm()
	if form.validate_on_submit():
		new_passage = Passage()

		new_passage.story_id = request.form['story_id']
		new_passage.paragraph = form.paragraph.data

		#new_passage.link_1 = request.form['decision_1']
		#new_passage.link_1_text = form.decision_1_text.data
		#new_passage.link_2 = request.form['decision_2']
		#new_passage.link_2_text = form.decision_2_text.data

		db.session.add(new_passage)
		db.session.commit()

		
		flash("Pasaje agregado!", 'info')
	
	passages = Passage.query.all()#por front hacer un fetch
	data = session.get('user') 
	userID = data["id"]
	stories = Story.query.filter(Story.user_id == userID)
	
	return render_template('edit.html', form=form, passages=passages, stories=stories)

@app.route('/story/createPassageLink/<int:story_id>', methods=['GET', 'POST'])
def createPassageLink(story_id):
	linkForm = PassageLinkForm()
	if linkForm.validate_on_submit():
		new_link = PassageLink()

		new_link.origin_paragraph_id = request.form['origen']
		new_link.link_description = linkForm.link_description.data
		new_link.destination_paragraph_id = request.form['destino']

		db.session.add(new_link)
		db.session.commit()
		flash("Los pasajes se unieron con exito!", 'info')
	
	passages = Passage.query.all()
	return render_template('linkForm.html', linkForm=linkForm, story_id=story_id, passages=passages )



@app.route('/story/passages/<int:story_id>', methods=['GET', 'POST'])
def storyPassages(story_id):
	passages = Passage.query.filter(Passage.story_id == story_id)
	
	passagesResults = []
	for passage in passages:
		passagesResults.append(passage.getData())

	return jsonify(passagesResults)

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
	
