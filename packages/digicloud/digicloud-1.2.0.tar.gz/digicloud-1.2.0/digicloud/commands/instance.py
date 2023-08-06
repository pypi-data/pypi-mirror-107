"""
    DigiCloud Compute Instance Service.
"""

from cliff.command import Command

from digicloud import schemas
from .base import Lister, ShowOne
from ..error_handlers import CLIError
from ..utils import is_tty


class ListInstance(Lister):
    """List instances."""
    help_file = 'instance.txt'
    schema = schemas.InstanceList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstance, self).get_parser(prog_name)
        parser.add_argument(
            '--simple',
            help='Advanced instances',
            default=None,
            action='store_true'
        )

        parser.add_argument(
            '--advanced',
            help='Simple instances',
            default=None,
            action='store_true'
        )

        return parser

    def get_data(self, parsed_args):
        args = (parsed_args.simple, parsed_args.advanced)
        if all(args):
            raise Exception("You need to specify one of --simple or --advanced")

        query_params = {}
        if parsed_args.simple:
            query_params['type'] = 'simple'
        elif parsed_args.advanced:
            query_params['type'] = 'advanced'

        data = self.app.session.get( '/instances', params=query_params)
        return data


class CreateInstance(ShowOne):
    """Create instance."""
    help_file = 'instance.txt'
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(CreateInstance, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Instance name'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Instance description'
        )
        parser.add_argument(
            '--instance-type',
            required=True,
            metavar='<instance_type>',
            help='InstanceType name or ID'
        )
        parser.add_argument(
            '--image',
            required=True,
            metavar='<image>',
            help='Image name or ID'
        )
        parser.add_argument(
            '--network',
            required=False,
            metavar='<network>',
            help='Network name or ID'
        )
        parser.add_argument(
            '--ssh-key',
            metavar='<ssh_key>',
            help='SSH key name'
        )

        parser.add_argument(
            '--firewall',
            metavar='<firewall>',
            default=[],
            action='append',
            help='Firewall name or ID'
        )
        parser.add_argument(
            '--simple',
            help='Create a instance quickly',
            default=None,
            action='store_true'
        )
        parser.add_argument(
            '--with-floating-ip',
            help='Create and associate a Floating IP automatically',
            default=None,
            action='store_true'
        )
        parser.add_argument(
            '--additional-volumes',
            metavar='<additional_volumes>',
            default=[],
            action='append',
            help='attach additional volume automatically, e.g --additional-volumes 500'
        )

        parser.add_argument(
            '--advanced',
            help='Create a instance with more configuration parameters',
            default=None,
            action='store_true'
        )

        return parser

    def _check_arg_validity(self, parsed_args):
        rules = [
            (
                all((parsed_args.advanced, parsed_args.simple)),
                "--advanced and --simple should not be used together",
            ),
            (
                parsed_args.simple and parsed_args.network is not None,
                "--simple and --network should not be used together",
            ),
            (
                parsed_args.simple and parsed_args.firewall,
                "--simple and --firewall should not be used together",
            ),
            (
                parsed_args.advanced and parsed_args.network is None,
                "--advanced requires --network to be present",
            ),
            (
                not parsed_args.simple and parsed_args.network is None,
                "--network is mandatory in advanced mode",
            ),

        ]

        for is_invalid, err_msg in rules:
            if is_invalid:
                raise Exception(err_msg)

    def get_data(self, parsed_args):
        self._check_arg_validity(parsed_args)
        payload = {
            'name': parsed_args.name,
            'instance_type': parsed_args.instance_type,
            'image': parsed_args.image,
            'type': 'simple' if parsed_args.simple else 'advanced',
        }
        if parsed_args.network:
            payload['network'] = parsed_args.network
        if parsed_args.ssh_key:
            payload['ssh_key_name'] = parsed_args.ssh_key
        if parsed_args.firewall:
            payload['security_groups'] = parsed_args.firewall
        if parsed_args.additional_volumes:
            payload['additional_volumes'] = [
                {
                    "size": volume_size,
                    "volume_type": "SSD",
                } for volume_size in parsed_args.additional_volumes
            ]
        if parsed_args.with_floating_ip:
            payload['has_floating_ip'] = parsed_args.with_floating_ip
        if parsed_args.description:
            payload['description'] = parsed_args.description

        data = self.app.session.post('/instances', payload)
        return data


