""" model_statistics.py """
from .layer_info import *
from .formatting import FormattingOptions, Verbosity

HEADER_TITLES = {
    "kernel_size": "Kernel Shape",
    # "input_size": "Input Shape",
    "output_size": "Output Shape",
    "num_params": "Param #",
    "mult_adds": "Mult-Adds",
}
CORRECTED_INPUT_SIZE_TYPE = List[Union[Sequence[Any], torch.Size]]


class ModelStatistics:
    """ Class for storing results of the summary. """

    def __init__(
        self,
        summary_list: List[LayerInfo],
        input_size: CORRECTED_INPUT_SIZE_TYPE,
        formatting: FormattingOptions,
        ucfg:{},
    ):
        self.summary_list = summary_list
        self.input_size = input_size
        self.total_input = sum([abs(np.prod(sz)) for sz in input_size])
        self.formatting = formatting
        self.total_params = 0
        self.trainable_params = 0
        self.total_output = 0
        self.total_mult_adds = 0
        # input batch size and BPE, captured from command line
        self.bs = ucfg['batchsize']
        self.bpe = ucfg['BPE']


    @staticmethod
    def to_bytes(num: int) -> float:
        """ Converts a number (assume floats, 4 bytes each) to megabytes. """
        assert num >= 0
        return num * 4 / (1024 ** 2)

    @staticmethod
    def to_readable(num: int) -> float:
        """ Converts a number to millions or billions. """
        # ? What about unit?
        assert num >= 0
        if num >= 1e9:
            return num / 1e9
        return num / 1e6

    def __repr__(self) -> str:
        """ Print results of the summary. """
        # header_row = self.formatting.format_row("Layer (type:depth-idx)", HEADER_TITLES)
        return "{}".format(self.layers_to_str())

    def layer_info_to_row(self, layer_info: LayerInfo, reached_max_depth: bool = False) -> str:
        """ Convert layer_info to string representation of a row. """

        def get_start_str(depth: int) -> str:
            return "├─" if depth == 1 else "|    " * (depth - 1) + "└─"

        def get_start_comma(depth: int) -> str:
            return "" if depth == 1 else "," * (depth - 1)

        row_values = {
            "input_size": layer_info.input_size[1:] if len(layer_info.input_size)==4 else layer_info.input_size[1:]+(['']*(4-len(layer_info.input_size))), # multiple in?
            "output_size": layer_info.output_size[1:] if len(layer_info.output_size)==4 else layer_info.output_size[1:]+(['']*(4-len(layer_info.output_size))),
            "num_in": np.prod(layer_info.input_size[1:]) * self.bs * self.bpe,
            "num_out": np.prod(layer_info.output_size[1:]) * self.bs * self.bpe,
            "num_params": layer_info.num_params * self.bs * self.bpe if layer_info.num_params else '',
            "mult_adds": layer_info.macs if layer_info.macs else '',
            "kernel_size": layer_info.kernel_size[2:] if len(layer_info.kernel_size)>2 else ['',''],
            "pad_size": layer_info.pad_size if layer_info.pad_size else ['',''],
            "stride_size": layer_info.stride_size if layer_info.stride_size else ['',''],
            # batch size and bpe
            "gemm": layer_info.gemm * self.bs if layer_info.gemm else [''],
            "vect": layer_info.vect * self.bs if layer_info.vect else [''],
            "acti": layer_info.acti * self.bs if layer_info.acti else [''],
            'gemmB': layer_info.gemmB * self.bs if layer_info.gemmB else [''],
            'vectB': layer_info.vectB * self.bs if layer_info.vectB else [''],
            'actiB': layer_info.actiB * self.bs if layer_info.actiB else [''],
        } # list instead of string

        depth = layer_info.depth
        if self.formatting.use_branching==1: # for 3 cases
            name = get_start_str(depth) + str(layer_info)
        elif self.formatting.use_branching==2:
            name = get_start_comma(depth) + str(layer_info) + "," * (self.formatting.max_depth-depth)
        else:
            name ='' + str(layer_info)
        new_line = self.formatting.format_row(name, row_values)
        if self.formatting.verbose == Verbosity.VERBOSE.value:
            for inner_name, inner_shape in layer_info.inner_layers.items():
                prefix = get_start_str(depth + 1) if self.formatting.use_branching else "  "
                extra_row_values = {"kernel_size": str(inner_shape)}
                new_line += self.formatting.format_row(prefix + inner_name, extra_row_values)
        return new_line

    def layers_to_str(self) -> str:
        """ Print each layer of the model as tree or as a list. """
        if self.formatting.use_branching:
            lines = self._layer_tree_to_str()
            lincnt = lines.count('\n')
            # to handle ModuleList
            if lincnt < len(self.summary_list):
                lines += self._layer_tree_to_str(lincnt, len(self.summary_list), 2)
            return lines

        layer_rows = ""
        for layer_info in self.summary_list:
            layer_rows += self.layer_info_to_row(layer_info)
        return layer_rows

    def _layer_tree_to_str(self, left: int = 0, right: Optional[int] = None, depth: int = 1) -> str:
        """ Print each layer of the model using a fancy branching diagram. """
        if depth > self.formatting.max_depth:
            return ""

        new_left = left - 1
        new_str = ""
        if right is None:
            right = len(self.summary_list)
        for i in range(left, right):
            layer_info = self.summary_list[i]
            if layer_info.depth == depth:
                # print(i,left,right)
                reached_max_depth = depth == self.formatting.max_depth
                new_str += self.layer_info_to_row(layer_info, reached_max_depth)
                new_str += self._layer_tree_to_str(new_left + 1, i, depth + 1)
                new_left = i
        return new_str