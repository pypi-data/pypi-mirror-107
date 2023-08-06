from setuptools import find_packages
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='paga-collect',
    version='1.0.1',
    license='MIT',
    description='A helper class/SDK to enable developers easily integrate Paga Collect API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Zubair Abubakar',
    author_email='zubair@zubairabubakar.co',
    url='https://github.com/Paga-Developer-Community/paga-collect-python-lib',
    packages=["paga-collect"],
    py_modules=["paga-collect"],
    python_requires='>=3.6',
    include_package_data=True,
    keywords=['payment api', 'paga', 'paga collect api'],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
