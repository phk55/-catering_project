import qrcode
from MyQR import myqr
from PIL import Image
from .qiniuupload import upload_qiniu2
import requests
from io import BytesIO
import time


def qr_with_central_img(link, central_picture, output_file):
    """

    :param link: 连接url
    :param central_picture: 中心图片
    :param output_file: 输出文件
    :return:
    """
    # 图片在二维码中心位置
    # time.sleep(1)
    qr = qrcode.QRCode(
        version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")

    response = requests.get(central_picture)  # 获取url图片
    icon = Image.open(BytesIO(response.content))  # 这里是二维码中心的图片


    # icon = Image.open(central_picture)  # 这里是二维码中心的图片

    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)
    img_byte=BytesIO()
    img.save(img_byte,format('PNG'))
    img_b=img_byte.getvalue()
    upload_qiniu2(img_b, output_file)
    return output_file
