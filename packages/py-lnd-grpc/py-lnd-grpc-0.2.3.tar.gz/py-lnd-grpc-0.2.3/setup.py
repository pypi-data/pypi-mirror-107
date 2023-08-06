# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lndgrpc', 'lndgrpc.aio']

package_data = \
{'': ['*']}

install_requires = \
['aiogrpc>=1.8,<2.0',
 'googleapis-common-protos>=1.53.0,<2.0.0',
 'grpcio-tools>=1.37.0,<2.0.0',
 'grpcio>=1.37.0,<2.0.0',
 'protobuf3-to-dict>=0.1.5,<0.2.0',
 'protobuf>=3.15.8,<4.0.0']

setup_kwargs = {
    'name': 'py-lnd-grpc',
    'version': '0.2.3',
    'description': 'An rpc client for LND (lightning network deamon)',
    'long_description': '# lndgrpc\nA python grpc client for LND (Lightning Network Daemon) ⚡⚡⚡\n\nThis is a wrapper around the default grpc interface that handles setting up credentials (including macaroons). An async client is also available to do fun async stuff like listening for invoices in the background. \n\n## Dependencies\n- Python 3.6+\n- Working LND lightning node, take note of its ip address.\n- Copy your admin.macaroon and tls.cert files from your node to a directoy on your machine. \n\n\n## Installation\n```bash\npip install py-lnd-grpc\n\n# Test it is working\n# Set these values as needed!\nexport CRED_PATH=/path/to/macaroon/and/tls/cert\nexport LND_NODE_IP=192.168.1.xx\n\n# This will run a get_info() request on your node, checking its connection.\npython3 -m lndgrpc\n```\n\n## Basic Usage\nThe api mirrors the underlying lnd grpc api (http://api.lightning.community/) but methods will be in pep8 style. ie. `.GetInfo()` becomes `.get_info()`.\n\n### Configuration Environment Variables\n\n```bash\nexport CRED_PATH=/path/to/macaroon/and/tls/cert\nexport LND_NODE_IP=192.168.1.xx\n```\n\n```python\nfrom lndgrpc import LNDClient\n\n# pass in the ip-address with RPC port and network (\'mainnet\', \'testnet\', \'simnet\')\n# the client defaults to 127.0.0.1:10009 and mainnet if no args provided\nlnd = LNDClient("127.0.0.1:10009", network=\'simnet\')\n\n# Unlock you wallet\nlnd.unlock_wallet(wallet_password=b"your_wallet_password")\n\n# Get general data about your node\nlnd.get_info()\n\nprint(\'Listening for invoices...\')\nfor invoice in lnd.subscribe_invoices():\n    print(invoice)\n```\n\n### Async\n\n```python\nimport asyncio\nfrom lndgrpc import AsyncLNDClient\n\nasync_lnd = AsyncLNDClient()\n\nasync def subscribe_invoices():\n    print(\'Listening for invoices...\')\n    async for invoice in async_lnd.subscribe_invoices():\n        print(invoice)\n\nasync def get_info():\n    while True:\n        info = await async_lnd.get_info()\n        print(info)\n        await asyncio.sleep(5)\n\nasync def run():\n    coros = [subscribe_invoices(), get_info()]\n    await asyncio.gather(*coros)\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(run())\n```\n\n### Specifying Macaroon/Cert files\nBy default the client will attempt to lookup the `readonly.macaron` and `tls.cert` files in the mainnet directory. \nHowever if you want to specify a different macaroon or different path you can pass in the filepath explicitly.\n\n```python\nlnd = LNDClient(macaroon_filepath=\'~/.lnd/invoice.macaroon\', cert_filepath=\'path/to/tls.cert\')\n```\n\n#### Admin macaroon\nUse the admin macaroon to perform write actions (ie. creating invoices, creating new addresses)\n\n```python\nlnd = LNDClient(admin=True)\nlnd.add_invoice(2000)\n```\n\n### Generating Proto Files\n```bash\nvirtualenv lnd\nsource lnd/bin/activate\npip install grpcio grpcio-tools googleapis-common-protos\ngit clone https://github.com/googleapis/googleapis.git\ngit clone https://github.com/lightningnetwork/lnd.git\n# python -m grpc_tools.protoc --proto_path=googleapis:. --python_out=. --grpc_python_out=. rpc.proto\n```\n\n```python\nfrom pathlib import Path\nimport shutil\n\nfor proto in list(Path("lnd/lnrpc").rglob("*.proto")):\n    shutil.copy(proto,Path.cwd())\n\nfor proto in list(Path(".").rglob("*.proto")):\n    sh.python("-m","grpc_tools.protoc","--proto_path=.","--python_out=.","--grpc_python_out=.", str(proto))\n```\n\nLast Step:\nIn File: verrpc_pb2_grpc.py\nChange:\nimport verrpc_pb2 as verrpc__pb2\nTo:\nfrom lndgrpc import verrpc_pb2 as verrpc__pb2\n\n## Deploy to Test-PyPi\n```bash\npoetry build\ntwine check dist/*\ntwine upload --repository-url https://test.pypi.org/legacy/ dist/*\n```',
    'author': 'Kornpow',
    'author_email': 'test@email.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
