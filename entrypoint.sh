#!/bin/sh

chown -R 0:0 /var/fasset/secrets.bot.json
chown -R 0:0 /var/fasset/secrets.user.json

case $1 in
    run) python -u -m run;;
    *)
    # The wrong first argument.
    echo "invalid argument: '$1'"
    echo $USAGE_MSG
    exit 1
esac