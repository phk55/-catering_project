from flask import Blueprint, render_template, request
from ..cms.models import MenuModels, ScoreModel, CMSUser
from .form import AddScoreForm
from utils import restful, ewm
from exit import db
import config
import json
import uuid

bp = Blueprint('front', __name__)


@bp.route('/placeorder/', methods=['GET', 'POST'])
def placeorder():
    if request.method == 'GET':
        return render_template('front/place_order.html')
    else:
        num_data = request.form['num_data']
        num_data = json.loads(num_data)
        if not num_data:
            return restful.params_error('请输入菜品编号！')
        for i in num_data:
            if len(i) != 3:
                return restful.params_error('请确保输入的编号均为3位数！')
        num_str = '&'.join(num_data)
        score_url = config.SCORE_URL + num_str
        ewm.qr_single_code(score_url, 'qr_images\\' + str(uuid.uuid4()) + '.png')
        print(score_url)
        return restful.success()


@bp.route('/score/<ids>')
def score(ids):
    # print(id)
    if '&' in ids:
        ids = ids.split('&')
    ids = ['001', '005', '302', '002', '004']

    menus = []
    new_ids = []
    for i in ids:
        menu = MenuModels.query.filter_by(menu_num=i).first()
        if menu:
            menus.append(menu)
            new_ids.append(str(menu.id))
    # print(menus)
    new_ids = ','.join(new_ids)
    context = {
        'menus': menus,
        'ids': new_ids
    }
    return render_template('front/score.html', **context)


@bp.route('/')
def menuall():
    menus = MenuModels.query.filter_by(sold_out=0).order_by(MenuModels.menu_num).all()
    context = {
        'menus': menus
    }
    return render_template('front/menus.html', **context)


@bp.route('/addscore/', methods=['POST'])
def addscore():
    score_data = request.form['score_data']
    score_data = list(json.loads(score_data))
    print(score_data)
    score_dict = {}
    print(len(score_data[-1]))
    menu_id = score_data[-1].split(',')
    for i in range(len(menu_id)):
        # print(i)
        score_dict[menu_id[i]] = config.SCORE_DICT.get(score_data[i])
    score_dict['server'] = config.SCORE_DICT.get(score_data[-3])
    score_dict['suggest'] = score_data[-2]
    print(score_dict)
    for key, value in score_dict.items():
        if key == 'server' or key == 'suggest':
            pass
        else:
            menu = MenuModels.query.get(int(key))
            if not menu:
                pass
            else:
                chefs = menu.menu_to_users
                # print(chefs)
                chefs = [chef.username for chef in chefs if int(chef.TAG) == 1]

                all_chefs = ','.join(chefs)

                new_score = ScoreModel(score=value, server=score_dict.get('server'), suggest=score_dict.get('suggest'),
                                       chefs=all_chefs)
                new_score.score_menu = menu
                db.session.add(new_score)
    db.session.commit()
    # score1 = config.SCORE_DICT.get(score1)
    # score2 = config.SCORE_DICT.get(score2)
    # score3 = config.SCORE_DICT.get(score3)
    #
    # menu = MenuModels.query.get(menu_id)
    #
    # if not menu:
    #     return restful.params_error('信息有误')
    # chefs = menu.menu_to_users
    # # print(chefs)
    # chefs = [chef.username for chef in chefs if int(chef.TAG) == 1]
    #
    # all_chefs = ','.join(chefs)
    #
    # new_score = ScoreModel(score1=score1, score2=score2, score3=score3, suggest=suggest, chefs=all_chefs)
    # new_score.score_menu = menu
    # db.session.add(new_score)
    # db.session.commit()
    return restful.success()
