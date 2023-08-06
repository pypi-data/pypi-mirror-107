# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['worstcase']

package_data = \
{'': ['*']}

install_requires = \
['Pint>=0.17,<0.18',
 'networkx>=2.5.1,<3.0.0',
 'pyDOE>=0.3.8,<0.4.0',
 'treelib>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'worstcase',
    'version': '0.2.1',
    'description': 'Worst case analysis and sensitivity studies using Extreme Value and/or Monte Carlo methods.',
    'long_description': '# worstcase\n\n## Overview\n\n`pip install worstcase`\n\nWorst case analysis and sensitivity studies using Extreme Value and/or Monte Carlo methods.\n\nThis package coexists alongside far more capable uncertainty analysis and error propagation packages such as [uncertainties](https://pypi.org/project/uncertainties/) (first-order propagation), [soerp](https://pypi.org/project/soerp/) (second-order propagation), and [mcerp](https://pypi.org/project/mcerp/) (Monte Carlo propagation).\n\nThis package is designed for engineering applications where worst case analysis computations are often done using the Extreme Value method over single-valued functions while falling back to the Monte Carlo method when the worst case is known to not exist at the extremes. The Extreme Value method is implemented as a brute-force search; the Monte Carlo method is implemented with Latin Hypercube Sampling over a uniform distribution.\n\nThis package does not transparently handle parameter covariance across functions. Instead, the graph of parameter dependence must be a tree (and therefore acyclic). Constructing a worst case analysis requires explicit definition of what the underlying parameter dependencies are.\n\n## Usage\n\n```python\nimport worstcase as wca\nimport numpy as np\n\nwca.config.n = 2000  # Number of Monte Carlo runs. (default: 5000)\nwca.config.sigfig = 4  # Number of significant firues to print. (default: 3)\n```\n\nThe primitive varying parameter is a *Param*. *Params* are constructed either by tolerance (absolute or relative) or by range. *Params* may be given units from the default unit registry of [Pint](https://pint.readthedocs.io/en/stable/) (default is unitless). A tag for printing is also optional (default is an empty string). A *Param* has the fields *nom* (nominal value), *lb* (lower bound), and *ub* (upper bound).\n\n```python\nspd_initial = wca.param.bytol(nom=2, tol=0.1, rel=True, unit=wca.unit("m/s"), tag="v0")\naccel = wca.param.byrange(nom=0.2, lb=0.1, ub=0.5, unit=wca.unit("m/s**2"), tag="a")\ndistance = wca.param.byrange(nom=1, lb=0.8, ub=1.1, unit=wca.unit.km, tag="x")\n\nprint([spd_initial, accel, distance])\n```\n```\n[v0: 2 m/s (nom), 1.8 m/s (lb), 2.2 m/s (ub),\n a: 200 mm/s² (nom), 100 mm/s² (lb), 500 mm/s² (ub),\n x: 1 km (nom), 800 m (lb), 1.1 km (ub)]\n```\n\nA more complex parameter is built up as a *ParamBuilder*. *ParamBuilders* are constructed by decorating single-valued functions by *ev* (Extreme Value) or *mc* (Monte Carlo). The arguments passed to the *ParamBuilder* are partially bound to the underlying function. A parameter dependency tree can be drawn using the assigned tags; *ParamBuilder* will assume a tag corresponding to the function name as a default.\n\n```python\n@wca.param.ev(spd_initial, accel, distance)\ndef spd_final(v, a, x):\n    return np.sqrt(v ** 2 + 2 * a * x)\n\n\nprint(spd_final)\n```\n```\nspd_final (ev)\n├── a\n├── v0\n└── x\n```\n\n*ParamBuilder* is a callable and the returned value depends on the arguments supplied. If no arguments are supplied, the parameter is built and a *Param* is returned.\n\n```python\nprint(spd_final())\n```\n```\nspd_final: 20.1 m/s (nom), 12.78 m/s (lb), 33.24 m/s (ub)\n```\n\nAlternatively, the *ParamBuilder* binding to the underlying function can be updated and a new *ParamBuilder* is returned.\n\n```python\nspd_final_noaccel = spd_final(a=0 * wca.unit("m/s**2"), tag="spd_noaccel")\nprint(spd_final_noaccel)\n```\n```\nspd_noaccel (ev)\n├── v0\n└── x\n```\n\nFinally, if the *ParamBuilder* binding is updated such that no arguments are varying parameters then the underlying function will be called to return a single value.\n\n```python\nresult = spd_final_noaccel(3 * wca.unit("m/s"), x=10 * wca.unit.m)\nprint(result)\n```\n```\n3.0 meter / second\n```\n\n*ParamBuilders* can be used to construct other *ParamBuilders*.\n\n```python\nspd_rel = wca.param.bytol(nom=20, tol=1, rel=False, unit=wca.unit("mi/hr"), tag="vrel")\n\n\n@wca.param.mc(spd_final, spd_rel)\ndef spd_total(vf, vr):\n    return vf + vr\n\n\nprint(spd_total)\nprint(spd_total())\n```\n```\nspd_total (mc)\n├── spd_final (ev)\n│   ├── a\n│   ├── v0\n│   └── x\n└── vrel\n\nspd_total: 29.04 m/s (nom), 21.36 m/s (lb), 42.52 m/s (ub)\n```\n\n*ParamBuilders* can be modified with the *ss* method to perform a sensitivity study. By supplying a *Param* or *ParamBuilder* (or a list of them), a new *ParamBuilder* is returned where all other varying parameters are set to their nominal value. A few examples below.\n\n```python\naccel_sens = spd_total.ss(accel, tag="accel-sens")\nprint(accel_sens)\nprint(accel_sens())\n```\n```\naccel-sens (mc)\n└── spd_final (ev)\n    └── a\n\naccel-sens: 29.04 m/s (nom), 23.23 m/s (lb), 40.62 m/s (ub)\n```\n\n```python\naccel_distance_sens = spd_total.ss([accel, distance], tag="accel/distance-sens")\nprint(accel_distance_sens)\nprint(accel_distance_sens())\n```\n```\naccel/distance-sens (mc)\n└── spd_final (ev)\n    ├── a\n    └── x\n\naccel/distance-sens: 29.04 m/s (nom), 21.75 m/s (lb), 42.16 m/s (ub)\n```\n\n```python\nfinalspd_sens = spd_total.ss(spd_final, tag="finalspd-sens")\nprint(finalspd_sens)\nprint(finalspd_sens())\n```\n```\nfinalspd-sens (mc)\n└── spd_final (ev)\n    ├── a\n    ├── v0\n    └── x\n\nfinalspd-sens: 29.04 m/s (nom), 21.73 m/s (lb), 42.18 m/s (ub)\n```\n\n```python\nrelspd_sens = spd_total.ss(spd_rel, tag="relspd-sens")\nprint(relspd_sens)\nprint(relspd_sens())\n```\n```\n\nrelspd-sens (mc)\n└── vrel\n\nrelspd-sens: 29.04 m/s (nom), 28.59 m/s (lb), 29.49 m/s (ub)\n```',
    'author': 'amosborne',
    'author_email': 'amosborne@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amosborne/worstcase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
