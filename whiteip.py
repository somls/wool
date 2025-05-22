# cron: 10 */2 * * *
# new Env('IP');
#3288588344
#https://pd.qq.com/s/672fku8ge

#https://hk.yunhaoka.cn/#/pages/micro_store/index?agent_id=669709


import requests
import hashlib
import urllib.parse


JULIANG_KEY = ''  #  Key
JULIANG_TRADE_NO = ''  #  Trade No
XK_APIKEY = 'XKD06E94CA0984133474'  #  API Key
XK_SIGN = '56fc2032a5aa69ad75e8fcfdb4ee07c4'  #  Sign
XIEQU_UID = ''  #  UID
XIEQU_UKEY = ''  #  UKEY


class SignKit:

    @staticmethod
    def md5_sign(params, secret):
        sign_content = SignKit.get_sign_content(params)
        return hashlib.md5((sign_content + '&key=' + secret).encode('utf-8')).hexdigest()

    @staticmethod
    def get_sign_content(params):
        params.pop('sign', None)  #  sign
        sorted_params = sorted(params.items())
        sign_content = '&'.join([f"{k}={str(v)}" for k, v in sorted_params if str(v) is not None and not 
str(v).startswith('@')])
        return sign_content

def get_current_ip():
    response = requests.get('https://myip.ipip.net/json')
    data = response.json()
    return data['data']['ip']

def update_juliang_white_list(ip, JULIANG_KEY, JULIANG_TRADE_NO):
    if JULIANG_KEY and JULIANG_TRADE_NO:
        params = {
            'new_ip': ip,
            'reset': '1',
            'trade_no': JULIANG_TRADE_NO
        }
        sign = SignKit.md5_sign(params, JULIANG_KEY)
        query_string = urllib.parse.urlencode(params) + "&sign=" + sign

        url = f'http://v2.api.juliangip.com/dynamic/replaceWhiteIp?{query_string}'
        response = requests.get(url)
        return response.text

def update_xk_white_list(ip, XK_APIKEY, XK_SIGN):
    if XK_APIKEY and XK_SIGN:
        url = 
f'http://api2.xkdaili.com/tools/XApi.ashx?apikey={XK_APIKEY}&type=addwhiteip&sign={XK_SIGN}&flag=8&ip={ip}'
        response = requests.get(url)
        return response.text

def update_xiequ_white_list(ip, XIEQU_UID, XIEQU_UKEY):
    if XIEQU_UID and XIEQU_UKEY:
        url = f'http://op.xiequ.cn/IpWhiteList.aspx?uid={XIEQU_UID}&ukey={XIEQU_UKEY}&act=get'
        response = requests.get(url)
        data = response.text
        arr = data.split(',')
        if ip not in arr:
            
requests.get(f'http://op.xiequ.cn/IpWhiteList.aspx?uid={XIEQU_UID}&ukey={XIEQU_UKEY}&act=del&ip=all')
            response = 
requests.get(f'http://op.xiequ.cn/IpWhiteList.aspx?uid={XIEQU_UID}&ukey={XIEQU_UKEY}&act=add&ip={ip}')
            return 'xiequ' if response.status_code == 200 else 'xiequ'
        else:
            return 'ip'


def main():
    ip = get_current_ip()
    print('ip', ip)

    print('', update_juliang_white_list(ip, JULIANG_KEY, JULIANG_TRADE_NO))
    print('', update_xk_white_list(ip, XK_APIKEY, XK_SIGN))
    print('', update_xiequ_white_list(ip, XIEQU_UID, XIEQU_UKEY))

if __name__ == "__main__":
    main()

