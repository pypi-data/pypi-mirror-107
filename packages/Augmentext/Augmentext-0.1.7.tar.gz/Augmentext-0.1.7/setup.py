from setuptools import setup

with open('PYPI.md') as f:
    long_description = f.read()

setup(
    name='Augmentext',
    packages=['Augmentext'],
    version='0.1.7',
    description='Text augmentation library for NLP with a focus on biomedical applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Marcus D. Bloice',
    author_email='marcus.bloice@medunigraz.at',
    url='https://github.com/mdbloice/Augmentext',  # URL to GitHub repo
    # download_url='https://github.com/mdbloice/Augmentext/tarball/0.1.0',  # Get this using git tag
    keywords=['text', 'augmentation', 'generation', 'NLP', 'machine', 'learning', 'biomedical', 'bioinformatics'],
    include_package_data=True,  # This will include all files in MANIFEST.in in the package when installing.
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'textblob',
        'nltk',
        'pandas'
    ]
    # zip_safe=False # Check this later.
)
