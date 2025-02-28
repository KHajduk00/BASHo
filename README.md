# BASHō - Your Linux Terminal Assistant

BASHō is a super-lightweight and efficient terminal assistant designed to help users navigate and utilize Linux efficiently. Inspired by both the Bash shell and the haiku poet Matsuo Bashō, this tool provides concise, relevant Linux command-line assistance using multiple llm models (Claude 3 Haiku recommended) via DuckDuckGo Search.

## WARNING!

By using this app, you acknowledge that you will not use it in a way that infringes on DuckDuckGo's terms. The official DuckDuckGo website can be found at https://duckduckgo.com.

## Features
- **Minimalist Responses**: Provides short and to-the-point Linux-related answers.
- **Context-Aware Assistance**: Answers only Linux-related queries and avoids unnecessary details.
- **Easy Installation**: Simple setup with a provided install script.
- **Seamless Execution**: Runs directly from the terminal using the `ask-basho` or `bsho "<question>"` command.

## Installation
To install BASHō, run the following commands:

```bash
git clone https://github.com/your-repo/basho.git  
cd BASHo
```
After pulling the project and cd'ing into the repo folder:

```bash
chmod +x install.sh
./install.sh
```

Once the installation is complete, restart your terminal or run:

```bash
source ~/.bashrc
```

Now, you can use BASHō by simply typing:

```bash
ask-basho
```

Or:

```bash
bsho "<your question here>"
```

## Usage
1. Start the assistant by running:
   ```bash
   ask-basho
   ```
2. Type your Linux-related question and press Enter.
3. To exit, type `exit`.

Or:

1. Give quick question to the assistant by running:
   ```bash
   bsho "<question>"
   ```
2. Wait a second or two to receive the answer.

### Example of all flags/commands:
```
$ ask-basho
Welcome to BASHō - Your Linux Terminal Assistant! Type 'exit' to quit.
You: How do I list all files in a directory?
BASHō: Use `ls -a` to list all files, including hidden ones.
```

```
$ bsho "how to create a folder?"
BASHō: To create a folder in the Linux terminal, use the `mkdir` command followed by the name of the new folder.
```

```
$ bsho -v "how to create groups in linux?"

Top 3 Video Results:
==================================================

[Video 1]
Title: How to Create Groups in Linux
Duration: 5:32
URL: https://www.youtube.com/watch?v=example1
Views: 25000

[Video 2]

(...)
```

```
$ bsho -t "archinstall guide"

Top 5 Text Results:
==================================================

[Result 1]
Title: Installation guide - ArchWiki
URL: https://wiki.archlinux.org/title/Installation_guide
Content: This document is a guide for installing Arch Linux using the live system booted from an installation medium made from an official installation image. The installation medium provides accessibility features which are described on the page Install Arch Linux with accessibility options.For alternative means of installation, see Category:Installation process.

[Result 2]

(...)
```

```
$ bsho -n "tech industry update"

Top 3 News Results:  
==================================================  

[News 1]  
Title: Tech leader supports adoption of new coding language, calls its rise inevitable  
Date: 2025-02-21T17:06:00+00:00  
Content: Among the issues raised about the new policy post, an industry expert corrected the assertion that some system maintainers might decide they simply don't want the new language, and that that's to be expected and accepted.  
URL: https://www.example.com/news/coding_language_adoption  
Source: techsource  

[News 2]

(...)
```

```
$ bsho -c<number>
$ bsho -c3
```
 (aviable numbers are 5-1, where 5 is newest conversation and 1 is the oldest one)

## Dependencies
- Python 3
- `duckduckgo-search` Python package

## Uninstallation
To remove BASHō from your system:
```bash
rm -rf ~/.local/bin/ask-basho
rm -rf .venv
```

## Notes
- The tool uses: gpt-4o-mini, llama-3.3-70b, claude-3-haiku, o3-mini, mixtral-8x7b models via DuckDuckGo Search.
- Responses are optimized for Linux command-line usage.
- If you encounter issues, ensure your Python environment and dependencies are correctly installed.
- IT REQUIRES INTERNET ACCESS

## 📌 BASHō Roadmap

### ✅ Current Features:

    AI-powered Linux assistant using multiple models via DuckDuckGo Search.
    Simple terminal-based interaction.
    Answers are concise and Linux-focused.
    Uses duckduckgo_search API for responses.
    Session History: Store recent queries and responses to go back to them, to load the conversation use '-c<number>' flag.
    Quick question feature: use bsho followed by "<question>" to ask BASHō a quick question and receive quick answer.
    Video Search: Find videos using 'bsho' command followed by '-v' flag.
    Search Functionality: Find information using 'bsho' command followed by '-t' flag.
    News search Functionality: Find news articles using 'bsho' command followed by '-n' flag.

## Current Version:

- v0.9.1 (check CHANGELOG.md or commits to keep track with changes).

## License
BASHō is open-source and licensed under the MIT License.

---

Enjoy your Linux journey with BASHō! 🐧

