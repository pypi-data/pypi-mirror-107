#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# dafaults.py
# @Author : Gustavo Freitas (gustavo@gmf-tech.com)
# @Link   :

# from pydantic import BaseModel, Field, validator
# import typer


from enum import Enum


class EnvironmentEnum(str, Enum):
    dev = "DEVELOPMENT"
    prd = "PRODUCTION"
    uat = "HOMOLOGATION"


# class CustomerBase(BaseModel):
#     kibana_server: str = typer.Argument("127.0.0.1", envvar="KIBANA_SERVER")


# def our_decorator(func):
#     """Decorator that inject default arguments"""

#     def wrap(*args, **kwargs):
#         result = func(*args, **kwargs)

#         print(func.__name__, "inject default env variables")
#         return result

#     return wrap

# def decorator_factory(argument):
#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             #funny_stuff()
#             #something_with_argument(argument)
#             result = function(*args, **kwargs)
#             #more_funny_stuff()
#             return result
#         return wrapper
#     return decorator
