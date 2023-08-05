from setuptools import setup, find_packages

setup_args = dict(
    name='classmanagement',
    version='0.0.3',
    description='Class Management by Nguyễn Chí Thanh',
    license='MIT',
    packages=find_packages(),
    author='Chi Thanh Nguyen',
    author_email='tenchithanh@gmail.com',
    keywords=['Class_Management', 'ClassManagement', 'CManagement'],
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)