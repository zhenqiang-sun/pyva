import os
import random
from shutil import copyfile

import cv2
import qrcode
import requests
from PIL import Image

from pyva.Global import G


def decodeQrcode(img_path):
    dir_path = os.path.abspath(os.curdir)
    file_path = dir_path + "/tmp_qrcode_" + str(random.randint(1, 9999)) + os.path.splitext(img_path)[-1]

    if os.path.isfile(img_path):
        copyfile(img_path, file_path)
    else:
        with open(file_path, "wb") as f:
            f.write(requests.get(url=img_path).content)

    # read the QRCODE image
    img = cv2.imread(file_path)
    os.remove(file_path)

    # create a qrcode detector
    detect = cv2.QRCodeDetector()

    try:
        # get the data and other threshold
        # put the image that we have read
        data, bbox, sqrcode = detect.detectAndDecode(img)

        # bbox is the main thing in the qrcode
        # if it exist it will give us the data
        if bbox is not None:
            return data
        else:
            data = decodeQrcodeByCaoliaoApi(img_path)

            if data == "解析失败1":
                return decodeQrcodeByUomgApi(img_path)
    except:
        return decodeQrcodeByCaoliaoApi(img_path)


def decodeQrcodeByMuxiaoguoApi(img_path):
    G.logger.info('decode by muxiaoguo api: {}'.format(img_path))
    api_url = 'https://api.muxiaoguo.cn/api/QrcodeRT?api_key=0d5f8678d522a4b2&url={}'.format(img_path)
    resp = requests.get(api_url)

    if resp.status_code == 200 and resp.json().get('code') == '200':
        data = resp.json()
        return str(data.get('data', {}).get('content', ''))
    else:
        G.logger.error('decode error by muxiaoguo api: {}'.format(api_url))
        return '解析失败'


def decodeQrcodeByUomgApi(img_path):
    G.logger.info('decode by uomg api: {}'.format(img_path))
    api_url = 'https://api.uomg.com/api/qr.encode?url={}'.format(img_path)
    resp = requests.get(api_url)

    if resp.status_code == 200 and resp.json().get('code') == 1:
        data = resp.json()
        return data.get('qrurl', '')
    else:
        G.logger.error('decode error by uomg api: {}'.format(api_url))
        return '解析失败'


def decodeQrcodeByCaoliaoApi(img_path):
    G.logger.info('decode by caoliao api: {}'.format(img_path))
    api_url = 'https://cli.im/Api/Browser/deqr'
    resp = requests.post(api_url, data={'data': img_path})

    if resp.status_code == 200 and resp.json().get('status') == 1:
        data = resp.json()
        result = data.get('data', {}).get('RawData', '')

        if result:
            return result
        else:
            return '解析失败2'
    else:
        G.logger.error('decode error by caoliao api: {}'.format(api_url))
        return '解析失败1'


def generateQrcode(text, file_path):
    img = qrcode.make(text)
    with open(file_path, 'wb') as f:
        img.save(f)


def generateQrcodeWithLogo(text, file_path, logo_path):
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=7,
        border=3,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(back_color="#FFF")

    # 添加logo，打开logo照片
    icon = Image.open(logo_path)
    # 获取图片的宽高
    img_w, img_h = img.size
    # 参数设置logo的大小
    factor = 1
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    # 重新设置logo的尺寸
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    # 得到画图的x，y坐标，居中显示
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    # 黏贴logo照
    img.paste(icon, (w, h), mask=None)

    with open(file_path, 'wb') as f:
        img.save(f)


if __name__ == '__main__':
    filePath = "https://dll-screen-prod.oss-cn-beijing.aliyuncs.com/screenQrCode/6aa3218b0c954935a71119534017c589.png"
    generateQrcodeWithLogo("https://mhimg.clewm.net/cli/images/beautify/new/logo/30.png", "vc.png",
                           "../templates/logo_zhifubao.png")
