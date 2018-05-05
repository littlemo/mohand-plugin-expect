from mohand import hands
from mohand_plugin_expect.hand import expect


class ExpectHand(hands.HandBase):
    def register(self):
        # print('ExpectHand:', expect)
        return expect
