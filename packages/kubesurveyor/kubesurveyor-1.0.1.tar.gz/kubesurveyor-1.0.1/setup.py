# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kubesurveyor']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'graphviz>=0.16,<0.17', 'kubernetes>=12.0.1,<13.0.0']

entry_points = \
{'console_scripts': ['kubesurveyor = kubesurveyor.main:parse_args']}

setup_kwargs = {
    'name': 'kubesurveyor',
    'version': '1.0.1',
    'description': 'Good enough Kubernetes namespace visualization tool',
    'long_description': "# Kubesurveyor  \n\nGood enough Kubernetes namespace visualization tool.  \nNo provisioning to a cluster required, only Kubernetes API is scrapped.  \n\n<img src='https://github.com/viralpoetry/kubesurveyor/raw/main/kubesurveyor.jpg'/>\n\n## Installation    \n```\nsudo apt-get install graphviz\npip install kubesurveyor\n```\n\n## Usage\n\nExport path to a custom certification authority, if you use one for your Kubernetes cluster API\n```\nexport REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt\n```\n\nAlternatively, ignore K8S API certificate errors using `--insecure` or `-k`\n```\nkubesurveyor <namespace> --insecure\n```\n\nShow `<namespace>` namespace as a `dot` language graph, using currently active K8S config context  \n```\nkubesurveyor <namespace>\n```\n\nSpecify context to be used, if there are multiple in the K8S config file  \n```\nkubesurveyor <namespace> --context <context>\n```\n\nDump crawled namespace data to a `YAML` format for later processing\n```\nkubesurveyor <namespace> --context <context> --save > namespace.yaml\n```\n\nLoad from `YAML` file, show as `dot` language graph\n```\ncat namespace.yaml | kubesurveyor <namespace> --load\n```\n\nLoad from `YAML` file and render as `png` visualization to a current working directory\n```\ncat namespace.yaml | kubesurveyor <namespace> --load --out png\n```\n\nIf you want to generate architecture image from `dot` definition by hand, use `dot` directly\n```\ndot -Tpng k8s.dot > k8s.png\n```\n\nLimitations:  \n - unconnected pods, services are not shown  \n - could have problems with deployments created by Tiller  \n - number of replicas is not tracked  \n",
    'author': 'Peter Gasper',
    'author_email': 'peter@gasper.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/viralpoetry/kubesurveyor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
