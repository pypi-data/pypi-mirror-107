#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# __main__.py
# @Author : Gustavo Freitas (gustavo@gmf-tech.com)
# @Link   :

from logger_es_cli.cli_driver import app
import sys


def main():
    app(prog_name="logger-es-cli")


if __name__ == "__main__":
    sys.exit(main())
