from flask import Blueprint, render_template, request
from ..cms.models import MenuModels, ScoreModel
from .form import AddScoreForm
from utils import restful
from exit import db
import config

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
    menus = MenuModels.query.order_by(MenuModels.weighted_value.desc()).all()
    context = {
        'menus': menus
    }
    return render_template('front/menus.html', **context)


@bp.route('/addscore/', methods=['POST'])
def addscore():
    form = AddScoreForm(request.form)
    if form.validate():
        score1 = form.score1.data
        score2 = form.score2.data
        score3 = form.score3.data
        suggest = form.suggest.data
        cur_url = form.cur_url.data
        menu_id = int(cur_url.split('/')[-1])

        score1 = config.SCORE_DICT.get(score1)
        score2 = config.SCORE_DICT.get(score2)
        score3 = config.SCORE_DICT.get(score3)
        print(score1, score2, score3, suggest)
        menu = MenuModels.query.get(menu_id)
        if not menu:
            return restful.params_error('信息有误')
        new_score = ScoreModel(score1=score1, score2=score2, score3=score3, suggest=suggest)
        new_score.score_menu = menu
        db.session.add(new_score)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())
