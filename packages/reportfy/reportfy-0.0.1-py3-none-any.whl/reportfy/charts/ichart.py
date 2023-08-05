from charts.axes import Axes
from charts.series import Series


class IChart:
    title = None
    axes = None
    series = None

    def __init__(self, title="My Chart", axes=None, series=[]):
        self.title = title
        self.axes = axes
        self.series

        assert type(self.title) == str
        assert type(self.axes) == Axes or self.axes == None
        assert type(self.series) == list and (
            len(self.series) == 0 or all([type(s) == Series for s in self.series])
        )

    def render(self):
        raise NotImplementedError
