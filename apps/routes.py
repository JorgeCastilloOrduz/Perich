from flask import Blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound

bp = Blueprint("routes", __name__)

@bp.route('/')
def route_default():
    return render_template('routes/index.html', segment='index')

@bp.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = request.path.split('/')[-1]

        # Serve the file (if exists) from app/templates/routes/*.html
        return render_template("routes/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('routes/page-404.html'), 404

    except:
        return render_template('routes/page-500.html'), 500