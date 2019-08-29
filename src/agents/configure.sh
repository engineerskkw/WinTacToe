#!/bin/bash


pipenv install --skip-lock
python -m ipykernel install --user --name=Python3.7-WinTacToe
pipenv shell