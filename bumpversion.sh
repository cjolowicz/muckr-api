#!/bin/bash

set -eo pipefail

program=$(basename $0)
current_version=$(<VERSION)
force=false
arg=

### functions ##########################################################

usage() {
    echo "usage: $program [options] [major | minor | patch | dev | final]

This script is used to update the version number and add a Git tag to
the repository.

  - Use \`./$program major' to create a major release.
  - Use \`./$program minor' to create a minor release.
  - Use \`./$program patch' to create a patch release.

These will create development snapshots with a .dev0 suffix.

  - Use \`./$program dev' to create another development snapshot.
  - Use \`./$program final' to promote a development snapshot to
    a final release, without the .devN suffix.

Development snapshots must be created on the develop branch. Final
releases must be invoked on the master branch.

Make sure to also push the tag to GitLab:

    git push
    git push --tags

options:
    -h, --help    Display this message.
    -f, --force   Permit {major,minor,patch} from development snapshot."
}

error() {
    echo "error: $*" >&2
    exit 1
}

bad_usage() {
    echo "error: $*" >&2
    echo "Try \`$program --help' for more information." >&2
    exit 1
}

do_major_minor_patch() {
    case $current_version in
	*'.dev'*)
	    if ! $force
	    then
		error "current version is not a final release
Use \`$program $arg --force' to override."
	    fi
	    ;;
    esac

    new_version=$(
	bumpversion --verbose --dry-run $arg 2>&1 |
	    sed -n 's/New version will be .\(.*\).$/\1/p') ||
	error "bumpversion encountered an error
Run \`bumpversion --verbose --dry-run $arg' to investigate."

    bumpversion --current-version $current_version --new-version $new_version.dev0 $arg
}

do_dev() {
    case $current_version in
	*'.dev'*)
	    bumpversion snapshot
	    ;;

	*)
	    error 'current version must be a development snapshot'
	    ;;
    esac
}

do_final() {
    case $current_version in
	*'.dev'*)
	    bumpversion phase
	    ;;

	*)
	    error 'current version is already a final release'
	    ;;
    esac
}

### command line #######################################################

while [ $# -gt 0 ]
do
    option="$1"
    shift

    case $option in
        -h | --help)
            usage
            exit
            ;;

        -f | --force)
            force=true
            ;;

	'major' | 'minor' | 'patch' | 'dev' | 'final')
	    arg=$option
	    ;;

        --)
            break
            ;;

        --* | -?)
            bad_usage "unrecognized option \`$option'"
            ;;

        -*)
            set -- "${option::2}" -"${option:2}" "$@"
            ;;

        *)
            set -- "$option" "$@"
            break
            ;;
    esac
done

if [ $# -gt 0 ]
then
    bad_usage "unrecognized argument \`$1'"
fi

if [ -z "$arg" ]
then
    bad_usage "missing argument"
fi

### main ###############################################################

case $arg in
    'major' | 'minor' | 'patch')
	do_major_minor_patch
	;;

    'dev')
	do_dev
	;;

    'final')
	do_final
	;;
esac

echo $(<VERSION)
