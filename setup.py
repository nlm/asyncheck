from setuptools import setup,find_packages

setup(
    name = "asyncheck",
    version = "0.1",
    packages = find_packages(),
    author = "Nicolas Limage",
    description = "asynchroneously store and retrieve nagios alerts",
    license = "GPL",
    keywords = "nagios redis",
    entry_points = {
        'console_scripts': [
            'asyncheck=asyncheck.main:check',
            'asynpush=asyncheck.main:push',
            'asyndel=asyncheck.main:delete',
        ],
    },
    install_requires=[
        'redis>=2.10',
        'nagplug>=1.0',
    ],
)
