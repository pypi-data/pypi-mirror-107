import uuid
import requests
import hashlib
import time
import json

URL = 'https://openapi.youdao.com/api'
APP_KEY = '7de30b04ccc71072'
APP_SECRET = 'fkTdxTSV0oZuLrsLuPUYLJJNgpm7BWJP'


class Word:
    ''' errorCode	text	错误返回码	一定存在
        query	text	源语言	查询正确时，一定存在
        translation	Array	翻译结果	查询正确时，一定存在
        basic	text	词义	基本词典，查词时才有
        web	Array	词义	网络释义，该结果不一定存在
        l	text	源语言和目标语言	一定存在
        dict	text	词典deeplink	查询语种为支持语言时，存在
        webdict	text	webdeeplink	查询语种为支持语言时，存在
        tSpeakUrl	text	翻译结果发音地址	翻译成功一定存在，需要应用绑定语音合成实例才能正常播放否则返回110错误码
        speakUrl	text	源语言发音地址	翻译成功一定存在，需要应用绑定语音合成实例才能正常播放否则返回110错误码
        returnPhrase	Array	单词校验后的结果	主要校验字母大小写、单词前含符号、中文简繁体
    '''
    def __init__(self, translation, speakUrl, webdict, **kwargs) -> None:
        # 翻译结果
        # 列表 [英俊的]
        self.translation = translation[0]
        # 基本释义（查询内容是单词是才有）
        # 字典
        # 会用到的键值对{phonetic:"ˈhænsəm",explains:[adj. （男子）英俊的；可观的；大方的，慷慨的；健美而端庄的]}
        self.basic = []
        self.phonetic = ''
        if kwargs.get("basic"):
            basic = kwargs.get("basic")
            self.basic = basic['explains']
            self.phonetic = basic['phonetic']
        # 网络释义
        # 列表
        # [{"handsome":["英俊的","美观的","大方的","漂亮的"]},
        #  {"handsome siblings":["绝代双骄","新绝代双骄","旷世双骄"]},
        #  {"handsom man reiver":["江玉郎","英俊的男人河"]}
        # ]
        self.web = {}
        if kwargs.get("web"):
            web = kwargs.get("web")
            for item in web:
                self.web[item['key']] = item['value']
        # 发音地址（audio/mp3）
        # 网址 content-type:audio/mp3
        self.speakUrl = speakUrl
        # 词典地址
        # 字典
        # {url:"http://mobile.youdao.com/dict?le=eng&q=handsome"}
        self.webdict = webdict["url"]

    def __repr__(self) -> str:
        return self.translation[0] + f"({self.webdict['url']})"


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(URL, data=data, headers=headers)


def phrase(word_json):
    ''' errorCode	text	错误返回码	一定存在
        query	text	源语言	查询正确时，一定存在
        translation	Array	翻译结果	查询正确时，一定存在
        basic	text	词义	基本词典，查词时才有
        web	Array	词义	网络释义，该结果不一定存在
        l	text	源语言和目标语言	一定存在
        dict	text	词典deeplink	查询语种为支持语言时，存在
        webdict	text	webdeeplink	查询语种为支持语言时，存在
        tSpeakUrl	text	翻译结果发音地址	翻译成功一定存在，需要应用绑定语音合成实例才能正常播放否则返回110错误码
        speakUrl	text	源语言发音地址	翻译成功一定存在，需要应用绑定语音合成实例才能正常播放否则返回110错误码
        returnPhrase	Array	单词校验后的结果	主要校验字母大小写、单词前含符号、中文简繁体
    '''

    word_dict = json.loads(word_json)
    return Word(**word_dict)


def connect(word):
    q = word

    data = {}
    data['from'] = 'auto'
    data['to'] = 'auto'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        # millis = int(round(time.time() * 1000))
        # filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        # fo = open(filePath, 'wb')
        # fo.write(response.content)
        # fo.close()
        return response.content
    else:
        # print(response.content)
        return response.text


if __name__ == '__main__':
    txt = connect("computer")
    word = Word(**json.loads(txt))
    print(word.translation)
    print(f"basic: {word.basic}")
    print(f"web: {word.web}")