import json
import requests
from flask import current_app
from flask_babel import _
from hashlib import md5
import random


def translate(text, source_language, dest_language):
#     if 'MS_TRANSLATOR_KEY' not in current_app.config or \
#             not current_app.config['MS_TRANSLATOR_KEY']:
#         return _('Error: the translation service is not configured.')
#     auth = {
#         'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
#     r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
#                      '/Translate?text={}&from={}&to={}'.format(
#                          text, source_language, dest_language),
#                      headers=auth)

    baidu_app_id = current_app.config['BAIDU_APP_ID']
    baidu_translator_key = current_app.config['BAIDU_TRANSLATOR_KEY']
    baidu_sault = random.randint(32768, 65536)
    baidu_sign = baidu_app_id + text + str(baidu_sault) + baidu_translator_key
    baidu_sign = md5(baidu_sign.encode('utf-8')).hexdigest()
    r = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate?q={}&from={}&to={}&appid={}&salt={}&sign={}'.format(
                         text.encode('utf-8'), source_language, dest_language, baidu_app_id, baidu_sault, baidu_sign))

    if r.status_code != 200:
        return _('Error: the translation service failed.')
#     return json.loads(r.content.decode('utf-8-sig'))
    return json.loads(r.content.decode('utf-8-sig'))["trans_result"][0]["dst"]
