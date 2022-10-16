python hook机制

https://zhuanlan.zhihu.com/p/275643739

半个小时学会pytorch

https://www.cnblogs.com/sddai/p/14412250.html

示例代码一：

```python
import time

class LazyPerson(object):
    def __init__(self, name):
        self.name = name
        self.watch_tv_func = None # 目标挂载点
        self.have_dinner_func = None

    def get_up(self):
        print("%s get up at:%s" % (self.name, time.time()))

    def go_to_sleep(self):
        print("%s go to sleep at:%s" % (self.name, time.time()))

    def register_tv_hook(self, watch_tv_func): # 挂接
        self.watch_tv_func = watch_tv_func

    def register_dinner_hook(self, have_dinner_func):
        self.have_dinner_func = have_dinner_func

    def enjoy_a_lazy_day(self):
        self.get_up()
        time.sleep(2)
        # watch tv  --> check the watch_tv_func(hooked or unhooked) --> hooked
        if self.watch_tv_func is not None:
            self.watch_tv_func(self.name)
        else: # unhooked
            print("no tv to watch")

        time.sleep(2)
        # have dinner --> check the have_dinner_func(hooked or unhooked) --> hooked
        if self.have_dinner_func is not None:
            self.have_dinner_func(self.name)
        else: # unhooked
            print("nothing to eat at dinner")

        time.sleep(2)
        self.go_to_sleep()

def watch_daydayup(name): # hook函数
    print("%s : The program ---day day up--- is funny!!!" % name)

def watch_happyfamily(name):
    print("%s : The program ---happy family--- is boring!!!" % name)

def eat_meat(name):
    print("%s : The meat is nice!!!" % name)

def eat_hamburger(name):
    print("%s : The hamburger is not so bad!!!" % name)


def test():
    lazy_tom = LazyPerson("Tom")
    lazy_jerry = LazyPerson("Jerry")

    # register hook
    lazy_tom.register_tv_hook(watch_daydayup)
    lazy_tom.register_dinner_hook(eat_meat)

    lazy_jerry.register_tv_hook(watch_happyfamily)
    lazy_jerry.register_dinner_hook(eat_hamburger)

    # enjoy a day
    lazy_tom.enjoy_a_lazy_day()
    lazy_jerry.enjoy_a_lazy_day()

test()						
	
```

示例代码二pytoch（计算中间值）：

```python
ef register_hook(module):
        def hook(module, input, output):
            class_name = str(module.__class__).split(".")[-1].split("'")[0]
            module_idx = len(summary)

            m_key = "%s-%i" % (class_name, module_idx + 1)
            summary[m_key] = OrderedDict()
            summary[m_key]["input_shape"] = list(input[0].size())
            summary[m_key]["input_shape"][0] = batch_size
            if isinstance(output, (list, tuple)):
                summary[m_key]["output_shape"] = [
                    [-1] + list(o.size())[1:] for o in output
                ]
            else:
                summary[m_key]["output_shape"] = list(output.size())
                summary[m_key]["output_shape"][0] = batch_size

            params = 0
            if hasattr(module, "weight") and hasattr(module.weight, "size"):##weight params
                params += torch.prod(torch.LongTensor(list(module.weight.size())))
                summary[m_key]["trainable"] = module.weight.requires_grad
            if hasattr(module, "bias") and hasattr(module.bias, "size"):
                params += torch.prod(torch.LongTensor(list(module.bias.size())))#bias params
            summary[m_key]["nb_params"] = params

        if (
            not isinstance(module, nn.Sequential)
            and not isinstance(module, nn.ModuleList)
        ):
            hooks.append(module.register_forward_hook(hook))

```

