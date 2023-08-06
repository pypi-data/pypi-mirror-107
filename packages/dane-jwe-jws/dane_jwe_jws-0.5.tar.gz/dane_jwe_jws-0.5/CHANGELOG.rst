Changelog
=========


v0.5
----

Fix
~~~
- Fix issue where only PKIX-CD certs were retrieved for authentication.
  [Ash Wilson]

  Close #9


v0.4 (2021-05-28)
-----------------

Changes
~~~~~~~
- Improve flexibility of Utility.get_pubkey_from_dns(). [Ash Wilson]

  Unspecified ``dane_type`` argument for Util.get_pubkey_from_dns()
  will cause the first entity certificate of any type to be returned.

  Close #7


v0.3 (2021-05-19)
-----------------

Changes
~~~~~~~
- Update CHANGELOG.rst. [Ash Wilson]
- Add strict mode support. [Ash Wilson]

  Closes #1

Other
~~~~~
- Build(deps): bump dane-discovery from 0.6 to 0.11. [dependabot[bot]]

  Bumps [dane-discovery](https://github.com/valimail/dane_discovery) from 0.6 to 0.11.
  - [Release notes](https://github.com/valimail/dane_discovery/releases)
  - [Commits](https://github.com/valimail/dane_discovery/commits)
- Build(deps): update pytest requirement from ~=6.0 to ~=6.2.
  [dependabot[bot]]

  Updates the requirements on [pytest](https://github.com/pytest-dev/pytest) to permit the latest version.
  - [Release notes](https://github.com/pytest-dev/pytest/releases)
  - [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest/compare/6.0.0...6.2.4)
- Build(deps): update pytest-cov requirement from ~=2.10 to ~=2.12.
  [dependabot[bot]]

  Updates the requirements on [pytest-cov](https://github.com/pytest-dev/pytest-cov) to permit the latest version.
  - [Release notes](https://github.com/pytest-dev/pytest-cov/releases)
  - [Changelog](https://github.com/pytest-dev/pytest-cov/blob/master/CHANGELOG.rst)
  - [Commits](https://github.com/pytest-dev/pytest-cov/compare/v2.10.0...v2.12.0)
- Build(deps): update sphinx requirement from ~=3.1 to ~=4.0.
  [dependabot[bot]]

  Updates the requirements on [sphinx](https://github.com/sphinx-doc/sphinx) to permit the latest version.
  - [Release notes](https://github.com/sphinx-doc/sphinx/releases)
  - [Changelog](https://github.com/sphinx-doc/sphinx/blob/4.x/CHANGES)
  - [Commits](https://github.com/sphinx-doc/sphinx/compare/v3.1.0...v4.0.1)


v0.2 (2020-09-14)
-----------------

Fix
~~~
- Correct parsing of DNS URI for message verification. [Ash Wilson]


v0.1 (2020-08-05)
-----------------

New
~~~
- Initial commit. [Ash Wilson]


