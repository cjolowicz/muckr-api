#!/bin/bash
# An httpie wrapper taking care of authentication.
# usage: http.sh METHOD URL [options]..

set -euo pipefail

app=muckr-service

method=$1
shift

url=$1
shift

# Read the app config.
case $url in
    *'heroku'*)
	eval $(heroku config --shell --app=$app)
	;;

    *)
	source .env
	;;
esac

: ${ADMIN_USERNAME:=admin}

# Match up to first slash, not counting any `://`
base_url=$(grep -Eo '^([^:]*://)?[^/]+' <<< "$url")

# Get an authentication token, using basic auth.
# The sed expression works like `jq -r .token`.
token=$(
    http POST $base_url/tokens \
	 --auth $ADMIN_USERNAME:$ADMIN_PASSWORD \
	 --print=b |
	sed -n 's/^.*"token": *"\([^"]\+\)".*$/\1/p')

# Perform the actual request using token auth.
exec http "$@" $method "$url" "Authorization: Bearer $token"
