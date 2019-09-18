from subprocess import call
import sys

if __name__ == '__main__':
    call([sys.executable, '-m', 'pip', 'install', '-e', './src/components/games/gym_environments/tic_tac_toe'])
