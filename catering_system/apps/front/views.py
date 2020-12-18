from flask import Blueprint, render_template
from ..cms.models import MenuModels

bp = Blueprint('front', __name__)


@bp.route('/score/<id>')
def score(id):
    menu = MenuModels.query.get(int(id))
    context = {
        'menu': menu
    }
    return render_template('front/score.html', **context)


@bp.route('/')
def menuall():
    menus = MenuModels.query.all()
    context = {
        'menus': menus
    }
    return render_template('front/menus.html', **context)
