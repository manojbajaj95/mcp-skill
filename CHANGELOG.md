# Changelog

## [0.3.0](https://github.com/manojbajaj95/mcp-skill/compare/v0.2.0...v0.3.0) (2026-03-11)


### Features

* add project scaffolding, regen script, and refresh generated skills ([3007b60](https://github.com/manojbajaj95/mcp-skill/commit/3007b602fd2a8e6d642c745463e435d79b0d819b))

## [0.2.0](https://github.com/manojbajaj95/mcp-skill/compare/v0.1.0...v0.2.0) (2026-03-11)


### Features

* Add generated skills ([c9c81b9](https://github.com/manojbajaj95/mcp-skill/commit/c9c81b93344c1e45ce152e8a58ef264835f89f8d))
* add persistent disk-backed token storage for all auth types ([531e402](https://github.com/manojbajaj95/mcp-skill/commit/531e40278268fb2997be012ef39e4b3ee0774078))
* **auth:** add ClientCredentialsAuth stub (NotImplementedError placeholder) ([133ebcc](https://github.com/manojbajaj95/mcp-skill/commit/133ebcc50aad4b04d3c60ff5dfe064daca4abc87))
* **auth:** extract auth classes into importable mcp_skill.auth module ([e0d0873](https://github.com/manojbajaj95/mcp-skill/commit/e0d0873d208100b05d40705108e78ecb47b48f0d))
* **cli:** add interactive wizard and non-interactive CLI mode ([2e7e30c](https://github.com/manojbajaj95/mcp-skill/commit/2e7e30c8d38d654368ab23b36dd06249b1c4770e))
* **core:** add introspector, app.py generator, and SKILL.md generator ([5256855](https://github.com/manojbajaj95/mcp-skill/commit/52568551306122451ef5cafcbe63103d22138b1a))
* fix skill output, add deps/usage to SKILL.md, add post-gen validation ([516218b](https://github.com/manojbajaj95/mcp-skill/commit/516218bc74c4153b7b569bf9f7668cd04a9ec86a))
* **scaffold:** initialize mcp-skill project with UV and pyproject.toml ([afcecd9](https://github.com/manojbajaj95/mcp-skill/commit/afcecd9f045a08c17a48bfd3973ac5b2d18a9ff3))
* **templates:** unify __init__ signature to use auth=None across all auth types ([99bd4ef](https://github.com/manojbajaj95/mcp-skill/commit/99bd4ef5ff54cd1c681d3b44a9887ff4eef22058))
* **types:** add JSON Schema to Python type mapper and name sanitizer ([6234fa1](https://github.com/manojbajaj95/mcp-skill/commit/6234fa1781963897c7b4407c923a1eb1b6d5d15f))


### Bug Fixes

* Fix parallel search name ([c5afbf6](https://github.com/manojbajaj95/mcp-skill/commit/c5afbf62d9c51346709c8fd7f87e0945138c35b5))
* **generate:** use per-method client pattern and user-provided app name ([c65bb3e](https://github.com/manojbajaj95/mcp-skill/commit/c65bb3e2412f740706f155b4a243389003ea2f6f))
* **generate:** use result.content for CallToolResult and filter None optional args ([48e4b56](https://github.com/manojbajaj95/mcp-skill/commit/48e4b566e3d2a88e0daaaaa6955c269ce944e764))
* sanitize skill name to valid Python identifier for folder and imports ([afba3b6](https://github.com/manojbajaj95/mcp-skill/commit/afba3b683860c294ec28d7716eab5a553e1ff099))


### Documentation

* rewrite README with before/after, diagram, generated output, and audience section ([e341453](https://github.com/manojbajaj95/mcp-skill/commit/e341453e690ff8fa46422b270a70f8bf271426d8))
