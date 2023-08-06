# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logger_es_cli']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.13.0,<8.0.0',
 'logger-es-handler>=0.1.0,<0.2.0',
 'python-dotenv[cli]>=0.17.1,<0.18.0',
 'typer[all]>=0.3.2,<0.4.0',
 'ujson>=4.0.2,<5.0.0']

entry_points = \
{'console_scripts': ['logger-es-cli = logger_es_cli.cli_driver:app']}

setup_kwargs = {
    'name': 'logger-es-cli',
    'version': '0.3.1',
    'description': 'CLI for sending logging to elasticsearch',
    'long_description': '# logger-es-cli\n\nCLI for sending logging to elasticsearch (alpha version)\n\n## How to build package\n\n- needs to have poetry installed.\n\n  ```bash\n  sudo python3 -m pip install poetry\n  ```\n\n- optional\n\n  ```bash\n  sudo python3 -m pip install git+https://github.com/sharkguto/python-elasticsearch-logger\n  sudo python3 -m pip install python-dotenv[cli]\n  ```\n\n- run build command\n\n  ```bash\n  poetry build\n  ```\n\n## Access AWS ES with VPC access using a tunning ssh\n\n- open a terminal and issue the following command:\n\n  ```bash\n  ssh -L 9200:vpc-kibana-dashboard-maneiro-brbrhuehue.sa-east-1.es.amazonaws.com:443 -i ~/.ssh/your-private-key.pem ec2-user@5.6.7.8\n  ```\n\n- now try to send logs to elasticsearch\n\n## .env file env variables\n\nexample:\n\n```bash\n# kibana ip or dns\nKIBANA_SERVER=localhost\n# use SSL\nKIBANA_SSL=true\n# exclude default args from kibana\n# if true exclude those following args:\n# pathname,exc_info,exc_text,thread,threadName,stack_info,filename,processName,process,args,msg,name,levelname\nEXCLUDE_DEFAULT=true\n# kibana server port\nKIBANA_SERVER_PORT=9200\n# kibana username\nKIBANA_USERNAME=robots.logger\n# kibana password\nKIBANA_PASSWORD=fd89078C-2e8e-4549-b9de-B9955123a0e3\n# software environment\nENVIRONMENT=DEVELOPMENT\n# project name that is the same index name in elastic search\nPROJECT_NAME=gmf-tech-modulex\n# exclude args to send to elasticsearch\nEXCLUDE=thread,threadName,processName\n# a custom json file , to append when send logs to elasticsearch\nCUSTOM_FILE=/run/media/gustavo/backup/git-projects/logger-es-cli/custom.json\n# unbuffer sysout python\nPYTHONUNBUFFERED=true\n# send debug logs to es?\nSEND_DEBUG=false\n```\n\n## custom.json file\n\nexample:\n\n```json\n{\n  "username": "gustavo@gmf-tech.com",\n  "account": "system"\n}\n```\n\n## poetry export dependencies\n\n```bash\npoetry export -f requirements.txt --output requirements.txt\n```\n\n## run logger-es-cli with a .env file [dotenv dependence]\n\n```bash\ndotenv run -- logger-es-cli info \'alo mundo louco!!!\'\n```\n\n- Do not forget to issue command message with single quote. In bash if you send with double quotes, escape caracters will broken the CLI\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Gustavo Freitas',
    'author_email': 'gustavo@gmf-tech.com',
    'maintainer': 'Gustavo Freitas',
    'maintainer_email': 'gustavo@gmf-tech.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
