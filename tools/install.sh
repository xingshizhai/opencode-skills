#!/bin/bash
#
# Install ocm (OpenCode Manager) to current system
#

set -e

REPO_URL="git@github.com:xingshizhai/opencode-skills.git"
REGISTRY_DIR="${HOME}/.opencode-skills"
BIN_DIR="/usr/local/bin"

echo "🔧 Installing OpenCode Manager (ocm)..."
echo ""

# Check if registry exists
if [ ! -d "${REGISTRY_DIR}/.git" ]; then
    echo "📦 Cloning registry repository..."
    git clone "${REPO_URL}" "${REGISTRY_DIR}"
else
    echo "📦 Registry already exists, updating..."
    cd "${REGISTRY_DIR}"
    git pull
fi

# Install ocm to PATH
if [ -w "${BIN_DIR}" ]; then
    ln -sf "${REGISTRY_DIR}/tools/ocm" "${BIN_DIR}/ocm"
    echo "✅ Installed ocm to ${BIN_DIR}/ocm"
else
    # Try ~/.local/bin
    mkdir -p "${HOME}/.local/bin"
    ln -sf "${REGISTRY_DIR}/tools/ocm" "${HOME}/.local/bin/ocm"
    echo "✅ Installed ocm to ${HOME}/.local/bin/ocm"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":${HOME}/.local/bin:"* ]]; then
        echo ""
        echo "⚠️  Please add the following to your shell profile:"
        echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Quick start:"
echo "  ocm init      # Initialize this system"
echo "  ocm sync      # Sync skills with registry"
echo "  ocm status    # Check status"
echo ""
echo "For more info: ocm help"
