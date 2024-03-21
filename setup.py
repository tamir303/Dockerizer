from setuptools import setup, find_packages

setup(
    name='pythonDockerizer',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create_docker_file=pythonDockerizer.dockerize:create_docker_file',
        ],
    },
    description='Generate a Dockerfile based on Python version and dependencies',
    author='Tamir Spilberg',
    url='https://github.com/tamir303/Dockerizer',
    license='MIT',
)
