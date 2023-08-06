from typing import Optional

from pydispix.client import Client


class MultiClient:
    def __init__(self, tokens: list, multiplex_amt: Optional[int] = None, multiplexed_positions: list[int] = None, *args, **kwargs):
        """
        Use multiple tokens to speed up the tasks.

        We can also use `multiplex_amt` to define precise amount of multiplexed work to be done.
        This is usually done to share work with other servers, since we can only work on a portion
        of multiplexed work.

        The portion reserved for this machine to work on is defined with `multiplexed_positions`.
        This variable needs to be set if `multiplex_amt` is higher than amount of aviable `tokens`.
        This variable should hold the indices of multiplexed work:
            With `multiplex_amt` of 10 and 5 `tokens`, we could work on first 5 positions:
            `multiplexed_positions = [0,1,2,3,4]`
            With the second server holding other 5 tokens working on the remaining 5 positions:
            `multiplexed_positions = [5,6,7,8,9]`

        If we have less `multiplexed_positions` than
        """
        raise NotImplementedError("This feature is still work in progress.")
        if multiplex_amt is None:
            multiplex_amt = len(tokens)

        self.tokens = tokens
        self.clients = [Client(token, *args, **kwargs) for token in tokens]
