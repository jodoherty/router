#!/bin/sh

if command -v gopass >/dev/null 2>&1; then
    gopass cat home/ansible/router/become
else
    pass show ansible/router/become
fi
