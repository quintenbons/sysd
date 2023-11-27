#!/bin/bash
JOB_IDS=$(oarstat -u | awk 'NR>2 {print $1}')
echo $JOB_IDS | xargs -r oardel
