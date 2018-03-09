import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import praw
import random

reddit = praw.Reddit('ShowerShuffle')
subreddit = reddit.subreddit('ShowerThoughts')

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
testlog = logging.getLogger("steven")

# return list of shower thoughts
def read_list_of_shower_thoughts(titles, cardTitle):
    speechString = '<speak>' + cardTitle + '<break time="1s"/>' + '<break time="1s"/>'.join(titles) + '</speak>'
    cardString = '\n'.join(titles)
    speechString.encode('ascii', 'ignore')
    cardString.encode('ascii', 'ignore')
    return statement(speechString).simple_card(title=cardTitle, content=cardString)


@ask.launch
def launch():
    return get_random_shower_thought_intent()

@ask.intent("GetRandomShowerThoughtIntent")
def get_random_shower_thought_intent():
    myLimit = 500
    many_submissions = subreddit.top(limit=myLimit)
    many_titles = [st.title for st in many_submissions]
    return read_list_of_shower_thoughts(random.sample(many_titles, 10), 'Random Showerthoughts')

@ask.intent("GetNewShowerThoughtsIntent")
def get_new_shower_thoughts():
    submissions = subreddit.new(limit=10)
    titles = [st.title for st in submissions]
    return read_list_of_shower_thoughts(titles, 'New Showerthoughts')

@ask.intent("GetHotShowerThoughtsIntent")
def get_hot_shower_thoughts():
    submissions = subreddit.hot(limit=10)
    titles = [st.title for st in submissions]
    return read_list_of_shower_thoughts(titles, 'Hot Showerthoughts')

@ask.intent("GetTopShowerThoughtsIntent")
def get_hot_shower_thoughts():
    submissions = subreddit.top(limit=10)
    titles = [st.title for st in submissions]
    return read_list_of_shower_thoughts(titles, 'Top Showerthoughts')

@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")

@ask.session_ended
def session_ended():
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)

