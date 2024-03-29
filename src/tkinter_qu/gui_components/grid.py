from math import ceil, floor

from tkinter_qu.base.important_variables import SCREEN_LENGTH, SCREEN_HEIGHT
from tkinter_qu.base.utility_functions import get_measurement
from tkinter_qu.gui_components.dimensions import Dimensions


class Grid(Dimensions):
    """Provides an easy way to put components into a grid"""

    rows = None
    columns = None
    length_buffer = get_measurement(SCREEN_LENGTH, 1)
    height_buffer = get_measurement(SCREEN_HEIGHT, 1)
    goes_top_to_bottom = True
    goes_left_to_right = True

    def __init__(self, dimensions, rows, columns, goes_top_to_bottom=True, goes_left_to_right=True):
        """ Initializes the object | IMPORTANT - columns and rows can't both be None

            Args:
                dimensions (Dimensions): the left_edge, top_edge, length, and height of the grid
                rows (int): the max amount of rows the grid can have (can be None)
                columns (int): the max amount of columns the grid can have (can be None)
                goes_top_to_bottom (bool): if the components of the grid start at the top and go down (start at bottom if False)
                goes_left_to_right (bool): if the components of the grid start at the left and go right (start at right if False)

            Returns:
                None
        """

        super().__init__(*dimensions.get_values())
        self.rows, self.columns = rows, columns
        self.goes_top_to_bottom, self.goes_left_to_right = goes_top_to_bottom, goes_left_to_right

    def turn_into_grid(self, items, item_max_length=None, item_max_height=None, component_stretching_is_allowed=True):
        """ Turns all the items into a grid format

            Args:
                items (list[Component]): the items that will be converted into a grid
                item_max_length (int): the max length that an item can be (None means there is no max length)
                item_max_height (int): the max height than an item can be (None means there is no max height)
                component_stretching_is_allowed (bool): whether the component has to be scaled by a specific value
                before it is rendered (instead of having uneven scales causing stretching)

            Returns:
                None
        """

        rows, columns = self.rows, self.columns
        number_of_items = len(items)

        # If there are no items, then nothing can be turned into a grid
        if number_of_items == 0:
            print("WARNING: the length of items was 0 for the Grid.turn_into_grid() method")
            return

        if rows is None:
            rows = self.get_grid_dimension(columns, number_of_items)

        if columns is None:
            columns = self.get_grid_dimension(rows, number_of_items)

        item_height = self.get_item_dimension(self.height, rows, item_max_height, self.height_buffer)
        item_length = self.get_item_dimension(self.length, columns, item_max_length, self.length_buffer)

        base_left_edge = self.left_edge if self.goes_left_to_right else self.right_edge - item_length
        base_top_edge = self.top_edge if self.goes_top_to_bottom else self.bottom_edge - item_height

        for x in range(number_of_items):
            column_number = x % columns
            row_number = floor(x / columns)

            left_edge = base_left_edge + self.get_dimension_change(column_number, item_length, self.length_buffer)
            top_edge = base_top_edge + self.get_dimension_change(row_number, item_height, self.height_buffer)

            current_item_length = item_length
            current_item_height = item_height

            if not component_stretching_is_allowed:
                current_item_length, current_item_height = items[x].get_scaled_dimensions(item_length, item_height)

            items[x].number_set_dimensions(left_edge, top_edge, current_item_length, current_item_height)

    def get_grid_dimension(self, other_dimension, number_of_items):
        """ Finds the number of either rows or columns there should be depending on the value of 'other_dimension' (ceil(number_of_items / other_dimension)

            Args:
                other_dimension (float): the grid dimension (number of rows or columns) other than the one that will be returned
                number_of_items (int): The number of items in the grid

            Returns:
                float: either the number of rows or columns depending on the value of 'other_dimension'"""

        return ceil(number_of_items / other_dimension)

    def get_item_dimension(self, grid_dimension_size, grid_dimension, item_dimension_max, buffer_between_items):
        """ Finds the size of the item that is in 'grid_dimension'- height for rows and length for columns

            Args:
                grid_dimension_size (float): the grid's height if the grid item height is wanted and grid's length if the grid item length is wanted
                grid_dimension (int): the grid's number of rows if the grid item height is wanted and grid's number of columns if the grid item length is wanted
                item_dimension_max (float): the max value this function can return
                buffer_between_items (float): the number of pixels between adjacent items

            Returns:
                float: the size of the item that is in 'grid_dimension'- height for rows and length for columns"""

        remaining_dimension = grid_dimension_size - buffer_between_items * (grid_dimension - 1)

        item_dimension = remaining_dimension / grid_dimension

        if item_dimension_max is not None and item_dimension > item_dimension_max:
            item_dimension = item_dimension_max

        return item_dimension

    def get_dimension_change(self, grid_dimension, item_dimension, buffer_between_items):
        """ The amount of pixels that are after the first grid item in the 'grid_dimension'

            Args:
                grid_dimension (int): rows if the grid item delta top_edge is wanted and columns if grid item delta left_edge is wanted
                item_dimension (float): the height of the grid item if delta top_edge is wanted and length of the grid item if delta left_edge is wanted
                buffer_between_items (float): the number of pixels between adjacent items

            Returns:
                float: the amount of pixels that are after the first grid item in the 'grid_dimension'"""

        dimension_change_amount = grid_dimension * (item_dimension + buffer_between_items)

        # If it starts at the top then the top_edge increases, but if it doesn't then the top_edge decreases
        return dimension_change_amount if self.goes_top_to_bottom else -dimension_change_amount