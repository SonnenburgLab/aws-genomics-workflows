#!/usr/bin/env python3
import boto3
import pandas as pd
from numpy import random
from time import sleep


def submit_batch_job(
    project: str,
    sample_name: str,
    fwd: str,
    rev: str,
    branch="main",
    job_queue="priority-nextflow-gwfcore",
    job_definition="nextflow-nextflow-nextflow",
):
    """Submit jobs for the nf-placeholder pipeline to AWS Batch

    Args:
        project (_str_): name of the project
        sample_name (_str_): name of the sample
        fwd (_str_): s3 path to QC-ed fwd file
        rev (_str_): s3 path to QC-ed rev file
        branch (str, optional): Branch of nf-placeholder to use. Defaults to "main".
        job_queue (str, optional): name of the queue for the head node. Defaults to "priority-nextflow-gwfcore".
        job_definition (str, optional): nextflow job definition. Doesn't usually change. Defaults to "nextflow-nextflow-nextflow".
        session (_type_, optional): boto3 session object for non-default aws profile. Defaults to sonn.

    Returns:
        _type_: _description_
    """

    # Create a session object using the AWS profile you'd like to use.
    session = boto3.session.Session()
    batch = session.client("batch")

    # Submit the job; capture the response
    response = batch.submit_job(
        jobName=f"nf-ph-{sample_name}",
        jobQueue=job_queue,
        jobDefinition=job_definition,
        containerOverrides={
            "command": [
                "SonnenburgLab/nf-placeholder",
                "-r",  # this is a reserved nextflow flag that tells it to use a specific branch/tag/revision
                branch,
                "--project",
                project,
                "--prefix",
                sample_name,
                "--singleEnd",
                "false",
                "--reads1",
                fwd,
                "--reads2",
                rev,
            ]
        },
    )

    # the response is a JSON object that contains details about the job submission
    # include the `jobId`. This `jobId` can be used with
    # `batch.describe_jobs(jobs = [jobId])` to check on the status of the job.
    return response


def read_manifest(filename: str) -> pd.DataFrame:
    # code to read some input file and
    # return a dataframe with headers as 'sampleName,R1,R2'
    return


### MAIN ###

project = "project"
my_manifest_file = "my_manifest.file"
my_manifest = read_manifest(my_manifest_file)

responses = list()
for row in my_manifest.itertuples():
    responses.append(submit_batch_job(project, row.sampleName, row.R1, row.R2))
    sleep(random.uniform(0, 1))  # to not overwhelm AWS

print(f"{len(responses)} jobs submitted.")
