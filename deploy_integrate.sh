#!/bin/bash

python scripts/deploy_setup.py --integration --dest=deploy/spack --debug=debug  --branches clean/develop     pr/.*  wip/.*  --prlist 2763 2771 2902 2686 2928
