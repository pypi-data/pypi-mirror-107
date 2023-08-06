#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/5/31 11:47
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : app.py
@Desc    : 应用实体
"""

import logging

_logger = logging.getLogger(__name__)


class App(object):

    def __init__(self, backend, id, name, desc, create_time, create_user_id, update_time, update_user_id):
        self._backend = backend
        self.id = id
        self.name = name
        self.desc = desc
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.update_time = update_time
        self.update_user_id = update_user_id

    def get(self):
        """
        # TODO()
        返回应用基础信息
        :return: Class `app` Object
        """
        pass

    def update(self, name, desc):
        """
        # TODO()
        更新模型基础信息
        :param name:应用名称
        :param desc:应用备注
        :return: Class `app` Object
        """
        pass

    def delete(self):
        """
        # TODO()
        删除当前应用
        :return:
        """
        pass

    def list_models(self):
        """
        # TODO()
        获取应用下模型对象列表
        :return: List of Class `Model` Object
        """

    def create_model(self, name, desc):
        """
        # TODO()
        当前应用下创建模型
        :param name:模型名称
        :param desc:模型备注
        :return: List of Class `Model` Object
        """
