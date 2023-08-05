import setuptools

setuptools.setup(
    name="nt-test",  # Replace with your own username
    version="0.0.2",
    author="newstower",
    author_email="kj2945@gmail.com",
    description="newstower",
    # long_description='',
    # long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    # packages={'nt-crawler'},
    # package_dir={'': 'nt-crawler/src'},
    packages=setuptools.find_packages(),
    # scripts=['nt.py'],
    entry_points={
        'console_scripts': ['nt-run=nt_crawler.src.nt:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
