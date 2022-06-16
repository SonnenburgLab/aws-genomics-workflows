#!/bin/bash -x
set -euo pipefail

# Update these to play around with different configurations
DIST_BUCKET=${1:-"sonn-pipelines-assets"} # no 's3://'
# STACK_NAME="sonn-pipelines"
# RESULTS_BUCKET="sonn-nextflow-results"

# DO NOT UPDATE THESE, UNLESS YOU KNOW WHAT YOU'RE DOING
###############################################################################
REGION="us-west-2"
###############################################################################

# SETUP

## Create an S3 bucket in your AWS account to use for the distribution deployment
## will throw an error if this bucket already exists
aws s3 mb s3://${DIST_BUCKET} 

## Assumes your default AWS profile points to the Sonnenburg Lab AWS account
## If that's not the case, update "--asset-profile <profile-name>" in the command below.
bash _scripts/deploy.sh --deploy-region ${REGION} --asset-profile default --asset-bucket s3://${DIST_BUCKET} test


TEMPLATE_ROOT_URL=https://${DIST_BUCKET}.s3-${REGION}.amazonaws.com/test/templates
AMAZON_S3_URI=$TEMPLATE_ROOT_URL/nextflow/nextflow-and-core.template.yaml
echo ""
echo "-----------------------------------------"
echo "   Make a note of the following values   "
echo "-----------------------------------------"
echo "TEMPLATE_ROOT_URL: ${TEMPLATE_ROOT_URL}"
echo "AMAZON_S3_URI: ${AMAZON_S3_URI}"
echo "-----------------------------------------"
echo ""