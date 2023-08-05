import re
import socket
import json
import logging
from IPy import IP
from .html import get_html, post_data

logger = logging.getLogger(__name__)


def get_addr_from_ip_by_whois(target):
    try:
        api = f'http://whois.pconline.com.cn/ipJson.jsp?ip={target}&json=true'
        info = get_html(api)
        info = json.loads(info)
        info = json.loads(info)
        res = info
    except Exception as e:
        logger.warning(e, exc_info=True)
        res = False
    return res


def get_jw_from_addr_by_mapqq(city):
    try:
        api = 'https://apis.map.qq.com/jsapi?qt=poi&wd=' + city
        info = get_html(api)
        info = json.loads(info)
        pointx = info['detail']['city']['pointx']
        pointy = info['detail']['city']['pointy']
    except Exception as e:
        logger.warning(e, exc_info=True)
        pointx = 0
        pointy = 0
    return pointx, pointy


def get_fingerprint_from_ip_by_whatweb(target):
    api = 'http://whatweb.bugscaner.com/what.go'
    _data = {'url': target, 'location_capcha': 'no'}
    try:
        info = post_data(api, _data)
        print('获取信息', info)
        if info:
            res = info
        else:
            res = False
    except Exception as e:
        logger.warning(e)
        res = False
    return json.loads(res.text)


def is_domain(domain):
    """判断是否是域名"""
    if re.match('(.+?\.)+[a-zA-Z0-9]+', domain):
        res = True
    else:
        res = False
    return res


def is_ip(target):
    """判断是否是ip"""
    return is_ipv6(target) or is_ipv4(target)


def is_ipv6(target):
    """判断是否是IPv6"""
    return re.search(
        r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$',
        target)


def is_ipv4(target):
    """判断是否是IPv4"""
    try:
        return re.search(r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$', target)
    except:
        return None


def is_ipv4_cidr(target):
    """判断是否是IPv4的网段"""
    return re.search(
        r'^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}\/(([12]{0,1}[0-9])|(3[0-2]))$',
        target)


def get_ip_from_target(url):
    try:
        domain = get_domain(url)
        myaddr = socket.getaddrinfo(domain, 'http')
        return myaddr[0][4][0]
    except socket.gaierror:
        logger.warning("{}未能找到ip".format(url))
        return None


def get_domain(site):
    if site.startswith('http://'):
        site = site[7:]
    elif site.startswith("https://"):
        site = site[8:]
    if site.endswith('/'):
        site = site[:-1]
    return site


# ########################分割IP段部分#########################


def split(ip_str: str):
    try:
        return split_cidr(ip_str)
    except:
        if len(ip_str.split('.')) == 4:
            return split_star_and_sections(ip_str)
        elif len(ip_str.split('.')) == 8 and '-' in ip_str:
            return split_ip_s_ip(ip_str)
        else:
            raise ValueError('{} is a invalid ip like str'.format(ip_str))


def split_star_and_sections(ip: str):
    """
    处理各处带星号、带横杠的单ip
    :param ip: 192.168.1.*   192.168.1-5.*
    """
    ips = list(ip.split('.'))
    for index, num in enumerate(ips):
        if '-' in num:
            try:
                start, end = num.split('-')
                assert start.isdigit(), end.isdigit()
                ips[index] = [x for x in range(int(start), int(end) + 1)]
            except (ValueError, AssertionError):
                ips[index] = [x for x in range(1, 256)]
        elif num.isdigit():
            ips[index] = [num]
        else:
            ips[index] = [x for x in range(1, 256)]

    return ['{}.{}.{}.{}'.format(n0, n1, n2, n3) for n3 in ips[3] for n2 in ips[2] for n1 in ips[1] for n0 in ips[0]]


def split_ip_s_ip(ip2ip_str):
    """
    处理两个具体ip的范围
    :param ip2ip_str: 形如192.168.1.250-192.168.2.5
    """
    ipx = ip2ip_str.split('-')
    ip2num = lambda x: sum([256 ** i * int(j) for i, j in enumerate(x.split('.')[::-1])])
    num2ip = lambda x: '.'.join([str(x // (256 ** i) % 256) for i in range(3, -1, -1)])
    a = [num2ip(i) for i in range(ip2num(ipx[0]), ip2num(ipx[1]) + 1) if not ((i + 1) % 256 == 0 or i % 256 == 0)]
    return a


def split_cidr(ip):
    """
    处理标准ip段
    :param ip: 192.168.1.0/24
    """
    return [str(i) for i in IP(ip)]
