### 什么是Type Hint

​	

```
https://zhuanlan.zhihu.com/p/519335398
```

Python 作为动态类编程语言，在定义变量时不需要预声明变量类型，这一特性为编程带来便利的同时，也引入了一些问题（例如代码可读性变差，容易引发各种各样的 TypeError）。为了解决这些问题，Python 3.5 引入了 [typing ](https://link.zhihu.com/?target=https%3A//docs.python.org/3/library/typing.html)模块，并在 [PEP 483](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0483/) 和 [PEP 484](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0484/) 进一步介绍了如何进行 Type Hints（类型提示）。**今天我们就一起来学习使用 Type Hints，让代码更加规范整洁。**

### 1. 增加代码可读性

要知道，我们阅读的代码数远远要多于我们写过的代码数，有了参数的类型信息，理解和维护代码库将会变得更加容易。例如：

```python
def add(a, b): 
    return a + b 
```

只看代码，你完全不知道应该传入什么类型的参数，来获得符合预期的结果（这里的 add 只是非常简单的例子，实际工程中可能函数实现非常复杂，只有传入了正确的类型才能获得正确的结果）。如果我们加上了 Type Hints：

```python
def add(a: int, b: int): 
    return a + b 
```

那么只看函数签名，我们就能知道传入的参数类型。

### 2. 帮助代码补全或函数跳转

我们在 IDE 里写代码时，经常会使用 Tab 来补全**类方法**，而这个功能，也是借助 Type Hints 实现的。假设我们想实现将两个 `np.ndarray` 变量相加的函数：

```python
def np_add(a, b): 
    c = a + b 
    return c.sum() 
```

这个时候我们会发现，c.sum() 这个函数是无法自动补全/跳转的，因为我们无法推导出 c 的类型，自然也无法补全 c 的方法。

![img](https://pic3.zhimg.com/80/v2-241c18a8a37fd055b01dbe4cec760dc2_720w.jpg)

上图为 vscode 展示的效果（真的是 vscode，JetBrain 主题 (●'◡'●)），vscode 插件推导 sum 的类型为 Any，自然没法补全、跳转代码。如果我们补上 Type Hints：

```python
def np_add(a: np.ndarray, b: np.ndarray): 
    c = a + b 
    return c.sum() 
```

此时 sum 方法既能够补全，也能够跳转。

![img](https://pic4.zhimg.com/80/v2-c5bca78769969b4fb784c878413b5b07_720w.png)

vscode 就能解析 ndarray.sum() 的函数签名了。

### 3. 在 vscode 中自动生成 docstring

有了 Type Hints，生成 docstring 也会变得简单。安装 autoDocstring 插件：

![img](https://pic4.zhimg.com/80/v2-02a6366d7560c7a91fc9a2fac2a2563b_720w.png)

写 docstring 时会有以下提示：

![img](https://pic3.zhimg.com/80/v2-6173911400518bbe37af801a69d8484e_720w.jpg)

一键生成 docstring：

![img](https://pic1.zhimg.com/80/v2-05a2283870d6817d53eae70df420d28c_720w.jpg)

利用 Type Hints 生成 docstring 可以大大减少 docstring 的工作量（Pycharm 党的哀嚎，不会自动补全 docstring 里的变量类型）

### 4. 增加代码鲁棒性

Type Hints 仅仅是类型提示，对变量类型没有强制性要求。换句话说，我们给函数传入和 Type Hints 不一致的变量类型，程序也不会因此而报错。为了让 Python 代码能够像 C/C++ 一样对类型做静态检查（类型不符合就报错），可以使用 mypy + Type Hints 来检查我们的代码。

```python
import numpy as np 
 
def np_add(a: np.ndarray, b: np.ndarray): 
    return a + b 
 
np_add(1, 2) 
```

上述代码调用 np_add 时，传入了类型不符的变量，使用 mypy 对其进行类型检查：

```python
mypy learn_type_hint.py 
learn_type_hint.py:8: error: Argument 1 to "np_add" has incompatible type "int"; expected "ndarray[Any, Any]" 
learn_type_hint.py:8: error: Argument 2 to "np_add" has incompatible type "int"; expected "ndarray[Any, Any]" 
```

执行 pre-commit 时，mypy 运行在独立的虚拟环境中，并没有你当前环境的依赖，因此无法对三方库的类型做检查。当你在本地环境执行 mypy 时，会导入三方库的 Type Hints，mypy 的类型检查会更加的严格。如果你想使用单独使用 mypy 检查某个文件，并得到和 pre-commit 相同的检查效果，则需要新建一个空的 python 环境，在空环境里执行 mypy。

综上，使用 Type Hints 的主要目的就是为了引入静态类型检查，增加一道防线，及早发现 bug 提高代码的鲁棒性。

## 基本用法

### 1. Type Hints 基本类型

对于 int、float、str 类型的 Python 内置类型，可以直接使用类型本身来写 Type Hints：

```python
# 声明类型 + 定义 
a: int = 1 
# 先声明 
b: int 
# 后定义 
b = 1 
# 函数中的 typehint, 输出类型用 -> 连接 
def foo(a: int, b: int=1) -> int: 
    return a + b 
# str 类型的 Type Hints 
repo: str = 'mmcv' 
# float 类型的 Type Hints  
value: float = 0.1 
```

### 2. 复合型的 Type Hints

对于 list、tuple、dict 等容器类的实例，我们也可以用内置类型的 Type Hints：

```python
info: dict = dict(a=1, b=2)  # 等价于 Dict[Any, Any] 
element: list = [1]  # 等价于 List[Any] 
```

上述写法仅声明了变量本身的类型是 `list`/`dict`，而变量中的元素可以是任意类型（Any）。如果想进一步约束容器中元素的类型，则需要引入 typing 模块的 Dict 和 List：

```python
from typing import List， Tuple, Dict 
int_list: List[int] = [1, 2] 
int_tuple: Tuple[int] = (1, 2) 
str_int_dict: Dict[str, int] = dict(name="lisa") 
```

如果变量可能是多种类型，则需要引入 Union：

```python
from typing import Union 
int_or_float: Union[int, float] = 1 
int_or_float = 0.5 
```

Optional 类来声明默认值为 None 的实例：

```python
from typing import Optional 
default_none: Optional[str] = None 
```

复杂一点的例子：

```python
from typing import Optional， Union 
name: Optional[Union[int, float]] = None 
```

如果变量的类型是生成器/迭代器，则需要导入容器类 Generator/Iterator，其写法和 List、Dict 相同：

```python
from typing import Generator, Iterator 
# generator 接受一个迭代器参数，函数会返回一个生成器 
def generator(iterator: Iterator[int]) -> Generator[int, None, None]: 
    for element in iterator: 
        yield element 
```

### 3. Type Hints 别名

有些变量类型的 Type Hints 过于复杂，直接在函数中声明会影响接口的可读性，因此可以重命名特定的变量类型：

```python
complex_type = Optional[Union[List[int], int]] 
 
def foo(comlex_arg: complex_type = None) -> None: 
    pass 
```

### 4. 函数类型的 Type Hints

可以使用 `Callable` 来声明函数类型的变量。直接使用 `Callable` 表示函数接受任意个数、任意类型的参数，并返回任意个数、任意类型的变量。如果想进一步约束函数入参和返回值类型，可以使用 `Callable[[Arg1Type, Arg2Type], ReturnType]`：

```text
from typing import Callable 
 
def foo(a: int, b: int) -> int: 
    return a + b 
 
# 不声明参数和返回值类型 
def register_callback2(func: Callable) 
    pass 
 
# 声明入参类型和返回类型。入参为 （int, int），返回值类型为 int 
def register_callback1(func: Callable[[int, int], int]): 
    pass 
```

### 5. Type Hints 对应的 docstring

- 参数有非 None 类型的默认值。直接在对应的 args 末尾加 `Defaults to xxx` 即可：

```python
def hello(name: str = 'heihei') -> None: 
 """Say hello to someone. 
 
    Args: 
 name (str): name of people. Defaults to "heihei". 
    """ 
```

- 参数有默认值，默认值为 None。此时（）内写（str, optional），且无需追加 `Defaults to xxx`：

```python
def hello(name: str = None) -> None: 
 """Say hello to someone. 
 
    Args: 
 name (str, optional): name of people. 
    """ 
 print(f'hello {name} ~') 
```

- 参数可能是多种类型。可以写作 `（str or List[str]）`或者 `（str | List[str]）`：

```python
def hello(name: Uninon[List[str], str]): 
 """Say hello to someone. 
 
    Args: 
        name (str or List[str]): name of people. 
    """ 
 print(f'hello {name} ~') 
```

- 参数可能是多种类型，且默认值为 None。可以写作 `(str or List[str], optional)`：

```python
def hello(name: Uninon[List[str], str] = None) - None: 
 """Say hello to someone. 
 
    Args: 
 name (str or List[str], optional): name of people. 
    """ 
 print(f'hello {name} ~') 
```

以上四种情况覆盖了大部分的 args 类型。

给代码添加了 Type Hints 后，我们就可以用 mypy 对其进行更加准确的静态检查了。接下来，我们和大家一起来认识一下 mypy。

## mypy 介绍

mypy 是一种静态检查工具，可以帮助我们像静态语言一样在运行代码之前捕捉到一些错误。

> mypy 配置项：[https://mypy.readthedocs.io/en/stable/config_file.html](https://link.zhihu.com/?target=https%3A//mypy.readthedocs.io/en/stable/config_file.html)
> 常见问题汇总： [Common issues and solutions - mypy 0.950 documentation](https://link.zhihu.com/?target=https%3A//mypy.readthedocs.io/en/stable/common_issues.html%23variables-vs-type-aliases)

### 类型推导规则

1.mypy 会对内置类型的表达式，做类型推导：

```python
a = 1 
b = []  # Need type annotation for "b" (hint: "b: List[<type>] = ...") 
a + b  # Unsupported operand types for + ("int" and "List[Any]") 
```

上述代码 mypy 会报两个错误：

- **空列表** b 需要预声明变量类型，应该写作 `b: list = []`
- list 和 int 类型的数据不能相加

2.源码实现/三方库的类型推导

mypy 可以根据我们源码中的 Type Hints，做类型推导：

```python
class MyClass: 
    def foo(self): 
        pass 
 
 
def get_my_class() -> MyClass: 
    return MyClass() 
 
 
instance = get_my_class() 
instance.foo() 
instance.unknown()  # error: "MyClass" has no attribute "unknown" 
```

mypy 能够检查出 instance 的类型是 `MyClass`，进而检查出第 12 行访问了不存在的属性。

虚拟环境中 mypy 不会对三方库的类型的做检查：

```python
import numpy as np 
 
array = np.array([1]) 
array.unknown() 
```

mypy 默认 array 的类型为 Any，可以访问其任意属性。

3.函数参数的类型推导

函数入参即使有默认值，mypy 也不会推断其类型，默认类型为 Any：

```python
class MypyDemo: 
 
    def __init__(self, parent='parent'): 
        self.get_value(parent) 
    # 尽管 parent 的默认类型和 i 的变量类型不匹配，仍然能够通过静态检查 
    def get_value(self, value: int): 
        return value 
```

如果我们给 parent 加上 Type Hints，mypy 就会报错：

```python
class MypyDemo: 
 
    def __init__(self, parent: str = 'parent'): 
        self.get_value(parent) 
 
    def get_value(self, i: int): 
        return i 
# error: Argument 1 to "get_value" of "MypyDemo" has incompatible type "str"; expected "int" 
```

### 常见问题

**1.变量类型改变引起的报错**

示例如下：

```python
def parse_data(data: list): 
    data = torch.stack(data) 
    return data 
```

这段代码是无法通过 mypy 检查的。入参 data 有 Type Hints，类型为 list，而 mypy 不允许复写变量类型。因此最好的解决方案是重命名变量：

```python
# 正确 
def parse_data(data: list): 
    batch_data = torch.stack(data) 
    return batch_data 
```

此外，我们也不应该复写 mypy 推导得到的变量类型：

```python
def my_func(condition) -> dict: 
    result = {'success': False} 
 
    if condition: 
        result['success'] = True 
        return result 
    else: 
        result['message'] = 'error message' 
    return result 
# error: Incompatible types in assignment (expression has type "str", target has type "bool") 
```

mypy 推导得到的 results 类型为 `Dict[str, bool]`，而第 8 行复写为 `Dict[str, str]`，无法通过 mypy 检查。解决方案是预定义变量类型 :

```python
def my_func(condition) -> dict: 
 result: Dict[str, Union[str, bool]] = {'success': False} 
 
    if condition: 
        result['success'] = True 
        return result 
    else: 
        result['message'] = 'error message' 
    return result 
```

**2.入参类型不匹配**

对于某些变量，例如字典。写代码的人可能知道每个 key 对应的 value 是什么类型的，就可能会写出这样的代码：

```python
from typing import Dict, Union 
 
def count_chars(string) -> Dict[str, Union[str, bool, int]]: 
    result = {}  # type: Dict[str, Union[str, bool, int]] 
 
    if not isinstance(string, str): 
        result['success'] = False 
        result['message'] = 'Inavlid argument' 
    else: 
        result['success'] = True 
        result['result'] = len(string) 
    return result 
 
def get_square(integer: int) -> int: 
    return integer * integer 
 
def validate_str(string: str) -> bool: 
    check_count = count_chars(string) 
    if not check_count['success']: 
        print(check_count['message']) 
        return False 
    str_len_square = get_square(check_count['result']) 
    return bool(str_len_square > 42) 
 
result = validate_str("Lorem ipsum") 
```

根据第 11 行和第 22 行我们知道 `check_count["result"]` 返回的类型为 int，是符合 `get_square` 的函数签名的。然而 mypy 是无法判断 `check_count["result"]` 的类型的。对 mypy 而言，get_square 接收的参数类型是 `Union[str, bool, int]`，因此报错。

对于这种情况，我们通常有 2 种解决方案：

- **类型窄化**（[Type narrowing - mypy 0.950 documentation](https://link.zhihu.com/?target=https%3A//mypy.readthedocs.io/en/stable/type_narrowing.html)）

使用 isinstance 和 assert 对 **check_count["result"]** 做类型限定。

```python
def validate_str(string: str) -> bool: 
    check_count = count_chars(string) 
    if check_count['success'] is False: 
        print(check_count['message']) 
        return False 
    assert isinstance(check_count['result'], int) 
    str_len_square = get_square(check_count['result']) 
    return bool(str_len_square > 42) 
```

mypy 会识别第六行代码，判断 check_count['result'] 的类型为 int。 因此在检查到第 7 行时不会报错。

- **类型忽视**

在某行代码的末尾加上 `# type ignore`，mypy 就不会检查这行代码了。要慎重使用 `# type ignore`，只有在 mypy 静态检查不合理时才使用它。

```python
def validate_str(string: str) -> bool: 
    check_count = count_chars(string) 
    if check_count['success'] is False: 
        print(check_count['message']) 
        return False 
    str_len_square = get_square(check_count['result'])  # type: ignore 
    return bool(str_len_square > 42) 
```