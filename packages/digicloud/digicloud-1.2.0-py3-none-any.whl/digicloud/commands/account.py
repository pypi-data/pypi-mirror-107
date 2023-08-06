"""
    Authentication to digicloud API.
"""
import getpass

from digicloud.commands.base import ShowOne, Command
from digicloud.error_handlers import CLIError
from digicloud.utils import is_tty


class Login(ShowOne):
    """Digicloud Login"""

    def get_parser(self, prog_name):
        parser = super(Login, self).get_parser(prog_name)
        parser.add_argument(
            '--email',
            required=False,
            default=None,
            metavar='<EMAIL>',
            dest='email',
            help=("Your Digicloud email")
        )

        parser.add_argument(
            '--password',
            metavar='<PASSWORD>',
            required=False,
            default=None,
            dest='password',
            help=("Your Digicloud account password")
        )

        parser.add_argument(
            '--namespace',
            metavar='<NAMESPACE>',
            dest='namespace',
            help=("ID of the Digicloud namespace")
        )

        return parser

    def get_data(self, parsed_args):
        payload = {
            'email': parsed_args.email or self._get_email(),
            'password': parsed_args.password or self._get_password(),
        }
        data = self.app.session.post('/tokens', payload)

        # NOTE: User may have no default namespace
        ns_ref = parsed_args.namespace or data['user']['default_namespace']
        selected_ns = self._find_namespace(ns_ref, data['namespaces'])

        self.app.config['api_token'] = data['token']
        self.app.config['AUTH_HEADERS'].update({
            'Authorization': 'Bearer {}'.format(data["token"]),
            'Digicloud-Namespace': selected_ns['id'],
        })
        self.app.config['USER'] = data['user']
        return {
            "Email": data['user']['email'],
            "Namespace name": selected_ns['name'],
            "Namespace ID": selected_ns['id'],
            "Region": self._get_active_region()
        }

    def _find_namespace(self, name_or_id, namespaces):
        if name_or_id is None:
            return namespaces[0]

        result = [ns for ns in namespaces
                  if name_or_id == ns['name'] or name_or_id == ns['id']]
        if len(result) == 0:
            print("You're not a member of '{}' namespace".format(name_or_id))
            return
        elif len(result) > 1:
            print("There are more than one namespace named '{}'".format(name_or_id))
            return
        return result[0]

    def _get_active_region(self):
        self.app.setup_session()
        auth_headers = self.app.config['AUTH_HEADERS']
        if 'Digicloud-Region' not in auth_headers:
            regions = self.app.session.get('/regions')
            if len(regions) == 0:
                raise Exception("There are no region available for your namespace, "
                                "Please contact support for further information.")
            auth_headers['Digicloud-Region'] = regions[0]['name']
        return auth_headers['Digicloud-Region']

    def _get_email(self):
        if not is_tty():
            raise Exception("Unable to login in non-interactive mode without --email")
        return input("Email: ")

    def _get_password(self):
        if not is_tty():
            raise Exception("Unable to login in non-interactive mode without --password")
        return getpass.getpass()

    def _on_401(self, parsed_args, exp):
        return CLIError([
            dict(
                msg="Username and password do not matched",
                hint="use this link in case you forget your password: "
                     "https://console.digicloud.ir/auth/forgot-password"
            )
        ])


class Logout(Command):
    """DigiCloud Logout"""

    def take_action(self, parsed_args):
        if 'api_token' in self.app.config:
            self.app.session.delete('/tokens/{}'.format(self.app.config['api_token']))
            del self.app.config['api_token']

        del self.app.config['AUTH_HEADERS']
        del self.app.session.headers['Authorization']

        return 0
