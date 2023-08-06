from setuptools import setup
import os
from setuptools import find_namespace_packages

setup(
    name="segmentpy",
    version="0.1a",
    description="Deep Learning Software for Tomography Segmentation",
    url="http://segmentpy.readthedocs.org",
    author="Zeliang Su, Arnaud Demortiere",
    author_email="zeliang.su@gmail.com, arnaud.demortiere@u-picardie.fr",
    license="Apache 2.0",
    packages=find_namespace_packages(where='src'),
    package_dir={'': "src"},
    package_data={
        'segmentpy': ['img/*.png'],
        '.': ['LICENSE', 'meta.yaml', 'build.sh', 'conda_build.bat'],
    },
    include_package_data=True,
    install_requires=[
        "numpy==1.19.1",
        "tensorflow==1.14",
        "pandas==1.1.1",
        "Pillow",
        # "openmpi",
        "mpi4py==3.0.3",
        # "PySide2",
        "matplotlib==3.3.1",
        "scikit-learn==0.23.2",
        "scikit-image==0.16.2",
        "scipy==1.5.2",
        "tqdm",
        "opencv-python-headless==3.4.2.*",
        "h5py==2.8.0",
    ],
    keywords=['segmentation', 'CNN', 'XCT-image', 'battery'],
    python_requires="==3.6",
    entry_points={
        'console_scripts': [
            'segmentpy = segmentpy.SegmentPy:main'
        ]

    },
    classfiers=[
        'License :: OSI Approved :: Apache Software License v2.0',
        'Programming Language :: Python :: 3.6',
    ],
)

