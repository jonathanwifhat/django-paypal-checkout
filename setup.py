from setuptools import setup, find_packages

def get_version():
    with open('django_paypal_checkout/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    return '0.0.1'

setup(
    name='django-paypal-checkout',
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django package for PayPal payment integration',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/carrington-dev/django-paypal-checkout',
    author='Carrington Muleya',
    author_email='carrington.muleya@outlook.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'Django>=3.2',
        'requests>=2.25.0',
    ],
)
