

**bug1：**UserWarning: Named tensors and all their associated APIs are an experimental feature and subject to change. Please do not use them for anything important until they are released as stable. (Triggered internally at ..\c10/core/TensorImpl.h:1156.) return torch.max_pool2d(input, kernel_size, stride, padding, dilation, ceil_mode)

解决办法：
这是pytorch1.9的bug，下个版本将修复，我将pytorch降级成1.8就不报这个错了。
