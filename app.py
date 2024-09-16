import os
import uuid

import boto3
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
import requests

region_name = os.getenv('AWS_DEFAULT_REGION', 'ap-northeast-1')
table_name = os.getenv('DYNAMODB_TABLE_NAME', 'messages')

db = boto3.resource('dynamodb', region_name=region_name)
table = db.Table(table_name)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'argqtahqtaatayaat'
app.config['JSON_AS_ASCII'] = False

class MessageForm(FlaskForm):
    message = StringField(validators=[DataRequired()])
    submit = SubmitField()


@app.route('/', methods=['GET'])

def home_page():
    db_response = table.scan()
    message_item = db_response['Items']
    r = jsonify(message_item)
    r.raise_for_status()
    items = r.json()

    form = MessageForm()

    return render_template('home.html', items=items, form=form)


@app.route('/', methods=['POST'])
def post_message():

    form = MessageForm()

    if form.validate_on_submit():
        json = {'message': form.message.data}
        json['uuid'] = str(uuid.uuid4())
        db_response = table.put_item(
            Item=json
        )
        return redirect(url_for('home_page'))

    return render_template('home.html', form=form)

@app.route('/healthz', methods=['GET'])
def health_check():
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
