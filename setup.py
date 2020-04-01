import setuptools

with open('requirements.txt') as require:
    REQUIRE = require.read().splitlines()

with open('README.rst') as readme:
    README = readme.read()

setuptools.setup(
    name = 'WTRobot',
    version = 2.0.1,
    description = 'WTRobot-v2 web testing framework',
    long_description = README,
    url = 'https://github.com/wtrobot/wtrobot-v2',
    author = 'Vishal Vijayraghavan',
    author_email = 'vishalvvr@fedoraproject.org',
    license = 'MIT',
    install_requires = REQUIRE,
    python_requires=">=3.6",
    zip_safe=False,
    classifiers = [
 	'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
