#  Install Virtual Environment

# Option A: With Anaconda

​	It's recommended to run the tool on a virtual environment. Installation using Anaconda is demonstrated below.

## 1. Install Anaconda

1.1. Download the latest 'anaconda' compatible  to the OS, and install it

​		The package can be downloaded from the [official site](https://www.anaconda.com/products/individual) or a [mirror site](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

1.2. Set a local mirror source (optional)

​		If it is inconvenient to access the official site,  a local mirror source can be added. For example, the mirror site from colleges,

​		https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/

​		One can set the source channel by adding the source links into '.condarc' which is under the system's user folder. For windows OS, the file is usually at 'C:\Users\xxx', where 'xxx' is the login user name.



## 2. Create a virtual environment

Launch the anaconda command windows, in the window,

2.1. Create a environment by:

​			`conda create nnp`

2.2. enter the environment

​			`conda activate nnp`

2.3. install the python package

​			`conda install xx`

​		where xx is the package name. The following packages are required for the tool:

​		Python 3.6+, 	Tensorflow 2.1 +,  Pytorch 1.5+

    pandas,​ numpy,​ matplotlib,​ openpyxl, scikit-learn, scikit-image, graphviz, python-graphviz, pydot

2.4 other packages

​	pip tool can be used to install packages under the activated virtual environment. For example,

​			`pip3 install keras-bert`

​	Similar to the conda, a [pip mirror site](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) can be used to accelerate the installation.




# Option B: Without Anaconda

## 1. Install Virtual Environment with python-venv (e.g. in Linux System)
[Python venv doc](https://docs.python.org/3/tutorial/venv.html) shows the command template as `python3 -m venv env_name`, make sure your Python is at least 3.3 for `venv` to work.
After installation, activate it by typing `source env_name/bin/activate`

## 2. Install Miscellaneous Required Packages
In your virtual env, type `pip3 install module_name` to install all desired modules. Typically, you would need to install `pandas numpy matplotlib openpyxl scikit-learn scikit-image graphviz pydot`. (And of course, `tensorflow torch torchvision` etc.)

For example, we have tested a virtual env with Python 3.8.2, pytorch 1.6.0 etc., a full list of module is saved in [req_wo_anaconda.txt](https://github.com/BirenResearch/NNparser/blob/master/req_wo_anaconda.txt).

NOTE: You may find it failed to generate Network Graph, that's because, as mentioned in issue ["No module named pydot"](https://stackoverflow.com/questions/35177262/importerror-no-module-named-pydot-unable-to-import-pydot) and ["Failed to import pydot"](https://stackoverflow.com/questions/36886711/keras-runtimeerror-failed-to-import-pydot-after-installing-graphviz-and-pyd), "graphviz package is just a python wrapper, and the graphviz binaries have to be installed separately for the python wrapper to work." One can fix this by simply following the instructions described [here](https://graphviz.gitlab.io/download/). (For example, in Ubuntu, type in `sudo apt install graphviz`.)
