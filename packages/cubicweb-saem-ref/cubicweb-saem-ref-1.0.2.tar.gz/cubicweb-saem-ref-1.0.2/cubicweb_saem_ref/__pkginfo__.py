# coding: utf-8
# pylint: disable=W0622
"""cubicweb-saem-ref application packaging information"""

distname = 'cubicweb-saem-ref'
modname = 'cubicweb_saem_ref'

numversion = (1, 0, 2)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = "Référenciel de Système d'Archivage Électronique Mutualisé"
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb[pyramid]': '>= 3.26.1, < 3.27',
    'cubicweb-squareui': ">=1.1.0,<1.2.0",
    'cubicweb-eac': '>= 0.8.4, < 0.9.0',
    'cubicweb-seda': ">=0.17.0,<0.18.0",
    'cubicweb-compound': '>= 0.7.0, < 0.8.0',
    'cubicweb-prov': '>= 0.4.0, < 0.5.0',
    'cubicweb-oaipmh': '>= 0.6.0, < 0.7.0',
    'cubicweb-relationwidget': '>= 0.5.1, < 0.6.0',
    'cubicweb-skos': ">=1.6.0,<1.7.0",
    'cubicweb-vtimeline': ">=0.6.0,<0.7.0",
    'cubicweb-signedrequest': ">=1.0.0,<1.1.0",
    'isodate': ">=0.6.0,<0.7.0",
    'python-dateutil': ">=2.8.0,<2.9.0",
    'pytz': ">=2021.1.0,<2021.2.0",
    'psycopg2-binary': None,
    'rdflib': ">=5.0.0,<5.1.0",
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python :: 3',
    'Programming Language :: JavaScript',
]
