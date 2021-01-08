# encoding:utf-8
import config
import calendar
import datetime
import threading
import uuid
import re
import random
import pandas as pd

from flask import Blueprint, render_template, request, json, jsonify, views, session, url_for, redirect
from sqlalchemy import and_
from exit import redis_db, db
from utils import restful, qiniuupload, ewm
from .models import MenuModels, CMSUser, ScoreModel, DiningTableModel, ServerScoreModel
from ..common_func.month_rane import get_month_range
from ..common_func.pd_read import pd_read_sql
from ..common_func.hyYz import SMS
from .form import LoginForm, SignupForm
from apps.common_func.decorators import login_required

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    redis_p = redis_db.pipeline()
    redis_p.set('ss3', 'fsdfd2')

    redis_p.execute()
    return render_template('cms/cms_index.html')


class LoginView(views.MethodView):
    def get(self, message=None):
        # 获取上个页面的url
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('cms.signup', _external=True):
            return render_template('cms/login.html', return_to=return_to)
        return render_template('cms/login.html')

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            print('aa')
            phone = form.phone.data
            password = form.pwd.data
            verify = form.verify.data
            if str(verify) == '1':
                user = CMSUser.query.filter_by(phone_number=phone).first()
                if user and user.check_password(password):
                    session[config.USER_ID] = user.id
                    session.permanent = True
                    return restful.success()
                else:
                    return restful.params_error('*手机号或密码错误!')
            else:
                yz_code = redis_db.get(phone)
                if not yz_code:
                    return restful.params_error('验证码有误！')
                yz_code = yz_code.decode()
                if yz_code != verify:
                    return restful.params_error('验证码有误！')
                user = CMSUser.query.filter_by(phone_number=phone).first()
                if user:
                    session[config.USER_ID] = user.id
                    session.permanent = True
                    return restful.success()
                else:
                    return restful.params_error('*手机号或密码错误!')

        else:
            return restful.params_error(form.get_error())


class SignupView(views.MethodView):
    def get(self):
        # 获取上个页面的url
        return_to = request.referrer
        if return_to and return_to != request.url:
            return render_template('cms/signup.html', return_to=return_to)
        return render_template('cms/signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            username = form.username.data
            phone = form.phone.data
            pwd = form.pwd.data
            verify = form.verify.data
            invite = form.invite.data
            yz_code = redis_db.get(phone)
            if not yz_code:
                return restful.params_error('验证码有误！')
            yz_code = yz_code.decode()
            if yz_code != verify:
                return restful.params_error('验证码有误！')
            if invite != config.INVITE:
                return restful.params_error('邀请码有误！')
            old_user = CMSUser.query.filter_by(phone_number=phone).first()
            if old_user:
                return restful.params_error(message='该员工号已被注册！')
            user = CMSUser(username=username, phone_number=phone, password=pwd, TAG=2)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))


