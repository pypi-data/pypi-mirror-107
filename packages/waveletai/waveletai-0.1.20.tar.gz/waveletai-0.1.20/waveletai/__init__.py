import logging
from waveletai import constants
import threading
from waveletai.sessions import Session
from waveletai.backends.hosted_backend import HostedBackend
from waveletai.constants import ModelRegisterMode

logging.basicConfig(format='[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                    level=logging.INFO)

_logger = logging.getLogger(__name__)

__lock = threading.RLock()

""""Access as an anonymous user.
You can pass this value as api_token during init() call, either by an environment variable or passing it directly
"""
ANONYMOUS = constants.ANONYMOUS
"""Anonymous user API token.
You can pass this value as api_token during init() call, either by an environment variable or passing it directly
"""
ANONYMOUS_API_TOKEN = constants.ANONYMOUS_API_TOKEN
from waveletai._version import get_versions

__version__ = get_versions()['version']

_backend = None


def init(name=None, pwd=None, backend=None):
    with __lock:
        global _backend

        if backend is None:
            # backend_name = os.getenv(envs.BACKEND)
            # if backend_name == 'offline':
            #     backend = OfflineBackend()

            # elif backend_name is None:
            _backend = HostedBackend(name, pwd)

            # else:
            #     raise InvalidBackend(backend_name)
        return _backend
        # session = Session(backend=backend)
        # return session


def create_app(name, desc):
    """
    创建应用
    :param name: 应用名称
    :param desc: 应用说明
    :return: App对象
    """
    pass


def get_app(app_id):
    """
    获取应用
    :param app_id: 应用ID
    :return: App对象
    """
    pass


def create_dataset(name, zone, path, data_type=constants.DataType.TYPE_FILE.value, desc=None):
    """
    创建数据集
    :param name: 数据集名称
    :param zone: 数据集区域
    :param path: 要上传的本地数据的路径
    :param data_type: 一个数据集中的数据类型是唯一的。备选值constants.DataType，固定提供图片、文件、视频、视频帧的数据类型
    :param desc: 数据集详情
    :return: Dataset对象
    """
    global _backend
    return _backend.create_dataset(name, zone, path, data_type, desc)


def get_dataset(dataset_id):
    """
    获取数据集对象
    :param dataset_id:数据集ID
    :return: Dataset对象
    """
    global _backend
    return _backend.get_dataset(dataset_id)


def download_dataset_artifact(dataset_id, path, destination):
    """
    获取模型对象
    :param dataset_id:数据集ID
    :param path:路径
    :param type:数据集类型
    :param destination:本地存储路径
    :return:
    """
    global _backend
    return _backend.download_dataset_artifact(dataset_id, path, destination)


def download_dataset_artifacts(dataset_id, destination):
    """
    获取模型对象
    :param dataset_id:数据集ID
    :param type:数据集类型
    :param destination:本地存储路径
    :return:
    """
    global _backend
    return _backend.download_dataset_artifacts(dataset_id, destination)


def upload_dataset_artifacts(dataset_id, path):
    """
    上传数据集资产文件
    :param dataset_id: 文件所属数据集
    :param path: 要上传的文件夹/文件路径
    :return:  上传文件 succ，共xxx个
    """
    global _backend
    return _backend.upload_dataset_artifacts(dataset_id, path)


def create_model(name, desc, app_id):
    """
    创建模型
    # TODO()
    :param name:模型名称
    :param desc:模型备注
    :param app_id:所属应用ID
    :return:
    """
    global _backend
    pass


def get_model(model_id):
    """
    获取模型对象
    :param model_id:模型ID
    :return:
    """
    global _backend
    return _backend.get_model(model_id)


def register_model_version(model_id, desc, artifacts, mode=ModelRegisterMode.PYFUNC.value):
    """
    注册模型库版本
    :param model_id: 模型ID
    :param desc: 备注
    :param artifacts: 注册文件路径，可以是文件夹,当为docker模式时，此处为docker-image,可以用save命令导出  eg：deployment.tar
    :param mode: 注册模式,默认为自定义(ModelRegisterMode.PYFUNC.value)
    :return:
    """
    global _backend
    return _backend.register_model_version(model_id, desc, artifacts, mode)


def get_model_version_by_model(model_id, version):
    """
    过模型获取模型库指定信息
    # TODO()
    :param model_id: 模型ID
    :param version:模型版本号
    :return:
    """


def get_model_version_by_id(model_version_id):
    """
    通过模型库ID获取模型库指定信息
    # TODO()
    :param model_version_id:模型库ID
    :return:
    """
