# encoding:utf-8
import config
from flask import Blueprint, render_template, request, g, json
from exit import redis_db, db
from utils import restful, qiniuupload, ewm
from .models import MenuModels, CMSUser, ScoreModel
import datetime
import threading
from ..common_func.month_rane import get_month_range

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
def index():
    redis_p = redis_db.pipeline()
    redis_p.set('ss3', 'fsdfd2')

    redis_p.execute()
    return render_template('cms/cms_index.html')


@bp.route('/menulist/')
def menulist():
    menus = MenuModels.query.order_by(MenuModels.weighted_value.desc()).all()
    context = {
        'menus': menus
    }
    return render_template('cms/menulist.html', **context)


@bp.route('/addmenulist/', methods=['POST'])
def addmenulist():
    menu_name = request.form['menu_name']
    weighted_value = request.form['weighted_value']
    describe_info = request.form['describe_info']
    pic_file = request.files['pic_file']
    if not menu_name or not weighted_value or not pic_file.filename:
        return restful.params_error(message='请确认是否填写菜品名称;权重;以及已上传图片！')
    try:
        weighted_value = int(weighted_value)
        if 0 < weighted_value <= 100:
            pass
        else:
            raise Exception
    except:
        return restful.params_error(message='请确保输入的权重为0-100的数字！')

    pic_name = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '_' + pic_file.filename
    t1 = threading.Thread(target=qiniuupload.upload_qiniu, args=(pic_file, pic_name))
    t1.start()

    new_menu = MenuModels(menu_name=menu_name, weighted_value=int(weighted_value), describe_info=describe_info,
                          pic_name=pic_name)

    db.session.add(new_menu)
    db.session.commit()
    t2 = threading.Thread(target=ewm.qr_with_central_img,
                          args=(config.SCORE_URL + str(new_menu.id), config.UEDITOR_QINIU_DOMAIN + pic_name,
                                'ewm_' + str(new_menu.id) + '.png'))
    t2.start()
    t2.join()
    #
    # ewm_filename = ewm.qr_with_central_img(link=config.SCORE_URL + str(new_menu.id),
    #                                        central_picture=config.UEDITOR_QINIU_DOMAIN + pic_name,
    #                                        output_file='ewm_' + str(new_menu.id) + '.png')
    new_menu.ewm_name = 'ewm_' + str(new_menu.id) + '.png'

    db.session.add(new_menu)
    db.session.commit()

    return restful.success()


@bp.route('/chef/', methods=['GET', 'POST'])
def chef():
    if request.method == 'GET':
        menus = MenuModels.query.order_by(MenuModels.weighted_value.desc()).all()
        chefs = CMSUser.query.filter_by(TAG=1).all()
        context = {
            'menus': menus,
            'chefs': chefs
        }
        return render_template('cms/chef.html', **context)
    else:
        chef_name = request.form['chef_name']
        menu_id_data = request.form['menu_id_data']
        menu_id_list = json.loads(menu_id_data)

        user = CMSUser.query.filter_by(username=chef_name).first()

        if user and int(user.TAG) != 0:
            for old_menu in user.menus:
                user.menus.remove(old_menu)
            db.session.commit()
            for menu_id in menu_id_list:
                menu = MenuModels.query.get(int(menu_id))
                user.menus.append(menu)
            db.session.add(user)
            db.session.commit()
        else:
            user = CMSUser(username=chef_name, password=88888888, phone_number=1111, TAG=1)
            for menu_id in menu_id_list:
                menu = MenuModels.query.get(int(menu_id))
                user.menus.append(menu)
            db.session.add(user)
            db.session.commit()

        return restful.success()


@bp.route('/delchef/', methods=['POST'])
def delchef():
    chef_name = request.form['chef_name']
    user = CMSUser.query.filter_by(username=chef_name).first()
    if not user:
        return restful.params_error(message='信息有误！')
    user.TAG = 0
    db.session.commit()
    return restful.success()


@bp.route('/scoreall/')
def scoreall():
    menus = MenuModels.query.order_by(MenuModels.weighted_value.desc()).all()

    month_list = get_month_range(config.START_TIME, datetime.datetime.now())

    month_list.reverse()
    context = {
        'menus': menus,
        'month_list': month_list
    }
    return render_template('cms/score_all.html', **context)


@bp.route('/scoredata/', methods=['POST'])
def scoredata():
    cur_month = request.form['cur_month']
    cur_menu_id = request.form['cur_menu_id']
    cur_month = cur_month.split('. ')[1]
    print(cur_month)
    print(cur_menu_id)
    return restful.success()
