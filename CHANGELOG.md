# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Image Search: Enable Linux-related image lookup
- Search Functionality: Add DuckDuckGo search command
- News Lookup: Fetch Linux-related news

## [v0.6.1] - 2025-02-21
### Added
- Added a '-v' flag to the 'bsho' command, now when typing 'bsho -v "How to install NixOS"' user will receive top three results related to the passed query.
### Misc
- Changed versioning to better represent what is going on.

## [v0.5.1] - 2025-02-20
### Added
- Added docstrings and typing for better code readability (even though its a microscopic project)

## [v0.5.0] - 2025-02-18
### Added
- Added a command -- bsho "<question>" -- that allows for a quick question that does not start a conversation (and by extension is not stored in history).
### Thanks to
- User [GalaxAI](https://github.com/GalaxAI) for suggesting this to me

## [v0.4.0] - 2025-02-18
### Added
- Session History Loading: Now you are able to load in one previous conversation back into the llm! (might blow up if conversation is really long, haven't tested yet)

## [v0.3.0] - 2025-02-17
### Added
- Session History Storing: Store recent queries and responses (feeding back into BASHō to be added)

## [v0.2.0] - 2025-02-13
### Added
- Model Selection: (e.g., gpt-4o-mini, mixtral-8x7b), all models are listed during first run after installation 

## [v0.1.0] - 2025-02-12
### Added
- Initial implementation of BASHō
- Basic command-line interaction