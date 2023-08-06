from distutils.core import setup

setup(
    name='entity-context-crawler',
    version='0.2.1',
    packages=['entity_context_crawler'],
    entry_points={
        'console_scripts': [
            'ecc = entity_context_crawler.__main__:main'
        ]
    }
)
