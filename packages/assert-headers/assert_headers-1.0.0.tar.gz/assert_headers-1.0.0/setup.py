# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['assert_headers', 'assert_headers.getCLIConfiguration']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['assert-headers-py = assert_headers.cli:cli']}

setup_kwargs = {
    'name': 'assert-headers',
    'version': '1.0.0',
    'description': 'Assert HTTP headers.',
    'long_description': '# assert_headers\n\nAssert HTTP headers\n\n## Usage\n\n### CLI\n\n#### Global usage\n\n```bash\npip install assert_headers\n# Assume headersSchema.json in current working directory\nassert-headers-py https://example.com\n```\n\nor with specified configuration\n\n```bash\nassert-headers-py --config ./customConfiguration.json https://example.com\n```\n\nin silent mode\n\n```bash\nassert-headers-py --silent --config ./customConfiguration.json https://example.com\n```\n\nto see what version you are running\n\n```bash\nassert-headers-py --version\n```\n\n##### Advanced CLI Usage\n\nTODO: Add example of how to stream a column of a .csv into the tool\n\nTODO: Show how the exit codes can be used in smoke tests\n\n#### CLI Configuration\n\n`assert-headers-py` currently accepts configuration in JSON or YAML formats. It allows specifying a schema for the headers, but also the outgoing origin and user-agent headers for the request. Below is an example configuration:\n\n```json\n{\n  "userAgent": "assert-headers-py",\n  "origin": "https://example.com",\n  "schema": {\n    "cache-control": false,\n    "strict-transport-security": true,\n    "x-content-type-options": "nosniff",\n    "x-frame-options": {\n      "DENY": true,\n      "SAMEORIGIN": false\n    }\n  }\n}\n```\n\n```yaml\nuserAgent: "assert-headers-py"\norigin: "https://example.com"\nschema:\n  cache-control: False\n  strict-transport-security: True\n  x-content-type-options: "nosniff"\n  x-frame-options:\n    DENY: True\n    SAMEORIGIN: False\n```\n\n**Schema Explanation:**\n\n> Note: Since the example format of the schema is JSON, the values will use `false` instead of `False` and `true` instead of `True`.\n\n1. `"disallowed-header-name": false` - It is considered an error if this header is defined\n1. `"required-header-name": true` - It is considered an error if this header is missing (or `undefined`)\n1. `"strict-header-name": "only good value"` - It is considered an error if this header does not have this value\n1. `"enumerated-header-name": { "good header value": true, "another good value": true }` - It is considered an error if this header contains a value other than one marked `true`.\n1. `"enumerated-header-name": { "bad header value": false, "another bad value": false }` - It is considered an error if this header contains a value not marked `true`\n1. If no enumerated header values are marked `true`, all listed values are considered invalid values. It is highly recommended to ONLY use `true` and `false` for enumerated values\n\n### assertHeader\n\n```python\nfrom assert_headers import assertHeader\n\nheaders = {\n  "strict-transport-security": "max-age=31536000; includeSubDomains",\n  "x-content-type-options": "nosniff",\n  "x-frame-options": "DENY"\n}\nschema = {\n  "cache-control": False,\n  "strict-transport-security": True,\n  "x-content-type-options": "nosniff",\n  "x-frame-options": {\n    # if any are true, the header value must match a true schema value\n    "DENY": True\n  }\n}\n\ntry:\n  assertHeaders(headers, schema)\nexcept BaseException as err:\n  print("OOPS!")\n  print(err.message)\n  if err.errors:\n    for assertionError in err.errors:\n      print(f\'The header {assertionError.headerName} was bad!\')\n```\n\nThis can also be used inside a test library for validating HTTP response headers.\n\n### assertHeaderFromUrl\n\n```python\nfrom assert_headers import assertHeaderFromUrl\n\nconfiguration = {\n  "userAgent": "Custom User Agent name",\n  "origin": "https://my-domain.com",\n  "schema": {\n    "cache-control": False,\n    "strict-transport-security": True,\n    "x-content-type-options": "nosniff",\n    "x-frame-options": {\n      # if any are true, the header value must match a true schema value\n      "DENY": True\n    }\n  }\n}\n\nassertHeaderFromUrl("https://example.com/my-test-page", configuration)\n```\n\n## Contributing\n\n```bash\n# 1. Install Poetry\n# 2. Install dependencies\npoetry install\n# 3. Start contained environment\npoetry shell\n# 3 (alternate). Run virtualenv inside current shell\n# source ./venv/bin/activate\n# 4. Make changes\n# 5. Run tests\npoetry run pytest\n```\n\nIf installing additional dependencies:\n\n```bash\n# Inside Poetry shell or virtualenv/venv\npoetry add my_new_package\n```\n\nFor more information, refer to https://python-poetry.org/docs/basic-usage/.\n',
    'author': 'David Ragsdale',
    'author_email': 'pkgsupport@davidjragsdale.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/djragsdale/assert-headers-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
