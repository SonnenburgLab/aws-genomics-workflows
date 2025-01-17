# Genomics Workflows on AWS

[![Build Status](https://travis-ci.com/aws-samples/aws-genomics-workflows.svg?branch=master)](https://travis-ci.com/aws-samples/aws-genomics-workflows)

This repository is the source code for [Genomics Workflows on AWS](https://docs.opendata.aws/genomics-workflows).  It contains markdown documents that are used to build the site as well as source code (CloudFormation templates, scripts, etc) that can be used to deploy AWS infrastructure for running genomics workflows.

If you want to get the latest version of these solutions up and running quickly, it is recommended that you deploy stacks using the launch buttons available via the [hosted guide](https://docs.opendata.aws/genomics-workflows).

If you want to customize these solutions, you can create your own distribution using the instructions below.

## Creating your own distribution

Clone the repo

```bash
git clone https://github.com/SonnenburgLab/aws-genomics-workflows.git
```

Create an S3 bucket in your AWS account to use for the distribution deployment

```bash
bash setup.sh <BUCKET-NAME>
```

This will create a `dist` folder in the root of the project with subfolders `dist/artifacts` and `dist/templates` that will be uploaded to the S3 bucket you created above. The command will also output two values `TEMPLATE_ROOT_URL` and `AMAZON_S3_URI`

At this point, it's easier to go to your cloud formation console and create a new stack.

- Under `Prepare template` select `Template is ready`
- Under `Template source` select `Amazon S3 URL` and paste the `AMAZON_S3_URI` output from the above script

Other defaults for the sonnenburg setup:

```md
VPC ID = vpc-aca08fd4
Subnets = subnet-306b691b,subnet-6cab0e26,subnet-2de26870,subnet-ec47ff94
Number of subnets = 4
Artifact Bucket = same as input to 'setup.sh' script; default 'sonn-pipelines-assets'
Results Bucket = sonn-nextflow-results
ExistingBucket = 'true' if using the default else 'false'
Create EFS = 'Yes'; you do not have to create a new one, simply select 'No' here and provide the existing EFS ID in the next textbox
FSx = No
Max CPUs = 4096
```

**NOTE about instance types used in the compute environments**
Default values for `BatchComputeInstanceTypes` in the file `gwfcore-root.template.yaml` was updated to the line below. The compute environments now consists of all available c5, c6i, r5, r6i, m5 and m6i instances. All instances are based on the Intel Xenon architecture

```bash
c5.large,c5.xlarge,c5.2xlarge,c5.4xlarge,c5.9xlarge,c5.12xlarge,c5.18xlarge,c5.24xlarge,c6i.large,c6i.xlarge,c6i.2xlarge,c6i.4xlarge,c6i.8xlarge,c6i.12xlarge,c6i.16xlarge,c6i.24xlarge,c6i.32xlarge,m5.large,m5.xlarge,m5.2xlarge,m5.4xlarge,m5.8xlarge,m5.12xlarge,m5.16xlarge,m5.24xlarge,m6i.large,m6i.xlarge,m6i.2xlarge,m6i.4xlarge,m6i.8xlarge,m6i.12xlarge,m6i.16xlarge,m6i.24xlarge,m6i.32xlarge,r5.large,r5.xlarge,r5.2xlarge,r5.4xlarge,r5.8xlarge,r5.12xlarge,r5.16xlarge,r5.24xlarge,r6i.large,r6i.xlarge,r6i.2xlarge,r6i.4xlarge,r6i.8xlarge,r6i.12xlarge,r6i.16xlarge,r6i.24xlarge,r6i.32xlarge
```

In order to update this, you'd have to update the file and relaunch the entire setup.

## Submitting Jobs

> Before you can submit any jobs please make sure your AWS cli properly configured.

### Using python

Example of a python function that you may use to submit a job can be found in [`examples/example_submission.py`](examples/example_submission.py)

### Using your terminal command line

Here is a sample command.

```bash
aws batch submit-job \
    --profile sonn \
    --job-name nf-sonn-test \
    --job-queue priority-nextflow-gwfcore \
    --job-definition nextflow-nextflow-nextflow \
    --container-overrides command=nextflow-io/rnatoy
```

- `--profile` this is an optional flag, generally used when you have more than one AWS accounts configured on your system.
- `--job-name` this flag assigns an identifiable name to the job submitted on your head node, try to keep it under 80 chars.
- `--job-queue` this should be one of `priority-nextflow-gwfcore` or `default-nextflow-gwfcore`. Usually, if you're using an on-demand instance as your head node, you would submit the job on the `priority-nextflow-gwfcore` queue and have your worker nodes run on `default-nextflow-gwfcore` (this is a setting in your nextflow config)
- `--job-definition` this should ALWAYS be `nextflow-nextflow-nextflow` (yes, it's a weird name. it's a quirk of the automated infrastrucutre deployment script)
- `--container-overrides command=` this is where you'd specify your github repo. Additional flags and values can be provided as a comma-sep list (no spaces between commas!!). Example:

```bash
--container-overrides command=nextflow-io/rnatoy\
"--arg1","arg1_value",\
"--arg2","arg2_value",\
"--arg3","arg3_value"
```

Example of an actual command on the Fischbach Lab infrastructure (this will not work for you):

```bash
aws batch submit-job \
    --profile maf \
    --job-name nf-blast-0825-2 \
    --job-queue default-maf-pipelines \
    --job-definition nextflow-production \
    --container-overrides command=FischbachLab/nf-blast,\
"--query","s3://nextflow-pipelines/blast/data/TY0000004.cons.fa",\
"--db","nt"
```

## License Summary

This library is licensed under the MIT-0 License. See the LICENSE file.
