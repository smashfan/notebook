#https://github.com/TylerYep/torch-summary
""" formatting.py """
import math
from enum import Enum, unique
from typing import Dict, List, Sequence
from .layer_info import LayerInfo


@unique
class Verbosity(Enum):
    """ Contains verbosity levels. """

    QUIET, DEFAULT, VERBOSE = 0, 1, 2


class FormattingOptions:
    """ Class that holds information about formatting the table output. """

    def __init__(
        self,
        use_branching: bool,
        max_depth: int,
        verbose: int,
        col_names: Sequence[str],
        col_width: int,
    ):
        self.use_branching = use_branching
        self.max_depth = max_depth
        self.verbose = verbose
        # col_names is a Sequence, e.g. tuple, of str
        # i.e. input_size, kernel_size, pad_size, gemm, vect, acti, etc.
        self.col_names = col_names
        # col_width controls Excel cell width
        self.col_width = col_width
        self.layer_name_width = 40

    def set_layer_name_width(self, summary_list: List[LayerInfo], align_val: int = 5) -> None:
        """ Set layer name width by taking the longest line length and rounding up to
        the nearest multiple of align_val. """
        max_length = 0
        for info in summary_list:
            depth_indent = info.depth * align_val + 1
            max_length = max(max_length, len(str(info)) + depth_indent)
        if max_length >= self.layer_name_width:
            self.layer_name_width = math.ceil(max_length / align_val) * align_val

    def get_total_width(self) -> int:
        """ Calculate the total width of all lines in the table. """
        return len(self.col_names) * self.col_width + self.layer_name_width

    def format_row(self, layer_name: str, row_values: Dict[str, str]) -> str:
        """ Get the string representation of a single layer of the model. """
        # based on the order of self.col_names
        info_to_use = [row_values.get(row_type, "") for row_type in self.col_names]
        # new_line = "{:<{}} ".format(layer_name, self.layer_name_width)
        new_line = f"{layer_name}, "
        for info in info_to_use:
            if isinstance(info,(list,tuple)):
                for item in info:
                    new_line += f"{item}, "
            else:
                new_line += f"{info}, "
        return new_line.rstrip() + "\n"