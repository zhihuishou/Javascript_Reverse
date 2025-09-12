import requests
import execjs
import re
cookies = {
    'sessionid' : 'yz27m41x2sz6ssib9lrp5ywbqc0skyjq'
}
url = "https://www.python-spider.com/challenge/11"

session = requests.session()

response =  session.get(url,cookies=cookies)

jscode = re.match("<script>(.*)</script>",response.text).group(1)


with open ("demo.js",'r',encoding='utf-8',errors='ignore') as f:
    result = execjs.compile(f.read().replace('__jscode',jscode)).call("decode")

cookies['__jsl_clearance'] = result.split('=')[1].split(';')[0]

response = session.get(url,cookies=cookies)
print(response.text)