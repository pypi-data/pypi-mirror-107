#!/bin/bash
set -e
echo "::group::Install Rust"
which rustup > /dev/null || curl --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable
export PATH="$HOME/.cargo/bin:$PATH"
rustup override set stable
echo "::endgroup::"
export PATH="$PATH:/opt/python/cp36-cp36m/bin:/opt/python/cp37-cp37m/bin:/opt/python/cp38-cp38/bin:/opt/python/cp39-cp39/bin"
echo "::group::Install maturin"
curl -L https://github.com/PyO3/maturin/releases/download/v0.10.6/maturin-x86_64-unknown-linux-musl.tar.gz | tar -xz -C /usr/local/bin
maturin --version
echo "::endgroup::"
maturin build -i python3.8 --release --strip