# Third-Party Notices

This repository is distributed under the MIT License in [LICENSE.txt](LICENSE.txt).
Copyright in repository-owned material is retained by the authors named in
`LICENSE.txt`: Zildjian E. California and Rey Marvin C. Rizal.

The MIT license applies to repository-owned material unless a specific file,
component, or notice states otherwise. When a third-party component, asset, or
notice applies, the applicable third-party terms govern that specific material.

## Documentation Adaptations

- The root `README.md` structure is adapted from the public
  Best-README-Template project. The resulting project-specific README content is
  maintained as part of this repository.
- `CODE_OF_CONDUCT.md` and `SECURITY.md` adapt principles from publicly
  available University of the Philippines policy and philosophy documents for
  this independent repository. The adaptation does not imply UP sponsorship,
  endorsement, or adoption.

## Development and Test Tooling

The runtime source under `sssp-modern/src/sssp/` is intended to use only the
Python standard library and local package modules. Test and validation workflows
may use external tools such as `pytest`, `coverage.py`, and optional NetworkX
oracle checks. These tools are not vendored in this repository.
