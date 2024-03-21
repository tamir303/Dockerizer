from setuptools import setup, find_packages

setup(
    name='create_python_docker_file',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create_docker_file=create_docker_file:main',
        ],
    },
    description='Generate a Dockerfile based on Python version and dependencies',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/create_docker_file',
    license='MIT',
)
