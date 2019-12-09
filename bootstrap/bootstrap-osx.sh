#!/bin/bash
set -euo pipefail

# This script needs to be standalone to be run like this:
# bash <(curl -fsSL https://raw.githubusercontent.com/rgreinho/bna-tools/master/bootstrap/bootstrap-osx.sh)
# Therefore cannot import other scripts.

# Install brew if needed.
brew --version || /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Update brew.
brew update

# Install brew formulas.
brew install \
  brew-cask-completion \
  bash-completion \
  editorconfig \
  osmosis \
  osmfilter \
  pip-completion \
  python3 \
  shellcheck
