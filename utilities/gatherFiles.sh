#/bin/bash
echo -------------------------------------------------------------------------------
echo Umbra - Files Gathering
echo -------------------------------------------------------------------------------

export PROJECT=$( dirname "${BASH_SOURCE[0]}" )/..

export DOCUMENTATION=$PROJECT/docs/
export RELEASES=$PROJECT/releases/
export REPOSITORY=$RELEASES/repository/
export UTILITIES=$PROJECT/utilities

#! Gathering folder cleanup.
rm -rf $REPOSITORY
mkdir -p $REPOSITORY/Umbra

#! Umbra Changes gathering.
cp -rf $RELEASES/Changes.html $REPOSITORY/Umbra/

#! Umbra Manual / Help files.
cp -rf $DOCUMENTATION/help $REPOSITORY/Umbra/Help
rm $REPOSITORY/Umbra/help/Umbra_Manual.rst

#! Umbra Api files.
cp -rf $DOCUMENTATION/sphinx/build/html $REPOSITORY/Umbra/Api