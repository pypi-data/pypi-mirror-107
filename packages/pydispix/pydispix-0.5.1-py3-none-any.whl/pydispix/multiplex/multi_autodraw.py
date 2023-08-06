from pydispix.canvas import Pixel
from pydispix.autodraw import AutoDrawer
from pydispix.multiplex.multi_client import MultiClient


class MultiAutoDrawer():
    def __init__(
        self,
        multiplexed_client: MultiClient,
        x: int, y: int,
        grid: list[list[Pixel]]
    ):
        """
        Split the image to same sized parts of the image grid.
        This splitting is happening by lines, which means there can't be
        more requested splits preset than there are lines.

        *Note: It would be better to evenly split the matrix, but there's
        no way I'm implementing that, feel free to make a PR.
        """
        raise NotImplementedError("This is not yet ready for production.")
        self.grid = grid
        # Top left coords.
        self.x0 = x
        self.y0 = y
        # Bottom right coords.
        self.x1 = x + len(self.grid[0])
        self.y1 = y + len(self.grid)

        self.split_parts = multiplexed_client.multiplex_amt
        self.parts_to_use = multiplexed_client.multiplexed_positions

        if len(self.grids) < self.parts_to_use:
            return ValueError(
                f"Unable to split {len(self.grids)} lines to {self.parts_to_use} even chunks, "
                "can't split to more parts than we have horizontal lines."
            )
        # Get needed clients to do `parts_to_use`
        self.clients = []
        for _ in range(self.parts_to_use):
            client = multiplexed_client.get_free_client(retry=True)
            multiplexed_client.clients[client] = False
            self.clients.append(client)

        self.parts = []
        # Split horizontal lines of the image evenly between our clients
        lines_per_client = len(grid) // self.split_parts
        for start_line in range(0, len(grid), lines_per_client):
            client_grid = grid[start_line:start_line + lines_per_client]
            client_y0 = self.y0 + start_line
            self.parts.append(client_grid, client_y0)

        # Make AutoDrawers for each part that we should use
        self.drawers = []
        for part_id in self.parts_to_use:
            client = self.clients[part_id]
            client_grid, client_y0 = self.parts[part_id]
            drawer = AutoDrawer(client, self.x0, client_y0, client_grid)
            self.drawers.append(drawer)

    @classmethod
    def load_image(cls, multiplexed_client: MultiClient, *args, **kwargs) -> "MultiAutoDrawer":
        # We have to go through `AutoDrawer` initialization here, and use the parameters from
        # the created instance to initialize out instance. This is the only way to avoid
        # too much code repetition, the initialization is relatively fast, so it shouldn't
        # be a huge issue

        mock_client = object()  # we must pass something as client, but it won't be used in any way
        auto_drawer = AutoDrawer.load_image(mock_client, *args, **kwargs)
        return cls(multiplexed_client, auto_drawer.x0, auto_drawer.y0, auto_drawer.grid)

    @classmethod
    def load(cls, multiplexed_client: MultiClient, *args, **kwargs) -> "MultiAutoDrawer":
        # Similarely to the method above, we need to initialize `AutoDrawer` here
        # to obtain parameters for our initialization

        mock_client = object()  # we must pass something as client, but it won't be used in any way
        auto_drawer = AutoDrawer.load(mock_client, *args, **kwargs)
        return cls(multiplexed_client, auto_drawer.x0, auto_drawer.y0, auto_drawer.grid)
