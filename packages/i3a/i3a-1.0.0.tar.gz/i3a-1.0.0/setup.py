from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f_:
    long_description = f_.read()

def main():
    setup(name='i3a',
          description="i3 automatic manager",
          long_description=long_description,
          long_description_content_type='text/markdown',
          use_scm_version={'write_to': 'src/i3a/_version.py'},
          license='GPLv3+',
          author='Michał Góral',
          author_email='dev@goral.net.pl',
          url='https://gitlab.com/mgoral/i3a',
          platforms=['linux'],
          python_requires='>=3.7,<3.10',
          setup_requires=['setuptools_scm'],
          install_requires=[
              'i3ipc==2.2.1',
          ],

          # https://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=['Development Status :: 4 - Beta',
                       'Environment :: Console',
                       'Intended Audience :: End Users/Desktop',
                       'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                       'Natural Language :: English',
                       'Operating System :: POSIX',
                       'Programming Language :: Python :: 3 :: Only',
                       'Programming Language :: Python :: 3.7',
                       'Topic :: Utilities',
                       ],

          packages=find_packages('src'),
          package_dir={'': 'src'},

          entry_points={
              'console_scripts': ['i3a=i3a.app:main'],
          },
          scripts=['contrib/i3a-swap', 'contrib/i3a-move-to-empty'])

if __name__ == '__main__':
    main()

