# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meilisearch_fastapi',
 'meilisearch_fastapi.models',
 'meilisearch_fastapi.routes']

package_data = \
{'': ['*']}

install_requires = \
['async-search-client>=0.7.1,<0.8.0',
 'fastapi>=0.65.1,<0.66.0',
 'python-dotenv>=0.17.1,<0.18.0']

setup_kwargs = {
    'name': 'meilisearch-fastapi',
    'version': '0.2.1',
    'description': 'MeiliSearch integration with FastAPI',
    'long_description': '# MeiliSearch FastAPI\n\n![CI Status](https://github.com/sanders41/meilisearch-fastapi/workflows/CI/badge.svg?branch=main&event=push)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/meilisearch-fastapi/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/meilisearch-fastapi/main)\n[![Coverage](https://codecov.io/gh/sanders41/meilisearch-fastapi/branch/main/graphs/badge.svg?branch=main)](https://codecov.io/gh/sanders41/meilisearch-fastapi)\n[![PyPI version](https://badge.fury.io/py/meilisearch-fastapi.svg)](https://badge.fury.io/py/meilisearch-fastapi)\n\nMeiliSearch FastAPI provides [FastAPI](https://fastapi.tiangolo.com/) routes for interacting with [MeiliSearch](https://www.meilisearch.com/).\n\n## Installation\n\nUsing a virtual environmnet is recommended for installing this package. Once the virtual environment is created and activated install the package with:\n\n```sh\npip install meilisearch-fastapi\n```\n\n## Useage\n\nRoutes are split in groups so that different dependencies can be injected, and therefore different levels of access, can be given to different groups of routes.\n\n### Example with no authentication require for routes\n\n```py\nfrom fastapi import APIRouter, FastAPI\nfrom meilisearch_fastapi.routes import (\n    document_routes,\n    index_routes,\n    meilisearch_routes,\n    search_routes,\n    settings_routes,\n)\n\napp = FastAPI()\napi_router = APIRouter()\napi_router.include_router(document_routes.router, prefix="/documents")\napi_router.include_router(index_routes.router, prefix="/indexes")\napi_router.include_router(meilisearch_routes.router, prefix="/meilisearch")\napi_router.include_router(search_routes.router, prefix="/search")\napi_router.include_router(settings_routes.router, prefix="/settings")\n\napp.include_router(api_router)\n```\n\n### Example with routes requiring authentication\n\n```py\nfrom fastapi import APIRouter, FastAPI\nfrom meilisearch_fastapi import routes\n\nfrom my_app import my_authentication\n\napp = FastAPI()\napi_router = APIRouter()\napi_router.include_router(document_routes.router, prefix="/documents", dependeincies=[Depends(my_authentication)])\napi_router.include_router(index_routes.router, prefix="/indexes", dependeincies=[Depends(my_authentication)])\napi_router.include_router(meilisearch_routes.router, prefix="/meilisearch", dependeincies=[Depends(my_authentication)])\napi_router.include_router(search_routes.router, prefix="/search", dependeincies=[Depends(my_authentication)])\napi_router.include_router(settings_routes.router, prefix="/settings", dependeincies=[Depends(my_authentication)])\n\napp.include_router(api_router)\n```\n\nThe url for MeiliSearch and API key are read from environment variables. Putting these into a .env\nfile will keep you from having to set these variables each time the terminal is restarted.\n\n```txt\nMEILISEARCH_URL=http://localhost:7700  # This is the url for your instance of MeiliSearch\nMEILISEARCH_API_KEY=masterKey  # This is the API key for your MeiliSearch instance\n```\n\nNow the MeiliSearch routes will be available in your FastAPI app. Documentation for the routes can be viewed in the OpenAPI documentation of the FastAPI app. To view this start your fast api app and naviate to the docs `http://127.0.0.1:8000/docs` replacing hte url with the correct url for your app.\n\n## Contributing\n\nContributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)\n',
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sanders41/meilisearch-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
