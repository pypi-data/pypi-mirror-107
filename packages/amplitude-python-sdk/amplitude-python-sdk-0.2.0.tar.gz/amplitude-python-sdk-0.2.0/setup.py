# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amplitude_python_sdk',
 'amplitude_python_sdk.common',
 'amplitude_python_sdk.integration_tests.v1',
 'amplitude_python_sdk.integration_tests.v2.clients',
 'amplitude_python_sdk.tests.common',
 'amplitude_python_sdk.tests.v1',
 'amplitude_python_sdk.tests.v1.models',
 'amplitude_python_sdk.tests.v2.clients',
 'amplitude_python_sdk.tests.v2.models',
 'amplitude_python_sdk.v1',
 'amplitude_python_sdk.v1.models',
 'amplitude_python_sdk.v2',
 'amplitude_python_sdk.v2.clients',
 'amplitude_python_sdk.v2.exceptions',
 'amplitude_python_sdk.v2.models',
 'amplitude_python_sdk.v2.models.event']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'amplitude-python-sdk',
    'version': '0.2.0',
    'description': 'Client for the Amplitude HTTP V1 and V2 API (https://developers.amplitude.com/docs).',
    'long_description': "# amplitude-python-sdk\n\n**Unofficial** SDK for the Amplitude HTTP API, providing a user-friendly interface through Pydantic models.\n\nSee [the Amplitude docs](https://developers.amplitude.com/docs) for more information on the various API methods and their parameters.\n\n**WARNING: This library is in very early development, and APIs are not guaranteed to be stable. Please bear that in mind when using this library.**\n\n# Installation\n\n```\npip install amplitude-python-sdk\n```\n\n## Dependencies\n\n* [pydantic](https://github.com/samuelcolvin/pydantic) is used to create cleaner and more readable data models within this library.\n* [requests](https://github.com/psf/requests) is used to handle all HTTP interactions with the Amplitude API.\n\n# Usage\n\n## Methods supported\n\nCurrently, only the [Identify API](https://developers.amplitude.com/docs/identify-api) and the [HTTP API V2](https://developers.amplitude.com/docs/http-api-v2) are supported. Support for other API methods coming soon!\n\n## Identify API Example\n\n```python\nimport logging\n\nfrom amplitude_python_sdk.common.exceptions import AmplitudeAPIException\nfrom amplitude_python_sdk.v1.client import AmplitudeV1APIClient\nfrom amplitude_python_sdk.v1.models.identify import Identification, UserProperties\n\nclient = AmplitudeV1APIClient(api_key='<YOUR API KEY HERE>')\ntry:\n    resp = client.identify([Identification(user_id='example', user_properties=UserProperties()])\nexcept AmplitudeAPIException:\n    logging.exception('Failed to send identify request to Amplitude')\n```\n\n## Event API Client Example\n\n```python\nimport logging\n\nfrom amplitude_python_sdk.common.exceptions import AmplitudeAPIException\nfrom amplitude_python_sdk.v2.clients.event_client import EventAPIClient\nfrom amplitude_python_sdk.v2.models.event import Event\nfrom amplitude_python_sdk.v2.models.event.options import EventAPIOptions\n\nclient = EventAPIClient(api_key='<YOUR API KEY HERE>')\n\ntry:\n    events = [\n        Event(\n            user_id='example',\n            event_type='Clicked on Foo',\n            event_properties={\n                'foo_id': 'bar',\n                'click_position': 5,\n            }\n        )\n    ]\n    client.upload(\n        events=events,\n        options=EventAPIOptions(min_id_length=1),\n    )\nexcept AmplitudeAPIException:\n    logging.exception('Failed to log event to Amplitude')\n```\n\n## Batch Event Upload API Example\n\nExactly the same as the Event V2 API example, just substitute `client.batch_upload` for `client.upload`.\n",
    'author': 'Krishnan Chandra',
    'author_email': 'krishnan.chandra@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/researchrabbit/amplitude-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
