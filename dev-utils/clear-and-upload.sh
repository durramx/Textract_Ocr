#!/usr/bin/env bash

bucket=

aws s3 rm s3://automated-plagiarism-detection-dev-us-west-2-/uploadpdf/*
aws s3 rm s3://automated-plagiarism-detection-dev-us-west-2-/output/*
aws s3 cp capstone_v1.pdf s3://automated-plagiarism-detection-dev-us-west-2-/uploadpdf/capstone_v1.pdf