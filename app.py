from flask import Flask, request, render_template, redirect, session, flash
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY']= "martial arts"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/') 
def home_page():
    session['response'] = []
    """ View Function that takes you to Home Page"""
    return render_template('home.html', title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)

@app.route('/question/<int:qn>')
def get_questions(qn):
    qn = len(session['response'])
    question = ""
    url = f'question.html'
    
    if qn == len(satisfaction_survey.questions):
        return render_template(('/complete.html'))
    
    elif qn != len(satisfaction_survey.questions):
         question = satisfaction_survey.questions[qn].question
         choices = satisfaction_survey.questions[qn].choices
         flash('Please answer questions in order')
         return render_template(f"{url}", question = question, choices = choices, title=satisfaction_survey.title, instructions=satisfaction_survey.instructions)
    
@app.route('/answer', methods = ['POST'])
def add_responses():
    qn = len(session['response'])
    choice = request.form['answer']
    response_f = session['response']
    response_f.append(choice)
    session['response'] = response_f

    if qn == len(satisfaction_survey.questions):
        return redirect('/complete.html')
    else:
    # import pdb
    # pdb.set_trace()
        return redirect(f'/question/{qn}')