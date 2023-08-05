"""

    Tool command Account Create


"""
import logging
import secrets

from .command_base import CommandBase

logger = logging.getLogger(__name__)


class AccountCreateCommand(CommandBase):

    def __init__(self, sub_parser=None):
        super().__init__('create', sub_parser)

    def create_parser(self, sub_parser):
        parser = sub_parser.add_parser(
            self._name,
            description='Create a new account',
            help='Create a new account'
        )

        parser.add_argument(
            '--topup',
            action='store_true',
            help='Topup account with sufficient funds. This only works for development networks. Default: False',
        )

        parser.add_argument(
            '-n',
            '--name',
            nargs='?',
            help='account name to register'
        )

        return parser

    def execute(self, args, output):
        convex = self.load_convex(args.url)

        import_account = self.import_account(args)
        logger.debug('creating account')
        account = convex.create_account(account=import_account)

        if args.topup:
            logger.debug('auto topup of account balance')
            convex.topup_account(account)

        if args.name:
            logger.debug(f'registering account name {args.name}')
            convex.topup_account(account)
            account = convex.register_account_name(args.name, account)
        if args.password:
            password = args.password
        else:
            password = secrets.token_hex(32)
        values = {
            'password': password,
            'address': account.address,
            'keyfile': account.export_to_text(password),
            'keywords': account.export_to_mnemonic,
            'balance': convex.get_balance(account)
        }
        if account.name:
            values['name'] = account.name
        output.set_values(values)
        output.add_line_values(values)
