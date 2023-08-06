from codecs import open
import os

from setuptools import setup, find_packages
from setuptools import dist  # Install numpy right now
dist.Distribution().fetch_build_eggs(['numpy>=1.15.4'])

try:
    import numpy as np
except ImportError:
    exit('Please install numpy>=1.15.4 first.')

__version__ = "0.6.6.2"

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from README.md
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs]

setup(
    name='LibRecommender-limited',
    author='massquantity',
    author_email='jinxin_madie@163.com',
    description=(
        'A collaborative-filtering and content-based recommender system '
        'for both explicit and implicit datasets.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=__version__,
    url='https://github.com/massquantity/LibRecommender',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords=['Matrix Factorization', 'Collaborative Filtering',
              'Content-Based', 'Recommender System',
              'Deep Learning', 'Data Mining'],

    packages=find_packages(exclude=['test*', 'examples']),
    include_package_data=True,
    install_requires=install_requires,
)
