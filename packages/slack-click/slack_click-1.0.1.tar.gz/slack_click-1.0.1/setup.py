# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_click']

package_data = \
{'': ['*']}

install_requires = \
['click<8',
 'first>=2.0.2,<3.0.0',
 'pyee>=8.1.0,<9.0.0',
 'slack-bolt>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'slack-click',
    'version': '1.0.1',
    'description': 'Click support for Slack-Bolt applications',
    'long_description': '# Click support for Slack Apps\n\nAs a Python\n[Slack-Bolt](https://slack.dev/bolt-python/tutorial/getting-started)\napplication developer I want to create slash-command that are composed with the\nPython [Click](https://click.palletsprojects.com/) package.  I use the\n[FastAPI](https://fastapi.tiangolo.com/) web framework in asyncio mode.\n\nI need support for  `--help` `--version` and any usage error to be properly\nsent as Slack messages.\n\n# Quick Start\n\nCheck out the [example](example/README.md) application.\n\n# Usage\n\nThe `slack-click` packagage provides the following to support the Slack environment:\n\n* *SlackClickCommand* - used as the `cls` parameter to the click.command decorator\n* *SlackClickGroup* - used as the `cls` parameter to the click.group decorator\n* *version_option* - used in the same was as the standard click.version_option decorator\n\nThe `slack-click` package provides a Slack Bolt registry adapter `SlackAppCommands`.\n\nExample for integrating with a Slack Bolt application:\n\n```python\nfrom fastapi import FastAPI\nfrom slack_bolt.async_app import AsyncApp\nfrom slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler\nfrom slack_click import SlackAppCommands\n\napi = FastAPI()\nslack_app = AsyncApp()\nslack_socket_handler = AsyncSocketModeHandler(slack_app)\nslack_commands = SlackAppCommands(app=slack_app)\n```\n\nA `SlackAppCommands` instance provides a `.register()` method decorator that is\nused to hook in the Slack bolt command handler process.  See examples below.\n\n---\nExample for definiting a Click command handler:\n\n```python\nimport click\nfrom slack_click import SlackClickCommand, version_option\nfrom slack_bolt.request.async_request import AsyncBoltRequest as Request\n\n@slack_commands.register()\n@click.command(name="/ping", cls=SlackClickCommand)\n@version_option(version="0.1.0")\n@click.pass_obj\nasync def cli_ping_command(obj: dict):\n    request: Request = obj["request"]\n    say = request.context["say"]\n    await say(f"Hiya <@{request.context.user_id}>.  Ping back at you :eyes:")\n```\n\n---\n\nExample for definiting a Click group handler "click" with a command "hello".\n\n```python\nimport click\nfrom slack_bolt.request.async_request import AsyncBoltRequest as Request\nfrom slack_click import SlackClickGroup, version_option\n\n@slack_commands.register()\n@click.group(name="/click", cls=SlackClickGroup)\n@version_option(version="0.1.0")\n@click.pass_obj\nasync def cli_click_group(obj: dict):\n    """\n    This is the Clicker /click command group\n    """\n    request: Request = obj["request"]\n    say = request.context["say"]\n    await say("`/click` command invoked without any commands or options.")\n\n\n@cli_click_group.command("hello")\n@click.pass_obj\nasync def click_hello_command(obj):\n    request: Request = obj["request"]\n    await request.context.say(f"Hi there <@{request.context.user_id}> :eyes:")\n```\n\n# Customizing Help\n\nIf you want to change the Slack message format for help or usage methods you can\nsubclass `SlackCLickCommand` or `SlackClickGroup` and overload the methods:\n\n* *format_slack_help* - returns the Slack message payload (dict) for `--help`\n* *format_slack_usage_help* - returns the Slack message payload (dict) when click exception `UsageError` is raised.\n\nFor implementation details, please refer to the `SlackClickHelper` class, the parent\nclass for the `SlackClickCommand` and `SlackClickGroup` classes.\n\n# References\n* [Click Package Home](https://click.palletsprojects.com/)\n* [Getting Started with Slack Bolt](https://slack.dev/bolt-python/tutorial/getting-started)\n* [Slack-Bolt-Python Github](https://github.com/slackapi/bolt-python)\n* [Internals of Bolt Callback Parameters](https://github.com/slackapi/bolt-python/blob/main/slack_bolt/listener/async_internals.py)\n',
    'author': 'Jeremy Schulman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeremyschulman/slack-click',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
