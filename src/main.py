# This file must be executed by python instead of executing src/spc/cli.py
# directly because the directory of the script gets added to PYTHONPATH

import spc.cli
spc.cli.main()
