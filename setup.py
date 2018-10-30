from setuptools import find_packages, setup


def parse_requirements(filename):
    with open(filename) as f:
        lineiter = (line.strip() for line in f)
        return [
            line.replace(' \\', '').strip()
            for line in lineiter
            if (
                line and
                not line.startswith("#") and
                not line.startswith("-e") and
                not line.startswith("--hash")
            )
        ]


INSTALL_REQUIREMENTS = parse_requirements('deps/requirements.in')

SETUP_REQUIREMENTS = [
    'pytest-runner',
]


setup(
    name='flask_flamegraph',
    url='https://github.com/schireson/flask-flamegraph',
    version='0.0.2',
    packages=find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
    test_suite='tests',
    zip_safe=False,
)
