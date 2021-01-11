import qiniu
import config
import datetime


def upload_qiniu(filestorage,filename):
    access_key = config.UEDITOR_QINIU_ACCESS_KEY
    secret_key = config.UEDITOR_QINIU_SECRET_KEY

    # 构建鉴权对象
    q = qiniu.Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = config.UEDITOR_QINIU_BUCKET_NAME

    # 设置 上传之后保存文件的名字
    # filename = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))+'_'+filestorage.filename

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filename, 3600)

    # put_file()
    ret, info = qiniu.put_data(token, filename, filestorage.read())
    # print(ret, info)

    if info.status_code == 200:
        return filename
    return None



def upload_qiniu2(filestorage,filename):

    """

    :param filestorage: 二进制流文件
    :param filename: 输出的文件名
    :return: 输出的文件名
    """
    access_key = config.UEDITOR_QINIU_ACCESS_KEY
    secret_key = config.UEDITOR_QINIU_SECRET_KEY

    # 构建鉴权对象
    q = qiniu.Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = config.UEDITOR_QINIU_BUCKET_NAME

    # 设置 上传之后保存文件的名字
    # filename = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))+'_'+filestorage.filename

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filename, 3600)

    # put_file()
    # print(filestorage,'ddd')
    ret, info = qiniu.put_data(token, filename, filestorage)
    # print(ret, info)

    if info.status_code == 200:
        return filename
    return None
