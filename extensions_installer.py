import subprocess
import sys

if __name__ == '__main__':
    subprocess.call([sys.executable, '-m', 'pip', 'install', '-e', './src/extensions/games/tic_tac_toe'])
