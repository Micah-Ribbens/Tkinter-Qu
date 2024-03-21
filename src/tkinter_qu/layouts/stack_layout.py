import abc

from tkinter_qu.gui_components.dimensions import Dimensions
import tkinter_qu


class LayoutType:
    HORIZONTAL = 1
    VERTICAL = 2


class StackLayout(Dimensions, abc.ABC):
    """A class that allows the user to make stack layouts. This allows for greater flexibility in design"""

    layout_type = LayoutType.VERTICAL
    components = []
    percentage_lengths = []
    percentage_heights = []

    def __init__(self, components, layout_type=LayoutType.VERTICAL):
        """Initializes the stack layout"""

        super().__init__(0, 0, 0, 0)
        self.layout_type = layout_type
        self.components = components

    def number_set_dimensions(self, left_edge, top_edge, length, height, update_components=False):
        """Sets the dimensions of this object (does the same thing as __init__)"""

        super().number_set_dimensions(left_edge, top_edge, length, height)

        if update_components:
            self.update_components()

    def update_components(self):
        """Updates the components of the stack layout"""

        pass

    def percentage_set_all_component_dimensions(self, percentage_lengths, percent_heights):
        """Sets the percentages of the components. tkinter_qu.None means evenly divide on remaining space."""



        percent_length_left = float(100 - total_percent_lengths)
        percent_height_left = float(100 - total_percent_heights)

        current_left_edge = 0
        current_top_edge = 0

        default_length = self.length * percent_length_left / 100.0
        default_height = self.height * percent_height_left / 100.0

        for x in range(len(percentage_lengths)):
            length = percentage_lengths[x] / 100.0 * self.length
            if length == tkinter_qu.NONE:
                length = default_length

            height = percent_heights[x] / 100.0 * self.height
            if height == tkinter_qu.NONE:
                height = default_height

            self.components[x].number_set_dimensions(current_left_edge, current_top_edge, length, height)

            # There is a contract that the total percent lengths and heights will be less than or equal to 100 if
            # the stack is cumulative (one item after another). Otherwise, the values will not increase
            if total_percent_heights <= 100:
                current_top_edge += height

            if total_percent_lengths <= 100:
                current_left_edge += length

    def get_total_percentages(self, percentages):
        """
            Returns:
                list[float]: The total percentages of the list (tkinter_qu.NONE is not counted)
        """

        return_value = 0

        for x in range(len(percentages)):
            if percentages[x] != tkinter_qu.NONE:
                return_value += percentages[x]

        return return_value


    @abc.abstractmethod
    def percentage_set_component_dimensions(self, percentages):
        """Sets the dimensions of the components using the percentages. tkinter_qu.None means evenly divide on remaining space."""

        pass







