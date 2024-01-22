#!/bin/bash

# List of packages to uninstall
packages=("PySide6" "shiboken6" "PySide6-Essentials" "PySide6-Addons")

# Uninstall each package
for package in "${packages[@]}"
do
    pip uninstall "$package"
done
