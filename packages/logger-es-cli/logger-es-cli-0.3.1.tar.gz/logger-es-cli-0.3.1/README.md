# logger-es-cli

CLI for sending logging to elasticsearch (alpha version)

## How to build package

- needs to have poetry installed.

  ```bash
  sudo python3 -m pip install poetry
  ```

- optional

  ```bash
  sudo python3 -m pip install git+https://github.com/sharkguto/python-elasticsearch-logger
  sudo python3 -m pip install python-dotenv[cli]
  ```

- run build command

  ```bash
  poetry build
  ```

## Access AWS ES with VPC access using a tunning ssh

- open a terminal and issue the following command:

  ```bash
  ssh -L 9200:vpc-kibana-dashboard-maneiro-brbrhuehue.sa-east-1.es.amazonaws.com:443 -i ~/.ssh/your-private-key.pem ec2-user@5.6.7.8
  ```

- now try to send logs to elasticsearch

## .env file env variables

example:

```bash
# kibana ip or dns
KIBANA_SERVER=localhost
# use SSL
KIBANA_SSL=true
# exclude default args from kibana
# if true exclude those following args:
# pathname,exc_info,exc_text,thread,threadName,stack_info,filename,processName,process,args,msg,name,levelname
EXCLUDE_DEFAULT=true
# kibana server port
KIBANA_SERVER_PORT=9200
# kibana username
KIBANA_USERNAME=robots.logger
# kibana password
KIBANA_PASSWORD=fd89078C-2e8e-4549-b9de-B9955123a0e3
# software environment
ENVIRONMENT=DEVELOPMENT
# project name that is the same index name in elastic search
PROJECT_NAME=gmf-tech-modulex
# exclude args to send to elasticsearch
EXCLUDE=thread,threadName,processName
# a custom json file , to append when send logs to elasticsearch
CUSTOM_FILE=/run/media/gustavo/backup/git-projects/logger-es-cli/custom.json
# unbuffer sysout python
PYTHONUNBUFFERED=true
# send debug logs to es?
SEND_DEBUG=false
```

## custom.json file

example:

```json
{
  "username": "gustavo@gmf-tech.com",
  "account": "system"
}
```

## poetry export dependencies

```bash
poetry export -f requirements.txt --output requirements.txt
```

## run logger-es-cli with a .env file [dotenv dependence]

```bash
dotenv run -- logger-es-cli info 'alo mundo louco!!!'
```

- Do not forget to issue command message with single quote. In bash if you send with double quotes, escape caracters will broken the CLI

## License

This project is licensed under the terms of the MIT license.
