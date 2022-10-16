from setuptools import setup
setup(
    name='NN Parser',
    url='https://github.com/jladan/package_demo',
    author='Li Liu',
    author_email='lliu@birentech.com',
    packages=['NNParser'],
    # Needed for dependencies
    install_requires=['numpy','pandas','matplotlib','openpyxl','scikit-learn',
    'scikit-image',	'graphviz','python-graphviz','pydot'],
    version='0.5',
    license='MIT',
    description='The tool was built for AI hardware/ software architectures'
     ' to quickly understand and analyze the overall and layer-wise structure '
     ' of neural network models.',
)
