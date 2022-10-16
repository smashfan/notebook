### pytorch中children()modules()，named_children()，named_modules()，named_parameters()，parameters()的使用

children()：返回包含直接子模块的迭代器

modules()：（递归）返回包含所有子模块（直接、间接）的迭代器

named_children() ：返回包含直接子模块的迭代器，同时产生模块的名称以及模块本身

named_modules()：返回包含所有子模块（直接、间接）的迭代器，同时产生模块的名称以及模块本身

[named_parameters](https://www.zhihu.com/search?q=named_parameters&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"article"%2C"sourceId"%3A"360398070"})()：返回模块参数上的迭代器，产生参数的名称和参数本身

parameters()： 返回模块参数上的迭代器，不包括名称（参考上）