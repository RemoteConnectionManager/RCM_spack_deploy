#!/bin/bash

python scripts/deploy_setup.py --integration --dest=deploy/spack --debug=debug  --branches clean/develop     pr/.*  wip/.*  --prlist 2686 2771 2902 3041 3057
