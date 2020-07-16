from bson.objectid import ObjectId
from flask import Flask, render_template, request
import pymongo
import json
import re
import os

app = Flask(__name__, static_folder=os.path.abspath('static'))

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/emailTemplates')
client = pymongo.MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
template_db = db.templates
petition_db = db.petitions


@app.before_first_request
def json_to_db():
    template_db.drop()
    with open('email_templates.json') as json_data:
        templates = json.load(json_data)
    for templ in templates:
        templ["template"] = re.split(r'[{}]', templ["template"])
        templ["inputs"] = get_inputs(templ["template"])
        template_db.insert_one(templ)
    petition_db.drop()
    with open('petitions.json') as json_data:
        petitions = json.load(json_data)
    for petition in petitions:
        petition_db.insert_one(petition)


@app.route('/')
def index():
    templates = template_db.find({})
    return render_template('index.html', templates=templates)


@app.route('/petitions')
def petitions():
    petitions = petition_db.find({})
    return render_template('petitions.html', petitions=petitions)


@app.route('/<templ_id>')
def show_email(templ_id):
    template = template_db.find_one({'_id': ObjectId(templ_id)})
    return render_template('email_template.html', template=template)


@app.route('/<templ_id>', methods=['POST'])
def send(templ_id):
    template = template_db.find_one({'_id': ObjectId(templ_id)})

    full = fill_template(template["template"], request.form)
    mailto = []
    if template["emails"]:
        for email in template["emails"]:
            mailto.append(f'mailto:{email}?bcc=&subject={template["title"]}&body={full}')
    else:
        mailto.append(f'mailto:PLEASE_FIND_YOUR_MAYORS_EMAIL?bcc=&subject=test&body={full}')
    return render_template('send.html', full=full, mailto=mailto)


def fill_template(template, inputs):
    filled = ""
    for section in template:
        if section in inputs.keys():
            filled += inputs[section]
        else:
            filled += section
    return filled


def get_inputs(template):
    inputs = {}
    for i in range(1, len(template), 2):
        inputs[template[i]] = ""
    return inputs


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
