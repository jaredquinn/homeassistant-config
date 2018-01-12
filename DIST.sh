#!/bin/bash
# DIST script used to update some files to keep the secrets

# Update secrets template file
awk  '{print $1}' > secrets.yaml.dist < secrets.yaml


