#!/bin/bash
set -e

./prepareDeploy.sh
cd ../server
aws s3 cp full.zip s3://chat-app-codes/full.zip

VERSION_LABEL="v$(date +%Y%m%d%H%M%S)"

echo "New version label $VERSION_LABEL"

aws elasticbeanstalk create-application-version \
    --application-name class1 \
    --version-label $VERSION_LABEL \
    --source-bundle S3Bucket=chat-app-codes,S3Key=full.zip \
    --no-cli-pager
aws elasticbeanstalk update-environment \
    --environment-name Class1-env \
    --version-label $VERSION_LABEL \
    --no-cli-pager

echo "Deploy completed successfully"