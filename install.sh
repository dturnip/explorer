#!/bin/sh

# Check if python3.10+ is installed and bound to python3

ERROR_PREFIX="\033[1;4;31m[ERROR]\033[0m"
SUCCESS_PREFIX="\033[1;4;32m[SUCCESS]\033[0m"
command -v python3 &>/dev/null || { echo >&2 "${ERROR_PREFIX} python3 is not" \
	"installed!\nAborting..."; exit 1; }

PY_VERSION=$(python3 -V | cut -d ' ' -f2)
IFS='.' array=($PY_VERSION)

[ ${array[1]} -lt 10 ] && { echo >&2 "${ERROR_PREFIX} Only python 3.10+ is"\
	"supported; current version bound to \`python3\`: ${PY_VERSION}\n" \
	"Aborting..."; exit 1; }

# Execute the following if python3.10+ is installed and bound

echo "~~~ Begin Installation ~~~"
git clone https://github.com/dturnip/explorer.git
cd ./explorer/
echo "~~~ Creating virtual environment ~~~"
python3 -m venv venv && source ./venv/bin/activate
echo "~~~ Installing dependencies ~~~"
pip install -r requirements.txt --disable-pip-version-check
echo "~~~ Removing installation script ~~~"
rm ./install.sh
echo "${SUCCESS_PREFIX} Installation complete!"

exit 0
