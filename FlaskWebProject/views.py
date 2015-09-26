"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWebProject import app
import contextio

from keys import CONTEXTIO_KEY, CONTEXTIO_SECRET

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/accounts')
def accounts():
    context_io = contextio.ContextIO(consumer_key=CONTEXTIO_KEY,
            consumer_secret=CONTEXTIO_SECRET)
    accounts = context_io.get_accounts()
    content = ''
    for acc in accounts:
        content += '<h2>' + acc.id + '</h2>'
        for msg in acc.get_messages():
            body = msg.get_body(type='text/plain')
            for b in body:
                content += str(b) 
                content += '<br>'
        content += '<br><br>'
    return content