@bp.route('/logout/')
@login_required
def logout():
    del session[config.USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/mesyzcode/', methods=['POST'])
def mesyzcode():
    phone_number = request.form['phone_number']
    phone_path = re.compile('1[3456789]\d{9}$')
    if re.match(phone_path, phone_number):
        print(phone_number)
        code = [str(random.randint(0, 9)) for i in range(0, 6)]
        code = ''.join(code)
        sms = SMS(config.ACCOUNT, config.PWD)
        sms.send_sms([phone_number], '您的验证码是：{}。请不要把验证码泄露给其他人。'.format(code))
        print(code)
        redis_p = redis_db.pipeline()
        redis_p.set(phone_number, code)
        redis_p.expire(phone_number, 300)
        redis_p.execute()

    return restful.success()


@bp.route('/menulist/')
@login_required
def menulist():
    menus = MenuModels.query.order_by(MenuModels.menu_num).all()
    context = {
        'menus': menus
    }
    return render_template('cms/menulist.html', **context)


@bp.route('/addmenulist/', methods=['POST'])
@login_required
def addmenulist():
    menu_name = request.form['menu_name']
    menu_num = request.form['weighted_value']
    describe_info = request.form['describe_info']
    pic_file = request.files['pic_file']
    if not menu_name or not menu_num or not pic_file.filename:
        return restful.params_error(message='请确认是否填写菜品名称;编号;以及已上传图片！')
    try:
        menu_num = str(menu_num)
        if len(menu_num) == 3:
            pass
        else:
            raise Exception
    except:
        return restful.params_error(message='请确保输入的编号为3位数！')
    new_menu = MenuModels.query.filter_by(menu_name=menu_name).first()
    new_menu2 = MenuModels.query.filter_by(menu_num=menu_num).first()
    if new_menu:
        return restful.params_error('您输入的菜品已存在系统中！')
    if new_menu2:
        return restful.params_error('您输入的编号已存在系统中！')

    pic_name = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '_' + pic_file.filename
    t1 = threading.Thread(target=qiniuupload.upload_qiniu, args=(pic_file, pic_name))
    t1.start()

    new_menu = MenuModels(menu_name=menu_name, menu_num=menu_num, describe_info=describe_info,
                          pic_name=pic_name)

    db.session.add(new_menu)
    db.session.commit()
    # t2 = threading.Thread(target=ewm.qr_with_central_img,
    #                       args=(config.SCORE_URL + str(new_menu.id), config.UEDITOR_QINIU_DOMAIN + pic_name,
    #                             'ewm_' + str(new_menu.id) + '.png'))
    # t2.start()
    # t2.join()
    # #
    # # ewm_filename = ewm.qr_with_central_img(link=config.SCORE_URL + str(new_menu.id),
    # #                                        central_picture=config.UEDITOR_QINIU_DOMAIN + pic_name,
    # #                                        output_file='ewm_' + str(new_menu.id) + '.png')
    # new_menu.ewm_name = 'ewm_' + str(new_menu.id) + '.png'
    #
    # db.session.add(new_menu)
    # db.session.commit()

    return restful.success()


@bp.route('/editmenu/', methods=['POST'])
@login_required
def editmenu():
    menu_name = request.form['menu_name']
    menu_num = request.form['weighted_value']
    describe_info = request.form['describe_info']
    pic_file = request.files['pic_file']
    sold_out = request.form.getlist('sold-out')
    old_menu = request.form['old-menu']
    # print(old_menu)

    if not old_menu:
        return restful.params_error('数据有误！')
    menu = MenuModels.query.filter_by(menu_name=old_menu).first()
    new_menu = MenuModels.query.filter_by(menu_name=menu_name).first()
    if new_menu and new_menu != menu:
        return restful.params_error('您输入的菜品已存在系统中！')
    if not menu_name or not menu_num:
        return restful.params_error(message='请确认是否填写菜品名称;权重;以及已上传图片！')
    try:
        menu_num = str(menu_num)
        if len(menu_num) == 3:
            pass
        else:
            raise Exception
    except:
        return restful.params_error(message='请确保输入的编号为3位数！')
    if pic_file:
        pic_name = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '_' + pic_file.filename
        t1 = threading.Thread(target=qiniuupload.upload_qiniu, args=(pic_file, pic_name))
        t1.start()
    menu.menu_name = menu_name
    menu.menu_num = menu_num
    menu.describe_info = describe_info
    if pic_file:
        pic_name = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '_' + pic_file.filename
        t1 = threading.Thread(target=qiniuupload.upload_qiniu, args=(pic_file, pic_name))
        t1.start()
        menu.pic_name = pic_name

    if sold_out:
        menu.sold_out = int(sold_out[0])

    db.session.add(menu)
    db.session.commit()
    # if pic_file:
    #     pic_new_name = 'ewm_' + str(uuid.uuid4()) + '.png'
    #     t2 = threading.Thread(target=ewm.qr_with_central_img,
    #                           args=(config.SCORE_URL + str(menu.id), config.UEDITOR_QINIU_DOMAIN + pic_name,
    #                                 pic_new_name))
    #     t2.start()
    #     t2.join()
    #     menu.ewm_name = pic_new_name
    #
    #     db.session.add(menu)
    #     db.session.commit()

    return restful.success()


@bp.route('/chef/', methods=['GET', 'POST'])
@login_required
def chef():
    if request.method == 'GET':
        menus = MenuModels.query.order_by(MenuModels.menu_num).all()
        chefs = CMSUser.query.filter_by(TAG=1).all()

        context = {
            'menus': menus,
            'chefs': chefs
        }
        return render_template('cms/chef.html', **context)
    else:
        chef_name = request.form['chef_name']
        menu_id_data = request.form['menu_id_data']
        tag = request.form['tag']
        menu_id_list = json.loads(menu_id_data)

        user = CMSUser.query.filter_by(username=chef_name).first()

        if tag:
            user = CMSUser.query.filter(and_(CMSUser.username == chef_name, CMSUser.TAG == 1)).first()

            if not user:
                return restful.params_error('请输入厨师姓名！')
            menus = [menu for menu in user.menus]
            for i in menus:
                user.menus.remove(i)
            for menu_id in menu_id_list:
                menu = MenuModels.query.get(int(menu_id))
                user.menus.append(menu)
            db.session.add(user)
            db.session.commit()

            return restful.success()

        else:
            if user:
                return restful.params_error('该员工已存在系统里，如果有新增的同名员工，可在名字后面加数字以示区分，如小明2...')
            else:
                user = CMSUser(username=chef_name, password=88888888, phone_number=1111, TAG=1)
                for menu_id in menu_id_list:
                    menu = MenuModels.query.get(int(menu_id))
                    user.menus.append(menu)
                db.session.add(user)
                db.session.commit()
            return restful.success()


@bp.route('/delchef/', methods=['POST'])
@login_required
def delchef():
    chef_name = request.form['chef_name']
    user = CMSUser.query.filter_by(username=chef_name).first()
    if not user:
        return restful.params_error(message='信息有误！')
    user.TAG = 0
    db.session.commit()
    return restful.success()


@bp.route('/scoreall/')
@login_required
def scoreall():
    menus = MenuModels.query.order_by(MenuModels.menu_num).all()

    month_list = get_month_range(config.START_TIME, datetime.datetime.now())

    table_nums = DiningTableModel.query.all()

    month_list.reverse()
    context = {
        'menus': menus,
        'month_list': month_list,
        'table_nums': table_nums
    }
    return render_template('cms/score_all.html', **context)


@bp.route('/scoredata/', methods=['POST'])
@login_required
def scoredata():
    cur_month = request.form['cur_month']
    cur_menu_id = request.form['cur_menu_id']
    table_num_id = request.form['table_num_id']

    cur_month = cur_month.split('. ')[1]
    cur_menu = MenuModels.query.get(cur_menu_id)

    year, month = cur_month.split('-')
    week, month_days = calendar.monthrange(int(year), int(month))  # 查看一一个月有几天，输出元祖（(2, 31)）,2代表第一天星期几
    start_time = cur_month + '-01'
    end_time = cur_month + '-' + str(month_days)
    scores = cur_menu.menu_score.filter(ScoreModel.create_time.between(start_time, end_time)).order_by(
        ScoreModel.create_time.desc()).all()

    servers = ServerScoreModel.query.filter(ServerScoreModel.create_time.between(start_time, end_time)).order_by(
        ServerScoreModel.create_time.desc()).all()
    if int(table_num_id) != 0:
        servers = [i for i in servers if int(i.table_num_id) == int(table_num_id)]

    # print(servers)
    server_dict = {}
    for i in range(0, len(servers)):
        # print(servers[i].get_data())
        server_dict[str(i)] = servers[i].get_data()

    t = {}
    for i in range(0, len(scores)):
        t[str(i)] = scores[i].get_data()

    chefs = cur_menu.menu_to_users
    chef_user = [i.username for i in chefs]
    chef_user = list(set(chef_user))

    # 菜品分数分布统计
    count = [0] * 5
    # print(count)
    for i in scores:
        # print(i.score)
        count[i.score - 1] += 1
        # count[i.score2 - 1] += 1
        # count[i.score3 - 1] += 1

    score_count = []
    for i in range(0, 5):
        tem_dict = {'value': count[i], 'name': str(i + 1)}
        score_count.append(tem_dict)

    # 服务分数分布统计
    s_count = [0] * 5
    for i in servers:
        s_count[i.server - 1] += 1
    server_count = []
    for i in range(0, 5):
        tem_dict = {'value': s_count[i], 'name': str(i + 1)}
        server_count.append(tem_dict)

        # 开始计数每天
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    now_year, now_month, now_day = now_time.split('-')
    if int(now_year) == int(year):
        if int(now_month) == int(month):
            day_num = int(now_day)
        else:
            day_num = month_days
    else:
        day_num = month_days
    start_year, start_month, start_day = str(config.START_TIME).split('-')
    sql_end_time = cur_month + '-' + str(day_num)
    sql_start_time = cur_month + '-01'

    if start_year == year:
        if int(start_month) == int(month):
            sql_start_time = str(config.START_TIME)

    query_sql = "SELECT create_time,chefs FROM score_data WHERE date(create_time)>=date('{start}') AND date(create_time)<=date ('{end}') AND menu_id='{menu_id}'".format(
        start=sql_start_time, end=sql_end_time, menu_id=cur_menu_id)
    df = pd_read_sql(query_sql)
    chef_user = list(set(df['chefs'].tolist()))
    chef_data = []
    for i in chef_user:
        if i:
            if ',' in i:
                chef_lis = i.split(',')
                for j in chef_lis:
                    if j not in chef_data:
                        chef_data.append(j)
            else:
                if i not in chef_data:
                    chef_data.append(i)

    df['create_time'] = pd.to_datetime(df['create_time'])
    day_df = df.groupby([df['create_time'].dt.day]).count()

    day_dict = day_df.to_dict()
    day_dict = day_dict.get('create_time')
    days = []
    count_num = []
    if day_dict:
        days = list(day_dict.keys())
        count_num = list(day_dict.values())

    tem_dict = {'score_data': t, 'chef_name': chef_data, 'score_count': score_count, 'days': days,
                'count_num': count_num, 'server_data': server_dict, 'server_count': server_count}
    data = {
        'code': 200,
        'data': tem_dict,
        'message': ''
    }
    return jsonify(data)


@bp.route('/chefscoreall/')
@login_required
def chefscoreall():
    chefs = CMSUser.query.filter(CMSUser.TAG != 2).order_by(CMSUser.TAG.desc()).all()

    context = {
        'chefs': chefs,

    }
    return render_template('cms/chef_score_all.html', **context)


@bp.route('/chefscoredata/', methods=['POST'])
@login_required
def chefscoredata():
    cur_chef = request.form['cur_chef']
    chef_name = cur_chef.split('.')[1]
    chef_name = chef_name.strip()
    scores = ScoreModel.query.filter(ScoreModel.chefs.contains(chef_name)).order_by(ScoreModel.create_time).all()
    month_list = get_month_range(config.START_TIME, datetime.datetime.now())
    month_list2 = []
    for i in month_list:
        tem_list = i.split('-')
        if len(tem_list[1]) == 1:
            tem_list[1] = '0' + tem_list[1]
        month = '-'.join(tem_list)
        month_list2.append(month)
    # month_list2.append('date')
    month_list2.insert(0, 'date')

    def score_month():
        score1 = [0] * (len(month_list))
        score2 = [0] * (len(month_list))
        score3 = [0] * (len(month_list))
        score4 = [0] * (len(month_list))
        score5 = [0] * (len(month_list))
        score1.insert(0, '1分')
        score2.insert(0, '2分')
        score3.insert(0, '3分')
        score4.insert(0, '4分')
        score5.insert(0, '5分')
        score_dict = {'date': month_list2, '1': score1, '2': score2, '3': score3, '4': score4, '5': score5, }
        for score in scores:
            index_num = month_list2.index(score.create_time.strftime('%Y-%m'))
            score_dict[str(score.score)][index_num] += 1
        month_score_data = list(score_dict.values())

        return month_score_data

    def menu_month():

        menu_dict = {'date': month_list2}
        for score in scores:
            menu = score.score_menu.menu_name
            if not menu_dict.get(menu):
                tem_lis = [0] * (len(month_list))
                tem_lis.insert(0, menu)
                menu_dict[menu] = tem_lis

        # for menu in menus:
        #     if not menu_dict.get(menu):
        #         tem_lis = [0] * (len(month_list))
        #         tem_lis.insert(0, menu)
        #
        #         menu_dict[menu] = tem_lis
        # print(menu_dict)

        # score_dict = {'date': month_list2, '': score1, '2': score2, '3': score3, '4': score4, '5': score5, }
        key_lis = []
        for score in scores:
            index_num = month_list2.index(score.create_time.strftime('%Y-%m'))
            menu_dict[score.score_menu.menu_name][index_num] += 1
            key_lis.append(score.score_menu.menu_name)
        menu_month_data = list(menu_dict.values())
        return menu_month_data

    month_score_data = score_month()
    month_menu_data = menu_month()
    # print(month_menu_data)
    data = {
        'code': 200,
        'data': {'month_score_data': month_score_data, 'month_menu_data': month_menu_data, 'end_date': month_list2[-1]},
        'message': ''
    }
    return jsonify(data)


@bp.route('/others/')
@login_required
def others():
    table_num = request.args.get('table-num')
    if table_num:
        old_table = DiningTableModel.query.filter_by(table_num=table_num).first()
        if not old_table:
            table = DiningTableModel(table_num=table_num)
            db.session.add(table)
            db.session.commit()

    table_nums = DiningTableModel.query.order_by(DiningTableModel.table_num).all()
    context = {
        'table_nums': table_nums
    }
    return render_template('cms/others.html', **context)

#
# @bp.route('/addtable/')
# def addtable():
#     table_num = request.args.get('table-num')
#     print(table_num)
