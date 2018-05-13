from mohand import hands
from mohand_plugin_expect.hand import expect
from mohand_plugin_expect.version import get_cli_version


class ExpectHand(hands.HandBase):
    def register(self):
        return expect

    def version(self):
        return 'mohand-plugin-expect', get_cli_version()
