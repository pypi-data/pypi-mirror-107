import os
import yaml
import shutil
import gzip
import ruamel.yaml
import zipfile
import uuid
import logging

logger = logging.getLogger(__name__)


def read_file(file, mode='r', encoding='utf-8'):
    """
    :param file: 文件名
    :param encoding: 编码，默认utf-8
    :return:
    """
    with open(file, mode, encoding=encoding) as f:
        return f.read()


def readline_file(file, encoding='utf-8'):
    """
    :param file: 文件名
    :param encoding: 编码，默认utf-8
    :return:
    """
    with open(file, 'r', encoding=encoding) as f:
        return f.readline()


def read_yaml(config_path, config_name=''):
    """
    config_path:配置文件路径
    config_name:需要读取的配置内容,空则为全读
    """
    if config_path:
        with open(config_path, 'r', encoding="utf-8") as f:
            conf = yaml.safe_load(f.read())  # yaml.load(f.read())
        if not config_name:
            return conf
        elif config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')


def round_read_yaml(path):
    """
    保留yaml所有注释，锚点的读取
    """
    with open(path, 'r', encoding="utf-8") as f:
        doc = ruamel.yaml.round_trip_load(f)
    return doc


def round_save_yaml(path, doc):
    """
    保留yaml所有注释，锚点的保存
    """
    with open(path, 'w', encoding="utf-8") as f:
        ruamel.yaml.round_trip_dump(doc, f, default_flow_style=False)


def read_file_index(file_path):
    num = readline_file(file_path)
    return int(num)


def save_file_index(file_path, cnt):
    with open(file_path, 'w+', encoding="utf-8") as f:
        f.write(str(cnt))


def move_file(src_file, dst_path) -> bool:
    if not os.path.isfile(src_file):
        print("文件不存在")
        return False
    else:
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        shutil.move(src_file, dst_path)
        print("move %s -> %s" % (src_file, dst_path))
        return True


def unpack_file(src_file, dst_path):
    try:
        with gzip.open(src_file, "rb") as s_file, open(dst_path, "wb") as d_file:
            shutil.copyfileobj(s_file, d_file)
    except Exception as e:
        print(e)
        os.remove(dst_path)
        print("移除错误解压后文件")
    finally:
        os.remove(src_file)
        print("正在删除gz压缩文件")


def deflated_zip(target, filename, file_url):
    f = zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED)
    f.write(filename, file_url)
    f.close()


def extract_zip(zip_path, target_path):
    """
    解压zip
    解压成功：返回解压出的文件路径
    解压失败：返回False
    """
    try:
        uuid_str = uuid.uuid4().hex
        f = zipfile.ZipFile(zip_path, 'r')
        f.extractall(path=target_path + '/' + uuid_str)
        # corrector(target_path)
    except Exception as e:
        logger.error(e, exc_info=True)
        return False

    return target_path + '/' + uuid_str
