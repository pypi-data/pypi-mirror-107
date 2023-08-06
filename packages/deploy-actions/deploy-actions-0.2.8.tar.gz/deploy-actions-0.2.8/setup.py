from setuptools import setup, find_packages

from app import __version__
from app import __doc__ as long_desc

setup(
    name='deploy-actions',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/desty2k/deploy-actions',
    license='MIT',
    author='Wojciech desty2k Wentland',
    author_email='wojciech.wentland@int.pl',
    description='Deployable app',
    long_description=long_desc,
    long_description_content_type='text/x-rst',

    python_requires='>=3.5',
    zip_safe=False,

    project_urls={
        'Issues': 'https://github.com/desty2k/deploy-actions/issues',
        'Docs': 'https://desty2k.github.io/deploy-actions/',
    }
)
