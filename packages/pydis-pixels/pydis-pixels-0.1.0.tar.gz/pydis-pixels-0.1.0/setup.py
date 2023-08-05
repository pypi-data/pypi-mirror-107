import setuptools

with open('README.md') as file:
    long_description = file.read()

setuptools.setup(
    name='pydis-pixels',
    version='0.1.0',
    author='Ben Soyka',
    author_email='bensoyka@icloud.com',
    description='Wrapper for the Python Discord Pixels API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bsoyka/pydis-pixels',
    packages=setuptools.find_packages(),
    python_requires='>=3.7.*',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    project_urls={
        'Source': 'https://github.com/bsoyka/pydis-pixels',
        'Changelog': 'https://github.com/bsoyka/pydis-pixels/releases',
    },
)
