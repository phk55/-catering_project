from flask import Blueprint, render_template, request, jsonify
from ..cms.models import MenuModels, ScoreModel, CMSUser, DiningTableModel, ServerScoreModel
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
        tables = DiningTableModel.query.all()
        menus = MenuModels.query.filter_by(sold_out=0).order_by(MenuModels.menu_num).all()
        context = {
            'tables': tables,
            'menus': menus
        }
        return render_template('front/place_order.html', **context)
    else:
        num_data = request.form['num_data']
        num_data = json.loads(num_data)
        if not num_data:
            return restful.params_error('请输入菜品编号！')
        table = DiningTableModel.query.filter_by(table_num=num_data[0]).first()
        if not table:
            return restful.params_error('输入的餐桌号不存在')
        tem_list = [num_data[0]]
        for i in num_data[1:]:
            menu = MenuModels.query.filter_by(menu_num=i).first()
            if menu:
                tem_list.append(i)
        num_str = '&'.join(tem_list)
        score_url = config.SCORE_URL + num_str
        ewm.qr_single_code(score_url, 'qr_images\\' + str(uuid.uuid4()) + '.png')
        print(score_url)
        return restful.success()


@bp.route('/querymenun/', methods=['POST'])
def querymenu():
    tables = DiningTableModel.query.all()
    menus = MenuModels.query.filter_by(sold_out=0).order_by(MenuModels.menu_num).all()
    menu_dict = {}
    for menu in menus:
        menu_dict[menu.menu_num] = menu.menu_name

    table_dict = {}
    for table in tables:
        table_dict[table.table_num] = 'y'
    print(menu_dict)
    print(table_dict)
    data = {
        'code': 200,
        'data': {
            'menu_dict': menu_dict,
            'table_dict': table_dict
        },
        'message': ''
    }
    return jsonify(data)


@bp.route('/score/<ids>')
def score(ids):
    # print(id)
    if '&' in ids:
        ids = ids.split('&')
    # ids = ['1', '005', '302', '002', '004']

    menus = []
    new_ids = []
    for i in ids[1:]:  # 0位为餐桌号
        menu = MenuModels.query.filter_by(menu_num=i).first()
        if menu:
            menus.append(menu)
            new_ids.append(str(menu.id))
    # print(menus)
    new_ids.append(str(ids[0]))
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
    for i in range(len(menu_id) - 1):
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

                new_score = ScoreModel(score=value, chefs=all_chefs)
                new_score.score_menu = menu
                db.session.add(new_score)
    table = DiningTableModel.query.filter_by(table_num=menu_id[-1]).first()
    if table:
        server = ServerScoreModel(server=score_dict.get('server'), suggest=score_dict.get('suggest'))
        server.server_tables = table
        db.session.add(server)
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
