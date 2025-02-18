# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Image Search: Enable Linux-related image lookup
- Search Functionality: Add DuckDuckGo search command
- News Lookup: Fetch Linux-related news
- Video Search: Find Linux-related tutorials via ddgs.videos()

## [v0.4.1] - 2025-02-18
### Added
- Added a command -- bsho "<question>" -- that allows for a quick question that does not start a conversation (and by extension is not stored in history).
### Thanks to:
- User GalaxAI for suggesting this to me

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