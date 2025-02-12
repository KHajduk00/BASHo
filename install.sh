#!/bin/bash

# Get the absolute path of the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create virtual environment if it doesn't exist
python3 -m venv "$SCRIPT_DIR/.venv"

# Activate virtual environment and install requirements
source "$SCRIPT_DIR/.venv/bin/activate"
pip install duckduckgo-search

# Create the executable script
cat > "$SCRIPT_DIR/ask-basho" << EOF
#!/bin/bash
source "$SCRIPT_DIR/.venv/bin/activate"
python3 "$SCRIPT_DIR/basho.py" "\$@"
EOF

# Make scripts executable
chmod +x "$SCRIPT_DIR/ask-basho"
chmod +x "$SCRIPT_DIR/basho.py"

# Create the bin directory if it doesn't exist
mkdir -p "$HOME/.local/bin"

# Create symbolic link
ln -sf "$SCRIPT_DIR/ask-basho" "$HOME/.local/bin/ask-basho"

# Add ~/.local/bin to PATH if it's not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo "Installation complete! Please restart your terminal or run: source ~/.bashrc"
echo "Then you can use 'ask-basho' command from anywhere!"