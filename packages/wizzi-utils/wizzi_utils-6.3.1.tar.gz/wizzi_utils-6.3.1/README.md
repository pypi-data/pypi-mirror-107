# Package wizzi utils:  
## Installation: 
```bash
pip install wizzi_utils 
```
## Usage
```python
import wizzi_utils as wu # imports all that is available
print(wu.__version__) 
wu.test_all_modules()  # run all tests in all 8 modules
```
* The above import will give you access to all functions and tests in wizzi_utils.<br/>
* For convenience, the wizzi_utils imports all it can from the sub modules, therefore
only the one import above is enough.
* Every function is covered by a test(usually the 'func_name'_test()). Use this to see how the 
function works and also to copy paste the signature.
```markdown
from wizzi_utils import algorithms as algs
from wizzi_utils import coreset as cot
from wizzi_utils import json as jt
from wizzi_utils import open_cv as cvt
from wizzi_utils import pyplot as pyplt
from wizzi_utils import socket as st
from wizzi_utils import torch as tt
from wizzi_utils import tensorflow as tft
from wizzi_utils import tflite as tflt
```

###  misc_tools & misc_tools_test
'pip install wizzi_utils' made sure you'll have everything needed installed so they should be fully working,
so there is no namespace for misc_tools module(direct access from wu)<br/>
```python
import wizzi_utils as wu

# all functions in misc_tools & misc_tools_test are imported to wizzi_utils
print(wu.to_str(var=2, title='my_int'))  # notice only wu namespace

# direct access to the misc_tools module  
print(wu.misc_tools.to_str(var=2, title='my_int'))  # not needed but possible

wu.test.test_all()  # runs all tests in misc_tools_test.py
wu.test.to_str_test()  # runs only to_str_test
```

### All other modules
Other modules, e.g. torch_tools, will work only if you have all the dependencies written in the init file of the module.  
* In torch_tools example, the dependencies are written here:  
wizzi_utils.torch.\_\_init__.py # for the tools  
wizzi_utils.torch.test.\_\_init__.py # for the tests and examples  

```python
import wizzi_utils as wu

# if we want torch tools: we need torch, torchvision  
# access to a function in the torch module  
print(wu.tt.to_str(var=3, title='my_int')) # notice wu and tt namespaces. tt for torch tools
  
# access to a function in the matplotlib module - same rules as torch example above  
print(wu.pyplt.get_RGB_color(color_str='r'))
  
# access to a module test  
wu.algs.test.test_all()  # all tests in algorithm module
wu.pyplt.test.plot_3d_iterative_dashboard_test() # specific test in pyplot module
```  
      
      
    