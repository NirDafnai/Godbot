from setuptools import setup

setup(
    name='generate_command',
    version='0.1',
    py_modules=['generate_command'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        generate_command=scripts.generate_command:create_command
    ''',
)