class ShowInstance(ShowOne):
    """Show instance details."""
    help_file = 'instance.txt'
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(ShowInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s' % parsed_args.instance
        data = self.app.session.get(uri)
        return data


class DeleteInstance(Command):
    """Delete a instance."""
    help_file = 'instance.txt'

    def get_parser(self, prog_name):
        parser = super(DeleteInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        parser.add_argument(
            '--delete-volumes',
            metavar='<instance>',
            help='Instance name or ID',
        )

        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        if not self.confirm(parsed_args):
            return
        if parsed_args.delete_volumes:
            volumes_uri = '/instances/%s/volumes' % parsed_args.instance
            volumes = self.app.session.get(volumes_uri)
            for volume in volumes:
                del_vol_uri = '/instances/%s/volumes/%s' % parsed_args.instance, volume[
                    'id']
                self.app.session.delete(del_vol_uri)

        uri = '/instances/%s' % parsed_args.instance
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            instance = self.app.session.get('/instances/%s' % parsed_args.instance)
            user_response = input(
                "You're about to delete the instance named {}  "
                "Are you sure? [yes/no]".format(
                    instance['name']
                ))
            if user_response == "yes":
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write(
                "Unable to perform 'instance delete' operation in non-interactive mode,"
                " without '--i-am-sure' switch\n")
            return False


class StartInstance(Command):
    """Start instance."""

    def get_parser(self, prog_name):
        parser = super(StartInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/state-transitions' % parsed_args.instance
        self.app.session.post(uri, payload=dict(new_state="ACTIVE"))


class StopInstance(Command):
    """Stop instance."""

    def get_parser(self, prog_name):
        parser = super(StopInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/state-transitions' % parsed_args.instance
        self.app.session.post(uri, payload=dict(new_state="SHUTOFF"))


class SuspendInstance(Command):
    """Suspend instance."""

    def get_parser(self, prog_name):
        parser = super(SuspendInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/state-transitions' % parsed_args.instance
        self.app.session.post(uri, payload=dict(new_state="SUSPENDED"))


class ResumeInstance(Command):
    """Resume instance."""

    def get_parser(self, prog_name):
        parser = super(ResumeInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/state-transitions' % parsed_args.instance
        self.app.session.post(uri, payload=dict(new_state="ACTIVE"))


class RebootInstance(Command):
    """Reboot instance."""

    def get_parser(self, prog_name):
        parser = super(RebootInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )

        parser.add_argument(
            '--type',
            default='SOFT',
            metavar='<type>',
            help='either `SOFT` for a software-level reboot, or `HARD` for a virtual '
                 'power cycle hard reboot',
            choices=['SOFT', 'HARD']
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/state-transitions' % parsed_args.instance
        self.app.session.post(uri, payload=dict(new_state="REBOOT",
                                                params={"reboot_type": parsed_args.type}))


class ListInstanceVolume(Lister):
    """List instance volume(s)."""
    schema = schemas.InstanceVolume(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        # TODO: Could use a little bit of cache maybe
        # TODO: Duplicate logic
        volumes = {
            v['id']: v for v in self.app.session.get('/volumes')
        }
        instance_info = self.app.session.get('/instances/%s' % parsed_args.instance)
        uri = '/instances/%s/volumes' % instance_info['id']
        instance_volumes = self.app.session.get(uri)
        return [
            {
                "instance": instance_info['name'],
                "volume": volumes[volume['id']]['name'],
                **volume
            }
            for volume in instance_volumes

        ]


class ShowInstanceVolume(ShowOne):
    """Show instance volume details."""
    schema = schemas.InstanceVolume(many=False)

    def get_parser(self, prog_name):
        parser = super(ShowInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID',
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID',
        )
        return parser

    def get_data(self, parsed_args):
        # TODO: Could use a little bit of cache maybe
        # TODO: Duplicate logic
        volumes = {
            v['id']: v for v in self.app.session.get('/volumes')
        }
        instance_info = self.app.session.get('/instances/%s' % parsed_args.instance)
        uri = '/instances/%s/volumes/%s' % (parsed_args.instance, parsed_args.volume)
        instance_volume = self.app.session.get(uri)
        return {
            "instance": instance_info['name'],
            "volume": volumes[instance_volume['id']]['name'],
            **instance_volume
        }


class AttachInstanceVolume(ShowOne):
    """Attach instance volume."""
    schema = schemas.InstanceVolume(many=False)

    def get_parser(self, prog_name):
        parser = super(AttachInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/volumes' % parsed_args.instance
        payload = {'id': parsed_args.volume}

        data = self.app.session.post(uri, payload)

        return data


class DetachInstanceVolume(Command):
    """Detach instance volume."""

    def get_parser(self, prog_name):
        parser = super(DetachInstanceVolume, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--volume',
            required=True,
            metavar='<volume>',
            help='Volume name or ID'
        )

        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/volumes/%s' % (parsed_args.instance, parsed_args.volume)
        self.app.session.delete(uri)


class ListInstanceInterface(Lister):
    """List instance interface(s)."""
    schema = schemas.InstanceInterface(many=True)

    def get_parser(self, prog_name):
        parser = super(ListInstanceInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/interfaces' % parsed_args.instance
        data = self.app.session.get(uri)

        return data


class AttachInterface(ShowOne):
    """Attach interface."""
    schema = schemas.InstanceInterface(many=False)

    def get_parser(self, prog_name):
        parser = super(AttachInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--network',
            required=True,
            metavar='<network>',
            help='Network name or ID',

        )
        return parser

    def get_data(self, parsed_args):
        payload = {'net': parsed_args.network}
        uri = '/instances/%s/interfaces' % parsed_args.instance
        data = self.app.session.post(uri, payload)
        return data


class DetachInterface(Command):
    """Detach interface."""

    def get_parser(self, prog_name):
        parser = super(DetachInterface, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--interface-id',
            required=True,
            metavar='<interface>',
            help='Interface ID',

        )

        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/interfaces/%s' % (
            parsed_args.instance, parsed_args.interface_id)
        self.app.session.delete(uri)


class UpdateInstance(ShowOne):
    """Update instance name."""
    schema = schemas.InstanceDetails()

    def get_parser(self, prog_name):
        parser = super(UpdateInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance ID or name',
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=False,
            help=('Instance new name, should be unique'),
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            required=False,
            help=('Instance description'),
        )
        parser.add_argument(
            '--instance-type',
            metavar='<instance_type>',
            required=False,
            help=('Instance type'),
        )

        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s' % parsed_args.instance
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description
        if parsed_args.instance_type:
            payload['instance_type'] = parsed_args.instance_type
            self.app.console.print(
                "Resizing your instance might cause additional charges",
                style='bold yellow'
            )
        if not payload:
            raise Exception(
                "At least one of --name or --description or "
                "--instance-type should be provided"
            )
        data = self.app.session.patch(uri, payload)

        return data

    def _on_400(self, parsed_args, response):
        error_msg = response.json()['errors']
        if 'stop your instance' in error_msg:
            return CLIError([
                dict(
                    msg=error_msg,
                    hint="You can stop your instance by running: "
                         "[bold blue]digicloud instance stop {}[/bold blue]".format(
                        parsed_args.instance
                    )
                )
            ])


class ListFirewall(Lister):
    """List Instance Firewalls"""
    schema = schemas.FirewallList(many=True)

    def get_parser(self, prog_name):
        parser = super(ListFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        return parser

    def get_data(self, parsed_args):
        uri = '/instances/%s/security-groups' % parsed_args.instance
        data = self.app.session.get(uri)
        return data


class AddFirewall(Command):
    """Add Firewall to instance"""

    def get_parser(self, prog_name):
        parser = super(AddFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--firewall',
            required=True,
            metavar='<firewall>',
            help='Firewall name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        payload = {'security_group_ref': parsed_args.firewall}
        uri = '/instances/%s/security-groups' % parsed_args.instance
        self.app.session.post(uri, payload)


class RemoveFirewall(Command):
    """Remove Firewall from Instance"""

    def get_parser(self, prog_name):
        parser = super(RemoveFirewall, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help='Instance name or ID'
        )
        parser.add_argument(
            '--firewall',
            required=True,
            metavar='<firewall>',
            help='Firewall name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instances/%s/security-groups/%s' % (parsed_args.instance,
                                                    parsed_args.firewall)
        self.app.session.delete(uri)
