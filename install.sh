#!/bin/bash

# Get the absolute path of the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create virtual environment if it doesn't exist
python3 -m venv "$SCRIPT_DIR/.venv"

# Activate virtual environment and install requirements
source "$SCRIPT_DIR/.venv/bin/activate"
pip install duckduckgo-search

# Create the executable script for conversation mode
cat > "$SCRIPT_DIR/ask-basho" << EOF
#!/bin/bash
source "$SCRIPT_DIR/.venv/bin/activate"
python3 "$SCRIPT_DIR/basho.py" "\$@"
EOF

# Create the quick question script
cat > "$SCRIPT_DIR/bsho" << EOF
#!/bin/bash
source "$SCRIPT_DIR/.venv/bin/activate"
python3 "$SCRIPT_DIR/quick_basho.py" "\$@"
EOF

# Make all scripts executable
chmod +x "$SCRIPT_DIR/ask-basho"
chmod +x "$SCRIPT_DIR/bsho"
chmod +x "$SCRIPT_DIR/basho.py"
chmod +x "$SCRIPT_DIR/quick_basho.py"

# Create the bin directory if it doesn't exist
mkdir -p "$HOME/.local/bin"

# Create symbolic links
ln -sf "$SCRIPT_DIR/ask-basho" "$HOME/.local/bin/ask-basho"
ln -sf "$SCRIPT_DIR/bsho" "$HOME/.local/bin/bsho"

# Add ~/.local/bin to PATH if it's not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo "Installation complete! Please restart your terminal or run: source ~/.bashrc"
echo "Then you can use 'ask-basho' for conversation mode or 'bsho \"question\"' for quick answers!"