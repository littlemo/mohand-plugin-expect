from mohand import hand
from mohand_plugin_expect.hand import expect


class ExpectHand(hand.HandBase):
    def register(self):
        # print('ExpectHand:', expect)
        return expect
