#! /bin/bash

# cleanup everything, except venv and .env
git clean -dXfq -e !.env !venv/

# check if we're in virtual environment
if ! command -v deactivate &>/dev/null; then
	# if not, does one exist
	if ! [ -d "./venv" ]; then
		python3 -m venv venv
	fi
	# activate virtual environment
	source ./venv/bin/activate
fi

# install python packages
pip install -r requirements.txt
