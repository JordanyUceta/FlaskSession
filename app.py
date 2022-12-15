from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__) 
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app) 


@app.route('/')
def home_page():
    """Select a survey"""

    return render_template('start.html', survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey(): 
    """Clear the session of responses"""

    session[RESPONSES_KEY] = [] 

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question(): 
    """Save response and redirect to next question"""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice) 
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)): 
        # they have answered all the questions!
        return redirect("/complete")

    else: 
        return redirect(f"/questions/{len(responses)}")



# @app.route("/questions/<int:qid>")
# def show_question(qid):
#     """Retrieve responses from session"""
#     responses = session.get(RESPONSES_KEY)
#     questions = survey.questions

#     if (responses is None): 
#         # trying to access question page too soon
#         return redirect('/')

#     if(len(responses) == len(survey.questions)):
#         # They've answered all the questions and we should thank them!
#         return redirect('/complete')

#     if(len(responses) != qid): 
#         # trying to access question out of order
#         flash(f'Invalid question id: {qid}')
#         return redirect(f'/questions/{len(responses)}')

#     question = survey.questions[qid] 
#     return render_template(
#         "question0.html", question_num=qid, question=question
#     )

@app.route("/questions/<int:qid>")
def show_question(qid):
    # Retrieve responses from session
    responses = session.get(RESPONSES_KEY)
    questions = survey.questions

    # If there are no responses, redirect to the home page
    if responses is None:
        return redirect('/')

    # If all questions have been answered, redirect to the 'complete' page
    if len(responses) == len(questions):
        return redirect('/complete')

    # If the question id is invalid, redirect to the current question
    if len(responses) != qid:
        flash(f'Invalid question id: {qid}')
        return redirect(f'/questions/{len(responses)}')

    # Retrieve the current question
    question = questions[qid] 

    # Render the question template
    return render_template(
        "question0.html", question_num=qid, question=question
    )


@app.route("/complete")
def complete(): 
    """Survey is completed, Show completion page"""

    return render_template("completed.html")

