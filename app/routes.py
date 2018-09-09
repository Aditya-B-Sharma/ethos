from app import app
from flask import render_template, request
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title = "E-thos Home",
        year = datetime.now().year,
    )
@app.route('/handle_data', methods=['POST'])
def handle_data():
    businessType = request.form['businessType']
    locationType = request.form['locationType']
    print(businessType)
    print(locationType)
    return render_template(
        'info.html',
        title = "E-thos Info",
        businessVar = str(businessType),
        locationVar = str(locationType),
        year = datetime.now().year,
    )


