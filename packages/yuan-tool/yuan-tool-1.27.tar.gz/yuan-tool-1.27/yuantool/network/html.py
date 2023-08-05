import socket
import requests
import logging

logger = logging.getLogger(__name__)

session = requests.Session()
session.keep_alive = False


class BaseMSG:
    @classmethod
    def msg(cls, res, **kwargs):
        """
        新修改判断逻辑，对于已有字段若更新为None则不更新
        :keyword enforce_update: bool 是否强制更新
               e.g. MSG.Success(code=None)
                    <<< {'code': 0, 'msg': '成功'}
                    MSG.Success(code=None,enforce_update=True)
                    <<< {'code': None, 'msg': '成功'}
        """
        # 修改写法，不接受更新参数为None的值
        if 'enforce_update' in kwargs and kwargs['enforce_update']:
            kwargs.pop('enforce_update')
            res.update(kwargs)
        else:
            res.update((k, v) for k, v in kwargs.items() if (k not in res) or v)
        return res


def get_html(url):
    # change_user_agent()
    html = requests.get(url)
    if html.status_code == 200:
        res = html.text
    else:
        res = False
    return res


def get_cookie(url):
    rep = session.get(url)
    return rep.cookies


def post_data(url, data):
    # change_user_agent()
    try:
        res = requests.post(url, data=str(data).encode('utf-8'))
        if res.status_code != 200:
            res = False
    except Exception as e:
        if 'Failed to establish a new connection:' in str(e):
            logger.warning(e)
            logger.warning(e)
        else:
            logger.warning(e, exc_info=True)
        res = False
    return res
