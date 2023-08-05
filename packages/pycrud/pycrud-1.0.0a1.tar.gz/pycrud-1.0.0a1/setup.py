# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycrud',
 'pycrud.crud',
 'pycrud.crud.ext',
 'pycrud.helpers',
 'pycrud.helpers.fastapi_ext',
 'pycrud.helpers.pydantic_ext',
 'pycrud.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyPika>=0.42.1',
 'multidict>=4.5,<6.0',
 'pydantic>=1.6.1',
 'typing_extensions>=3.7.4.2']

setup_kwargs = {
    'name': 'pycrud',
    'version': '1.0.0a1',
    'description': 'A common crud framework for web.',
    'long_description': '# pycrud\n\n[![codecov](https://codecov.io/gh/fy0/pycrud/branch/master/graph/badge.svg)](https://codecov.io/gh/fy0/pycrud)\n\nAn async crud framework for RESTful API.\n\nFeatures:\n\n* Do CRUD operations by json.\n\n* Easy to integrate with web framework.\n\n* Works with popular orm.\n\n* Role based permission system\n\n* Data validate with pydantic.\n\n* Tested coveraged\n\n### Install:\n\n```bash\npip install pycrud==1.0.0a1\n```\n\n### Examples:\n\n#### CRUD service by fastapi and SQLAlchemy\n\n```python\nimport uvicorn\nfrom typing import Optional\nfrom fastapi import FastAPI, Request\nfrom fastapi.middleware.cors import CORSMiddleware\n\nfrom model_sqlalchemy import engine, UserModel, TopicModel\nfrom pycrud import Entity, ValuesToUpdate, ValuesToCreate, UserObject\nfrom pycrud.crud.ext.sqlalchemy_crud import SQLAlchemyCrud\nfrom pycrud.helpers.fastapi_ext import PermissionDependsBuilder\n\n# Crud Initialize\n\nclass User(Entity):\n    id: Optional[int]\n    nickname: str\n    username: str\n    password: str = \'password\'\n\n\nc = SQLAlchemyCrud(None, {\n    User: \'users\'\n}, engine)\n\n\nclass PDB(PermissionDependsBuilder):\n    @classmethod\n    async def validate_role(cls, user: UserObject, current_request_role: str) -> RoleDefine:\n        return c.default_role\n\n    @classmethod\n    async def get_user(cls, request: Request) -> UserObject:\n        pass\n\n# Web Service\n\napp = FastAPI()\napp.add_middleware(CORSMiddleware, allow_origins=[\'*\'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])\n\n\n@app.post("/user/create", response_model=User.dto.resp_create())\nasync def user_create(item: User.dto.get_create()):\n    return await c.insert_many(User, [ValuesToCreate(item)])  # response id list: [1]\n\n\n@app.get("/user/list", response_model=User.dto.resp_list())\nasync def user_list(query=PDB.query_info_depends(User)):\n    return [x.to_dict() for x in await c.get_list(query)]\n\n\n@app.post("/user/update", response_model=User.dto.resp_update())\nasync def user_list(item: User.dto.get_update(), query=PDB.query_info_depends(User)):\n    return await c.update(query, ValuesToUpdate(item))\n\n\n@app.post("/user/delete", response_model=User.dto.resp_delete())\nasync def user_delete(query=PDB.query_info_depends(User)):\n    return await c.delete(query)\n\n\nprint(\'Service Running ...\')\nuvicorn.run(app, host=\'0.0.0.0\', port=3000)\n```\n\nSee docs at `http://localhost:3000/redoc`\n\nYou can make requests like:\n\n`http://localhost:3000/topic/list?id.eq=1\nhttp://localhost:3000/topic/list?id.gt=1\nhttp://localhost:3000/topic/list?id.in=[2,3]\nhttp://localhost:3000/topic/list?user_id.eq=1\n`\n\n\n#### CRUD service with permission\n\nSee [Examples](/examples)\n\n#### Query filter\n\n```python\nfrom pycrud.values import ValuesToUpdate\nfrom pycrud.query import QueryInfo\n\n\nasync def fetch_list():\n    # dsl version\n    q1 = QueryInfo.from_table(User, where=[\n        User.id == 1\n    ])\n\n    # json verison\n    q2 = QueryInfo.from_json(User, {\n        \'id.eq\': 1\n    })\n\n    lst = await c.get_list(q1)\n    print([x.to_dict() for x in lst])\n\n\nasync def update_by_ids():\n    v = ValuesToUpdate({\'nickname\': \'bbb\', \'username\': \'u2\'})\n\n    # from dsl\n    q1 = QueryInfo.from_table(User, where=[\n        User.id.in_([1, 2, 3])\n    ])\n\n    q2 = QueryInfo.from_json(User, {\n        \'id.in\': [1,2,3]\n    })\n\n    lst = await c.update(q1, v)\n    print(lst)\n\n\nasync def complex_filter_dsl():\n    # $or: (id < 3) or (id > 5)\n    (User.id < 3) | (User.id > 5)\n\n    # $and: 3 < id < 5\n    (User.id > 3) & (User.id < 5)\n\n    # $not: not (3 < id < 5)\n    ~((User.id > 3) & (User.id < 5))\n    \n    # logical condition: (id == 3) or (id == 4) or (id == 5)\n    (User.id != 3) | (User.id != 4) | (User.id != 5)\n\n    # logical condition: (3 < id < 5) or (10 < id < 15)\n    ((User.id > 3) & (User.id < 5)) | ((User.id > 10) & (User.id < 15))\n\n\nasync def complex_filter_json():\n    # $or: (id < 3) or (id > 5)\n    QueryInfo.from_json(User, {\n        \'$or\': {\n            \'id.lt\': 3,  \n            \'id.gt\': 5 \n        }\n    })\n    \n    # $and: 3 < id < 5\n    QueryInfo.from_json(User, {\n        \'$and\': {\n            \'id.gt\': 3,  \n            \'id.lt\': 5 \n        }\n    })\n    \n    # $not: not (3 < id < 5)\n    QueryInfo.from_json(User, {\n        \'$not\': {\n            \'id.gt\': 3,  \n            \'id.lt\': 5 \n        }\n    })\n\n    # logical condition: (id == 3) or (id == 4) or (id == 5)\n    QueryInfo.from_json(User, {\n        \'$or\': {\n            \'id.eq\': 3,  \n            \'id.eq.2\': 4,\n            \'id.eq.3\': 5, \n        }\n    })\n\n    # logical condition: (3 < id < 5) or (10 < id < 15)\n    QueryInfo.from_json(User, {\n        \'$or\': {\n            \'$and\': {\n                \'id.gt\': 3,\n                \'id.lt\': 5\n            },\n            \'$and.2\': {\n                \'id.gt\': 10,\n                \'id.lt\': 15\n            }\n        }\n    })\n```\n\n### Operators\n\n| type | operator | text |\n| ---- | -------- | ---- |\n| compare | EQ | (\'eq\', \'==\') |\n| compare | NE | (\'ne\', \'!=\') |\n| compare | LT | (\'lt\', \'<\') |\n| compare | LE | (\'le\', \'<=\') |\n| compare | GE | (\'ge\', \'>=\') |\n| compare | GT | (\'gt\', \'>\') |\n| relation | IN | (\'in\',) |\n| relation | NOT_IN | (\'notin\', \'not in\') |\n| relation | IS | (\'is\',) |\n| relation | IS_NOT | (\'isnot\', \'is not\') |\n| relation | PREFIX | (\'prefix\',) |\n| relation | CONTAINS_ALL | (\'contains_all\',) |\n| relation | CONTAINS_ANY | (\'contains_any\',) |\n| logic | AND | (\'and\',) |\n| logic | OR | (\'or\',) |\n',
    'author': 'fy',
    'author_email': 'fy0748@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fy0/pycrud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9',
}


setup(**setup_kwargs)
