from setuptools import setup, find_packages

version = '1.0.dev0'

setup(name='collective.storedtranslations',
      version=version,
      description="Store translations in the registry",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          ],
      keywords='i18n translations po plone',
      author='Maurits van Rees',
      author_email='maurits@vanrees.org',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
