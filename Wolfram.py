import wolframalpha
from flask import Flask, render_template
from flask_ask import *
from variables import *

client = wolframalpha.Client(WOLFRAMALPHA_API_KEY)

app = Flask(__name__)
ask = Ask(app, '/wolfram')

@ask.launch
def launch():
    speech_text = "What would you like me to lookup?"
    reprompt_text = "I can search for almost anything on Wolfram Alpha, what would you like me to look for?"
    return question(speech_text).reprompt(reprompt_text).simple_card('WolframAlpha', speech_text)

@ask.intent('Search', mapping={'query': 'Query'})
def search(query):
    reprompt_text = "Im sorry, I didnt get that, what would you like me to search for?"
    response = client.query(query)
    try:
        response = response['pod'][1]['subpod']['plaintext']
    except:
        response = "Unable to find answer!"
    return statement(response).simple_card('WolframAlpha', response)

app.run()
