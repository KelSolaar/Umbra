#/bin/bash
echo -------------------------------------------------------------------------------
echo Umbra - Files Gathering
echo -------------------------------------------------------------------------------

export PROJECT_DIRECTORY=$(cd $( dirname "${BASH_SOURCE[0]}" )/..; pwd)

export DOCUMENTATION_DIRECTORY=$PROJECT_DIRECTORY/docs/
export RELEASES_DIRECTORY=$PROJECT_DIRECTORY/releases/
export REPOSITORY_DIRECTORY=$RELEASES_DIRECTORY/repository/
export UTILITIES_DIRECTORY=$PROJECT_DIRECTORY/utilities

#! Gathering folder cleanup.
rm -rf $REPOSITORY_DIRECTORY
mkdir -p $REPOSITORY_DIRECTORY/Umbra

#! Umbra Changes gathering.
cp -rf $RELEASES_DIRECTORY/Changes.html $REPOSITORY_DIRECTORY/Umbra/

#! Umbra Manual / Help files.
cp -rf $DOCUMENTATION_DIRECTORY/help $REPOSITORY_DIRECTORY/Umbra/Help
rm $REPOSITORY_DIRECTORY/Umbra/help/Umbra_Manual.rst

#! Umbra Api files.
cp -rf $DOCUMENTATION_DIRECTORY/sphinx/build/html $REPOSITORY_DIRECTORY/Umbra/Api