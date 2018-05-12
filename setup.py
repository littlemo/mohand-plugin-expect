from setuptools import setup, find_packages
from mohand_plugin_expect.version import get_setup_version


setup(
    name='mohand-plugin-expect',
    url='https://github.com/littlemo/mohand-plugin-expect',
    author='moear developers',
    author_email='moore@moorehy.com',
    maintainer='littlemo',
    maintainer_email='moore@moorehy.com',
    version=get_setup_version(),
    description='MoHand插件，用以提供可自动控制其他终端应用的任务支持',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='mohand plugin automation',
    packages=find_packages(exclude=('docs', 'tests*')),
    include_package_data=True,
    zip_safe=False,
    license='GPLv3',
    python_requires='>=3',
    project_urls={
        'Documentation': 'http://mohand-plugin-expect.rtfd.io/',
        'Source': 'https://github.com/littlemo/mohand-plugin-expect',
        'Tracker': 'https://github.com/littlemo/mohand-plugin-expect/issues',
    },
    install_requires=open('requirements/pip.txt').read().splitlines(),
    entry_points={
        'mohand.plugin.hand': [
            'expect = mohand_plugin_expect.main:ExpectHand',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Email',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Testing :: Unit',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Terminals',
        'Topic :: Text Editors :: Emacs',
        'Topic :: Utilities',
    ],
)
