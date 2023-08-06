# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0,<1', 'python-jose>=3.2,<4.0']

setup_kwargs = {
    'name': 'fastapi-resource-server',
    'version': '0.1.2',
    'description': 'Build resource servers with FastAPI',
    'long_description': '# FastAPI Resource Server\n\nBuild an OIDC resource server using FastAPI.\n\nYour aplication receives the claims decoded from the access token.\n\n# Usage\n\nRun keycloak on port 8888:\n\n```sh\ndocker container run --name auth-server -d -p 8888:8080 \\\n    -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin \\\n    jboss/keycloak:latest\n```\n\nInstall dependencies\n\n```sh\npip install fastapi fastapi_resource_server uvicorn\n```\n\nCreate the main.py module\n\n```python\nfrom fastapi import Depends, FastAPI, Security\nfrom pydantic import BaseModel\n\nfrom fastapi_resource_server import JwtDecodeOptions, OidcResourceServer\n\napp = FastAPI()\n\ndecode_options = JwtDecodeOptions(verify_aud=False)\n\nauth_scheme = OidcResourceServer(\n    "http://localhost:8888/auth/realms/master",\n    scheme_name="Keycloak",\n    jwt_decode_options=decode_options,\n)\n\n\nclass User(BaseModel):\n    username: str\n    given_name: str\n    family_name: str\n    email: str\n\n\ndef get_current_user(claims: dict = Security(auth_scheme)):\n    claims.update(username=claims["preferred_username"])\n    user = User.parse_obj(claims)\n    return user\n\n\n@app.get("/users/me")\ndef read_current_user(current_user: User = Depends(get_current_user)):\n    return current_user\n```\n\nRun the application\n\n```sh\nuvicorn main:app\n```\n',
    'author': 'Livio Ribeiro',
    'author_email': 'livioribeiro@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/livioribeiro/fastapi-resource-server',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
