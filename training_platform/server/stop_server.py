

from training_platform import EnvironmentServer
from training_platform.server.environment_server import AccessingUninitializedEnvServerError

if __name__ == '__main__':
    try:
        server = EnvironmentServer()
        server.shutdown()
        print("Training platform shutdown completed successfully!")
    except AccessingUninitializedEnvServerError:
        print("Nothing to shutdown.")

