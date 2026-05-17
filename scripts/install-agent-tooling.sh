#!/usr/bin/env bash
set -euo pipefail

# Install APM, Claude Code and common agent libraries on Ubuntu/macOS.
# Usage:
#   ./scripts/install-agent-tooling.sh
#   INSTALL_CLAUDE_CODE=0 ./scripts/install-agent-tooling.sh

OS="$(uname -s)"
INSTALL_CLAUDE_CODE="${INSTALL_CLAUDE_CODE:-1}"
INSTALL_APM="${INSTALL_APM:-1}"
INSTALL_NODE_LIBS="${INSTALL_NODE_LIBS:-1}"

need_cmd() {
  command -v "$1" >/dev/null 2>&1
}

install_homebrew() {
  if need_cmd brew; then
    return
  fi
  echo "[INFO] Homebrew をインストールします..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /home/linuxbrew/.linuxbrew/bin/brew ]]; then
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
  fi
}

install_node_if_missing() {
  if need_cmd node && need_cmd npm; then
    return
  fi

  case "$OS" in
    Darwin)
      install_homebrew
      brew install node
      ;;
    Linux)
      if need_cmd apt-get; then
        sudo apt-get update
        sudo apt-get install -y ca-certificates curl gnupg
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
        echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list >/dev/null
        sudo apt-get update
        sudo apt-get install -y nodejs
      else
        echo "[ERROR] Linux ですが apt-get が見つかりません。Node.js を手動で導入してください。" >&2
        exit 1
      fi
      ;;
    *)
      echo "[ERROR] 未対応 OS: $OS" >&2
      exit 1
      ;;
  esac
}

install_global_npm_package() {
  local package="$1"
  if npm list -g --depth=0 "$package" >/dev/null 2>&1; then
    echo "[INFO] $package は既に導入済みです。"
  else
    echo "[INFO] $package を導入します。"
    npm install -g "$package"
  fi
}

main() {
  install_node_if_missing

  if [[ "$INSTALL_APM" == "1" ]]; then
    install_global_npm_package "@anthropic-ai/apm"
  fi

  if [[ "$INSTALL_CLAUDE_CODE" == "1" ]]; then
    install_global_npm_package "@anthropic-ai/claude-code"
  fi

  if [[ "$INSTALL_NODE_LIBS" == "1" ]]; then
    install_global_npm_package "pnpm"
    install_global_npm_package "typescript"
    install_global_npm_package "tsx"
  fi

  echo "[OK] セットアップ完了"
  echo " - node: $(node --version)"
  echo " - npm:  $(npm --version)"
  if need_cmd apm; then
    echo " - apm:  $(apm --version || true)"
  fi
  if need_cmd claude; then
    echo " - claude: $(claude --version || true)"
  fi
}

main "$@"
