from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, brown
from nltk import pos_tag
from nltk.stem import PorterStemmer
import nltk

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

graph = Graph(url + '/db/data/', username=username, password=password)

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class AddNewsForm(FlaskForm):
    title = StringField('Title',  validators=[DataRequired()])
    detail= StringField('Detail', validators=[DataRequired()])
    submit = SubmitField('Add News')

class user:
    def __init__(self, email):
        self.email = email

    def find(self):
        user = graph.find_one('Reporter', 'email', self.email)
        return user

    def register(self, password,username):
        if not self.find():
            user = Node('Reporter', username=username, password=bcrypt.encrypt(password),email=self.email)
            graph.create(user)
            return True
        else:
            return False

    def find_name(self,nam,names1):
        Names1=[]
        Names1=names1
        flag=0
        for n in Names1:
            if(n==nam):
                flag=1
        return flag

    def create_node(self,EXAMPLE_TEXT):
        ps = PorterStemmer()
        #"Nimra kill food."
        #"I love cheese"
        #"five people killed twenty five people in Lahore"
        stop_words = set(stopwords.words('english'))
        #print(sent_tokenize(EXAMPLE_TEXT))
        #print(word_tokenize(EXAMPLE_TEXT))
        word_tokens = word_tokenize(EXAMPLE_TEXT)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        #print(word_tokens)
        print(filtered_sentence)
        #for w in filtered_sentence:
        #    print(ps.stem(w))
        noyuns=pos_tag(filtered_sentence)
        print(noyuns)
        noun1=[]
        verb1=[]
        Names = []
        for line in open('out.txt','r').readlines():
            Names.append(line.strip())
        #print(Names)
        for entity, tag in noyuns:
            if(tag=='NN' or tag=='NNS'or tag=='NNP'or tag=='NNPS' or self.find_name(entity,Names)==1):
                noun1.append(entity)
            elif(tag=='VB'or tag=='VBD'or tag=='VBG'or tag=='VBN' or tag=='VBP'or tag=='VBZ'):
                verb1.append(entity)
        relat=verb1[0]
        noun2=Node(noun1[0],id=1,name=noun1[0])
        noun3=Node(noun1[1],id=2,name=noun1[1])
        rel=Relationship(noun2,relat,noun3)
        graph.create(rel)


    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])
        else:
            return False

    def add_post(self,title1,detail1):
        user = self.find()
        news = Node(
            'News',
            id=str(uuid.uuid4()),
            title=title1,
            detail=detail1
           
        )
        self.create_node(title1)
        rel = Relationship(user, 'Reported', news)
        graph.create(rel)

def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()

def date():
    return datetime.now().strftime('%Y-%m-%d')



  



   