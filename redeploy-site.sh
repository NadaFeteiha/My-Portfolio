#!/bin/bash

echo "********************************************"
# init project location and go to it
PORTFOLIO_DIR=~/My-Portfolio

# check if portfolio exists
if [ ! -d "$PORTFOLIO_DIR" ]; then
    echo "********************************************"
    echo "Portfolio directory does not exist."
    echo "Cloning repository..."
    git clone https://github.com/NadaFeteiha/My-Portfolio.git $PORTFOLIO_DIR
else
    # get all new changes from git repos
    echo "********************************************"
    echo "fetching new commits on repository..."
    git fetch && git reset --hard origin/main
fi

cd $PORTFOLIO_DIR
# same step to run VM
echo "********************************************"
echo "setting up virtual environment..."
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate

# install req
echo "********************************************"
echo "installing requirements..."
pip install -r requirements.txt

echo "********************************************"
echo "Starting services"
systemctl restart myportfolio.service

echo "********************************************"
echo "portfolio redeployed successfully!"
