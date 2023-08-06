# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_data_tools',
 'aws_data_tools.cli',
 'aws_data_tools.models',
 'aws_data_tools.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.80,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'dacite>=1.6.0,<2.0.0',
 'pyhumps>=3.0.2,<4.0.0',
 'structlog>=21.1.0,<22.0.0']

extras_require = \
{'devtools': ['ipdb[all,devtools]>=0.13.8,<0.14.0',
              'notebook[all,devtools]>=6.4.0,<7.0.0',
              'pre-commit[all,devtools]>=2.13.0,<3.0.0'],
 'docs': ['mkdocs[all,docs]>=1.1.2,<2.0.0',
          'mkdocs-git-revision-date-localized-plugin[all,docs]>=0.9.2,<0.10.0',
          'mkdocs-macros-plugin[all,docs]>=0.5.5,<0.6.0',
          'mkdocs-material[all,docs]>=7.1.5,<8.0.0']}

entry_points = \
{'console_scripts': ['awsdata = aws_data_tools.cli:cli']}

setup_kwargs = {
    'name': 'aws-data-tools',
    'version': '0.1.0a1',
    'description': 'A set of Python libraries for querying and transforming data from AWS APIs',
    'long_description': '# AWS Data Tools\n\nAn set of opinioned (but flexible) Python libraries for querying and transforming data\nfrom various AWS APIs, as well as a CLI interface.\n\nThis is in early development.\n\n## Data Types and Sources\n\nThe goal of this package is to provide consistent, enriched schemas for data from both\nraw API calls and data from logged events. We should also be able to unwrap and parse\ndata from messaging and streaming services like SNS, Kinesis, and EventBridge.\n\nHere are some examples:\n\n- Query Organizations APIs to build consistent, denormalized models of organizations\n- Validate and enrich data from CloudTrail log events\n- Parse S3 and ELB access logs into JSON\n\nThis initial release only contains support for managing data from AWS Organizations\nAPIs.\n\nThe following table shows what kinds of things may be supported in the future:\n\n| Library Name  | Description                                                       | Data Type | Data Sources                                                  | Supported |\n|---------------|-------------------------------------------------------------------|-----------|---------------------------------------------------------------|-----------|\n| organizations | Organization and OU hierarchy, policies, and accounts             | API       | Organizations APIs                                            | ☑         |\n| cloudtrail    | Service API calls recorded by CloudTrail                          | Log       | S3 / SNS / SQS / CloudWatch Logs / Kinesis / Kinesis Firehose | ☐         |\n| s3            | Access logs for S3 buckets                                        | Log       | S3 / SNS / SQS                                                | ☐         |\n| elb           | Access logs from Classic, Application, and Network Load Balancers | Log       | S3 / SNS / SQS                                                | ☐         |\n| vpc_flow      | Traffic logs from VPCs                                            | Log       | S3 / CloudWatch Logs / Kinesis / Kinesis Firehose             | ☐         |\n| config        | Resource state change events from AWS Config                      | Log       | S3 / SNS / SQS                                                | ☐         |\n| firehose      | Audit logs for Firehose delivery streams                          | Log       | CloudWatch Logs / Kinesis / Kinesis Firehose                  | ☐         |\n| ecs           | Container state change events                                     | Log       | CloudWatch Events / EventBridge                               | ☐         |\n| ecr           | Repository events for stored images                               | Log       | CloudWatch Events / EventBridge                               | ☐         |\n\nReferences:\n\n- CloudWatch Logs: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/aws-services-sending-logs.html\n- CloudWatch Events: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html\n\n## Installing\n\n---\n\n**NOTE**: None of the following installation methods actually work. This is stubbed out\nto include possible future installation methods.\n\n---\n\nUsing pip should work on any system with at least Python 3.9:\n\n`$ pip install aws-data-tools`\n\n### MacOS\n\nWith homebrew:\n\n`$ brew install aws-data-tools-py`\n\nUsing the pkg installer:\n\n(This isn\'t how we\'ll want to do this. We want to bundle the application with _all_ its\ndependencies, including Python itself. This probably means using pyInstaller to bundle\nan "app" image.)\n\n```\n$ LATEST=$(gh release list --repo timoguin/aws-data-tools-py | grep \'Latest\' | cut -f1)\n$ curl -sL https://github.com/segmentio/aws-okta/releases/download/aws-data-tools-py.pkg --output aws-data-tools-py_$LATEST.pkg\n$ installer -pkg aws-data-tools.py_$LATEST.pkg -target /usr/local/bin\n```\n\n### Windows\n\nWith chocolatey:\n\n`$ choco install aws-data-tools-py`\n\n## Usage\n\nEmpty.\n\n## Testing\n\n### Organizations Data ETL\n\n- Bring up localstack instance (Pro) running IAM and Organizations (master account)\n- Seed instance with Organization data (OUs, accounts, policies)\n- Run script that performs ETL against data from the AWS Organizations APIs\n- Ensure generated data is the same as the seed data\n',
    'author': "Tim O'Guin",
    'author_email': 'timoguin@gmail.com',
    'maintainer': "Tim O'Guin",
    'maintainer_email': 'timoguin@gmail.com',
    'url': 'https://timoguin.github.io/aws-data-tools-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
