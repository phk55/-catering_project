# encoding:utf-8
import config
from flask import Blueprint, render_template, request, g, json
from exit import redis_db, db
from utils import restful, qiniuupload
from .models import MenuModels, CMSUser
import datetime
import threading

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
