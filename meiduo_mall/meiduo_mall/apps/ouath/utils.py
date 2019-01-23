from django.conf import settings
from itsdangerous import BadData
from itsdangerous import TimedJSONWebSignatureSerializer


def generate_encrypted_openid(openid):
    """
    生成加密的openid
    :param openid: 用户的openid
    """
    serializer = TimedJSONWebSignatureSerializer(
            settings.SECRET_KEY, expires_in=600)    # 有效期10分钟
    return serializer.dumps({'openid': openid}).decode()

def check_encrypted_openid(encrypted_openid):
    '''
    校验openid是否过期，是否被篡改
    :param encrypted_openid:
    :return: openid or None 加密的openid
    '''
    serializer = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY,600) #有效期10分钟

    try:
    # {'openid': xxxx}
        data = serializer.loads(encrypted_openid)

    except BadData:
        return None

    else:# 没有被篡改,也没有过期
        #这里是传递给序列化器检验，不是返回json，是个字典
        return data.get('openid')