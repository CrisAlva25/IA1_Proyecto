from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfasdfasdfasdfas'

class NameForm(Form):
   name = StringField('What is your name?')
   submit = SubmitField('Submit')

   @app.route('/', methods=['GET', 'POST'])
   def index():
      name = None
      form = NameForm()
      if form.validate_on_submit():
         name = form.name.data
         form.name.data = ''
      return render_template('index.html', form=form, name=name)

if __name__ == "__main__":
    app.run()