# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bx_py_utils',
 'bx_py_utils.aws',
 'bx_py_utils.humanize',
 'bx_py_utils.test_utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['publish = bx_py_utils_tests.publish:publish']}

setup_kwargs = {
    'name': 'bx-py-utils',
    'version': '38rc1',
    'description': 'Various Python utility functions',
    'long_description': '# Boxine - bx_py_utils\n\nVarious Python utility functions\n\n\n## Quickstart\n\n```bash\npip install bx_py_utils\n```\n\n\n## Existing stuff\n\nHere only a simple list about existing utilities.\nPlease take a look into the sources and tests for deeper informations.\n\n\n[comment]: <> (✂✂✂ auto generated start ✂✂✂)\n\n### bx_py_utils.anonymize\n\n* `anonymize()` - Anonymize the given string with special handling for eMail addresses.\n\n### bx_py_utils.auto_doc\n\n* `assert_readme()` - Check and update README file with generate_modules_doc()\n* `generate_modules_doc()` - Generate a list of function/class information via pdoc.\n\n#### bx_py_utils.aws.client_side_cert_manager\n\n* `ClientSideCertManager()` - Helper to manage client-side TLS certificate via AWS Secrets Manager by\n\n#### bx_py_utils.aws.secret_manager\n\n* `SecretsManager()` - Access AWS Secrets Manager values\n\n### bx_py_utils.compat\n\n* `removeprefix()` - Backport of `removeprefix` from PEP-616 (Python 3.9+)\n* `removesuffix()` - Backport of `removesuffix` from PEP-616 (Python 3.9+)\n\n### bx_py_utils.dict_utils\n\n* `dict_get()` - nested dict `get()`\n* `pluck()` - Extract values from a dict, if they are present\n\n### bx_py_utils.environ\n\n* `cgroup_memory_usage()` - Returns the memory usage of the cgroup the Python interpreter is running in.\n\n### bx_py_utils.error_handling\n\n* `print_exc_plus()` - Print traceback information with a listing of all the local variables in each frame.\n\n### bx_py_utils.graphql_introspection\n\n* `introspection_query()` - Generate GraphQL introspection query with variable nested depth.\n\n### bx_py_utils.hash_utils\n\n* `url_safe_encode()` - Encode bytes into a URL safe string.\n* `url_safe_hash()` - Generate a URL safe hash with `max_size` from given string/bytes.\n\n#### bx_py_utils.humanize.pformat\n\n* `pformat()` - Format given object: Try JSON fist and fallback to pformat()\n\n#### bx_py_utils.humanize.time\n\n* `human_timedelta()` - Converts a time duration into a friendly text representation.\n\n### bx_py_utils.iteration\n\n* `chunk_iterable()` - Returns a generator that yields slices of iterable of the given `chunk_size`.\n\n### bx_py_utils.path\n\n* `assert_is_dir()` - Check if given path is a directory\n* `assert_is_file()` - Check if given path is a file\n\n### bx_py_utils.processify\n\n* `processify()` - Decorator to run a function as a process.\n\n### bx_py_utils.stack_info\n\n* `FrameNotFound()` - Base class for lookup errors.\n* `last_frame_outside_path()` - Returns the stack frame that is the direct successor of given "file_path".\n\n#### bx_py_utils.test_utils.assertion\n\n* `assert_equal()` - Check if the two objects are the same. Display a nice diff, using `pformat()`\n* `assert_text_equal()` - Check if the two text strings are the same. Display a error message with a diff.\n* `pformat_ndiff()` - Generate a `ndiff` from two objects, using `pformat()`\n* `pformat_unified_diff()` - Generate a unified diff from two objects, using `pformat()`\n* `text_ndiff()` - Generate a `ndiff` between two text strings.\n* `text_unified_diff()` - Generate a unified diff between two text strings.\n\n#### bx_py_utils.test_utils.datetime\n\n* `parse_dt()` - Helper for easy generate a `datetime` instance via string.\n\n#### bx_py_utils.test_utils.filesystem_utils\n\n* `FileWatcher()` - Helper to record which new files have been created.\n\n#### bx_py_utils.test_utils.mock_aws_secret_manager\n\n* `SecretsManagerMock()` - Mock for `bx_py_utils.aws.secret_manager.SecretsManager()`\n\n#### bx_py_utils.test_utils.mock_boto3session\n\n* `MockedBoto3Session()` - Mock for `boto3.session.Session()`\n\n#### bx_py_utils.test_utils.requests_mock_assertion\n\n* `assert_json_requests_mock()` - Check the requests history.\n\n#### bx_py_utils.test_utils.snapshot\n\nAssert complex output via auto updated snapshot files with nice diff error messages.\n\n* `assert_py_snapshot()` - Assert complex python objects vio PrettyPrinter() snapshot file.\n* `assert_snapshot()` - Assert given data serialized to JSON snapshot file.\n* `assert_text_snapshot()` - Assert "text" string via snapshot file\n\n#### bx_py_utils.test_utils.time\n\n* `MockTimeMonotonicGenerator()` - Helper to mock `time.monotonic()` in tests.\n\n[comment]: <> (✂✂✂ auto generated end ✂✂✂)\n\n\n## Backwards-incompatible changes\n\n### v36 -> v37 - Outsourcing Django stuff\n\nWe split `bx_py_utils` and moved all Django related utilities into the separated project:\n\n* https://github.com/boxine/bx_django_utils\n\nSo, `bx_py_utils` is better usable in non-Django projects, because Django will not installed as decency of "bx_py_utils"\n\n\n## developing\n\nTo start developing e.g.:\n\n```bash\n~$ git clone https://github.com/boxine/bx_py_utils.git\n~$ cd bx_py_utils\n~/bx_py_utils$ make\nhelp                 List all commands\ninstall-poetry       install or update poetry\ninstall              install via poetry\nupdate               Update the dependencies as according to the pyproject.toml file\nlint                 Run code formatters and linter\nfix-code-style       Fix code formatting\ntox-listenvs         List all tox test environments\ntox                  Run pytest via tox with all environments\ntox-py36             Run pytest via tox with *python v3.6*\ntox-py37             Run pytest via tox with *python v3.7*\ntox-py38             Run pytest via tox with *python v3.8*\ntox-py39             Run pytest via tox with *python v3.9*\npytest               Run pytest\npytest-ci            Run pytest with CI settings\npublish              Release new version to PyPi\nclean                Remove created files from the test project\n```\n\n\n## License\n\n[MIT](LICENSE). Patches welcome!\n\n## Links\n\n* https://pypi.org/project/bx-py-utils/\n',
    'author': 'Jens Diemer',
    'author_email': 'jens.diemer@boxine.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0.0',
}


setup(**setup_kwargs)
