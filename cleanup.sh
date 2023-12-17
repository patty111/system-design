#!/bin/bash

autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive . --exclude=__init__.py

# listing all TODO comments
grep --color=always -rn --exclude-dir=env --exclude-dir=env-wsl --exclude=cleanup.sh "TODO" .