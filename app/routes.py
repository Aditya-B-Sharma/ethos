from app import app
from flask import render_template, request
from datetime import datetime
from .data import geocode_fwd, get_district_pp, get_meshID_ACT, get_district_ACT, get_population_projections_ACT


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
    loc = geocode_fwd(str(locationType))
    locationType = loc
    print(loc)
    mesh = get_meshID_ACT(loc)
    dist = get_district_ACT(mesh)

    graph = get_population_projections_ACT(dist)

    # otherwise address/district
    return render_template(
        'info.html',
        title = "E-thos Info",
        businessVar = str(businessType),
        locationVar = str(locationType),
        graph = graph,
        year = datetime.now().year,
    )


