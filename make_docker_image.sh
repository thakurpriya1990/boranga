#!/bin/bash
## sole parameter is an integer indicating incremental daily version
## git branch --set-upstream-to=origin/das_dev das_dev



if [ $# -lt 1 ]; then
echo "ERROR: Must specify <github branch> and <integer indicating incremental daily version> e.g."
echo "$0 das_dev <optional: --no-cache>"
exit 1
fi



if [ $# -eq 2 ]; then
NO_CACHE=$2
fi



GIT_BRANCH=$1
date_var=$(date +%Y.%m.%d.%H.%M%S)
BUILD_TAG=thakurpriya1990/boranga:v$date_var
#git checkout $GIT_BRANCH &&
#git pull &&
cd boranga/frontend/boranga/ &&
npm run build &&
cd ../../../ &&
source venv/bin/activate &&
#./manage_co.py collectstatic --no-input &&
docker image build $NO_CACHE --tag $BUILD_TAG . &&
echo $BUILD_TAG &&
docker push $BUILD_TAG
