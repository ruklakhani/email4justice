from flask import Flask, render_template, request
import os
STATIC_DIR = os.path.abspath('static')
print(STATIC_DIR)
app = Flask(__name__, static_folder=STATIC_DIR)

form1 = ["Hello, My name is ", "name", ".\n I am a resident of ", "city", ", ", "state", " and I am emailing today to demand accountability for the racist murder of Breonna Taylor. I demand that charges be pressed against all officers involved in this heinous killing, including Sgt. Jonathan Mattingly and officers Brett Hankison and Myles Cosgrove. They should all be fired, with their pensions revoked, and should be charged and prosecuted to the fullest extent of the law for murder. In addition, LMPD must eliminate No Knock Warrants. I demand that Mayor Greg Fischer and the Louisville City Council address the excessive use of force by LMPD and that we provide more support for community efforts and organizations that work to prevent police brutality and violence. Breonna Taylor was an ER technician, working tirelessly to help others during this global pandemic. She should be alive today. She would be alive today if it were not for the gross abuse of power and white supremacy exhibited by the Louisville Police Department. All officers involved must face consequences for this murder in order to provide her family with justice and to deter law enforcement from committing racist and brutal acts of violence against communities of color.\n Sincerely, ", "name"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/breonnataylor')
def form():
    return render_template('b_taylor.html')

@app.route('/send', methods=['POST'])
def send():
    # name = request.form['name']
    # city = request.form['city']
    # state = request.form['state']
    email = "cats@gmail.com"
    full = fill_template(form1, request.form)
    mailto = f'mailto:{email}?subject=test&body={full}'
    return render_template('send.html', full=full, mailto=mailto)

if __name__ == '__main__':
    app.run()

inputs = { 'name': 'name', 'city': 'city', 'state': 'state', 'rep': 'rep'}

def fill_template(form, inputs):
    full_template = ""
    for s in form:
        if s in inputs.keys():
            full_template += inputs[s]
        else: 
            full_template += s
    return full_template