from app import db
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)
		
class RegisterForm(FlaskForm):
	username = StringField('Nombre de usuario', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Contraseña', validators=[DataRequired()])
	rePassword = PasswordField('Confirmar contraseña', validators=[DataRequired()])
	submit = SubmitField('Agregar')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Contraseña', validators=[DataRequired()])
	submit = SubmitField('Agregar')



class Story(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64), index=True, unique=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Story {}'.format(self.title)

class StoryForm(FlaskForm):
	id = IntegerField('ID de la historia', validators=[DataRequired()], default=1)
	title = TextAreaField('Titulo de la historia', validators=[DataRequired()], default="Escribir el titulo...")
	user_id = IntegerField('ID del usuario', validators=[DataRequired()], default=1)
	submit = SubmitField('Agregar')
		

class PassageForm(FlaskForm):
	id = IntegerField('ID del párrafo', validators=[DataRequired()], default=1)
	paragraph = TextAreaField('Texto del párrafo', validators=[DataRequired()], default="Escribir el párrafo...")
	story_id = IntegerField('ID de la historia', validators=[DataRequired()], default=1)
	#decision_1 = IntegerField('Decisión_1', validators=[DataRequired()], default=1)
	#decision_1_text = TextAreaField('Texto del link', validators=[DataRequired()], default="Escribir el párrafo...")
	#decision_2 = IntegerField('Decisión_2', validators=[DataRequired()], default=1)
	#decision_2_text = TextAreaField('Texto del link', validators=[DataRequired()], default="Escribir el párrafo...")
	submit = SubmitField('Agregar')


class Passage(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
	paragraph = db.Column(db.String(64))
	#link_1 = db.Column(db.Integer)
	#link_1_text = db.Column(db.String(64))
	#link_2 = db.Column(db.Integer)
	#link_2_text = db.Column(db.String(64))

	def getData(self):
		return {
			"id": self.id,
			"story_id": self.story_id,
			"paragraph": self.paragraph,
			#"link_1": self.link_1,
			#"link_2": self.link_2,
		}

class PassageLink(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	origin_paragraph_id = db.Column(db.Integer, db.ForeignKey('passage.id'))
	link_description = db.Column(db.String(64))
	destination_paragraph_id =  db.Column(db.Integer, db.ForeignKey('passage.id'))


class PassageLinkForm(FlaskForm):
	id = IntegerField('ID del link', validators=[DataRequired()], default=1)
	origin_paragraph_id = IntegerField('ID del párrafo de origen', validators=[DataRequired()], default=1)
	link_description = StringField('Texto del link', validators=[DataRequired()])
	destination_paragraph_id = IntegerField('ID del parrafo destino', validators=[DataRequired()], default=1)
	submit = SubmitField('Agregar')