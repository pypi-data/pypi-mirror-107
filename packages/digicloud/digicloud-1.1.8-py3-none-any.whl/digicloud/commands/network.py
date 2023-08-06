"""
    DigiCloud Network Service.
"""
from cliff.command import Command

from .base import Lister, ShowOne
from .. import schemas


def enrich_network_details(session, network_details):
    subnets = {
        subnet['id']: subnet
        for subnet in session.get('/subnets')
    }

    network_details['subnets'] = [
        {
            "name": subnets[subnet_id]['name'],
            "cidr": subnets[subnet_id]['cidr'],
            "gateway": subnets[subnet_id]['gateway_ip'],
        }
        for subnet_id in network_details['subnets']
    ]
    return network_details


class ListNetwork(Lister):
    """List networks"""
    help_file = 'network.txt'
    schema = schemas.NetworkList(many=True)

    def get_data(self, parsed_args):
        networks = self.app.session.get('/networks')
        return networks


class ShowNetwork(ShowOne):
    """Show network details."""
    schema = schemas.NetworkDetail()

    def get_parser(self, prog_name):
        parser = super(ShowNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        network = self.app.session.get(uri)
        return enrich_network_details(self.app.session, network)


class DeleteNetwork(Command):
    """Delete network."""

    def get_parser(self, prog_name):
        parser = super(DeleteNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        self.app.session.delete(uri)


class UpdateNetwork(ShowOne):
    """Update network."""
    schema = schemas.NetworkDetail()

    def get_parser(self, prog_name):
        parser = super(UpdateNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network ID',
        )
        parser.add_argument(
            '--name',
            metavar='<Name>',
            help='New name for network.'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<Description>',
            help='New admin state.'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.admin_state:
            payload['admin_state'] = parsed_args.admin_state
        if not payload:
            raise Exception("At least one of --name or --admin_state is necessary")
        data = self.app.session.patch(uri, payload)
        return enrich_network_details(self.app.session, data)


class CreateNetwork(ShowOne):
    """Create Network"""
    schema = schemas.NetworkDetail()

    def get_parser(self, prog_name):
        parser = super(CreateNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Network name'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<AdminState>',
            default='UP',
            help='Set admin state (default UP).'
        )
        return parser

    def get_data(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'admin_state': parsed_args.admin_state
        }
        data = self.app.session.post('/networks', payload)
        return enrich_network_details(self.app.session, data)
