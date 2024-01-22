#!/bin/bash

# List of packages to uninstall
packages=("PySide6" "PySide6-tools" "PySide6-examples")

# Uninstall each package
for package in "${packages[@]}"
do
    pip uninstall "$package"
done
