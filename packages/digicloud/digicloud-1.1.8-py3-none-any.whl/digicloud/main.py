"""
    Main app components definition.
"""
import signal
import sys
import time

from pkg_resources import get_distribution
from cliff.app import App
from cliff.commandmanager import CommandManager
from rich.console import Console

from digicloud.cli import signal_handler
from digicloud.error_handlers import ErrorHandler
from .managers import ConfigManager, Session, VersionChecker
from .utils import get_help_file


class DigicloudApp(App):
    """Overwrite ``cliff.app.App`` class.

    Make possibility to further extension and overwrite methods.
    """

    def __init__(self):
        command_manager = CommandManager('digicloud.cli')
        self.current_version = get_distribution('digicloud').version
        self.debug_mode = False
        super(DigicloudApp, self).__init__(
            description=get_help_file('digicloud.txt'),
            version=self.current_version,
            command_manager=command_manager,
            deferred_help=True
        )
        self.config = ConfigManager(self.LOG)
        # Http session from requests.Session.
        base_url = self.config['BASE_URL']
        self.session = self.config.get('SESSION', Session(base_url))
        self.error_handler = ErrorHandler(self)
        self.console = Console()

    def initialize_app(self, argv):
        signal.signal(signal.SIGINT, signal_handler.interrupt_handler)
        self.LOG.debug('Initialize session')
        self.setup_session()

    def setup_session(self):
        self.session.base_url = self.config['BASE_URL']

        if self.config.get('AUTH_HEADERS'):
            auth_headers = self.config['AUTH_HEADERS']
            self.session.headers.update(auth_headers)
            self.config['SESSION'] = self.session
        else:
            self.config['AUTH_HEADERS'] = {}
        self.config.save()

    def clean_up(self, cmd, result, err):
        """Is invoked after a command runs."""
        self.config.save()
        self.LOG.debug('Configuration saved.')
        if err:
            self.LOG.debug(err)

    def run(self, argv):
        self.debug_mode = '--debug' in argv
        self._check_version()
        return super(DigicloudApp, self).run(argv)

    def _check_version(self):
        try:
            version_checker = VersionChecker('digicloud')
            now = int(time.time())
            if 'last_version_check_time' in self.config:
                last_version_check_time = int(self.config['last_version_check_time'])
                if now - last_version_check_time < 3600:
                    return
            latest_release_version = version_checker.get_latest_version_number()
            self.config['last_version_check_time'] = now
            if self.current_version != latest_release_version:
                self.stdout.write(
                    "\033[91mCurrent digicloud is not the latest released version, "
                    "Please consider updating your digicloud CLI using "
                    "'pip install digicloud -U'\033[0m\n"
                )
        except Exception as exp:
            if self.debug_mode:
                raise exp


def main(argv=None):
    """Initialize main ``cliff.app.App`` instance and run.

    Cliff look for this function as a console script entry point.
    """
    if not argv:
        argv = sys.argv[1:]
    if len(argv) == 0:  # Disable interactive mode
        argv = ['--help']  # display --help instead of interactive mode
    if argv == ['--help']:
        print(get_help_file('digicloud.txt'))
        sys.exit()
    return DigicloudApp().run(argv)


if __name__ == '__main__':
    sys.exit(main())
