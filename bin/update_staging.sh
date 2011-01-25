#!/bin/bash

# Update script for staging server. Takes care of updating code repo, vendor
# dir, and running DB migrations.

PROG_NAME=$(basename $0)

REMOTE="origin"
BRANCH="master"

while getopts r:b: OPTION
do
	case ${OPTION} in
		r) REMOTE=${OPTARG};;
		b) BRANCH=${OPTARG};;
		\?) print -u2 "Usage: ${PROG_NAME} [-r remote_repos -b branch]"
		exit 2;;
	esac
done

echo "updating from ..."
echo "REMOTE: ${REMOTE}"
echo "BRANCH: ${BRANCH}"

HERE=`dirname $0`
GIT=`which git`
PYTHON=`which python2.6`

pushd "$HERE/../" > /dev/null

# pull actual code
$GIT pull -q $REMOTE $BRANCH
$GIT submodule update --init

# pull vendor repo
pushd vendor > /dev/null
$GIT pull -q origin master
$GIT submodule update --init
popd > /dev/null

# Run database migrations.
$PYTHON vendor/src/schematic/schematic migrations/

# Minify assets.
$PYTHON manage.py compress_assets

popd > /dev/null
