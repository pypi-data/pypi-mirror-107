# The Calculation Manager Interface
This file defines the interface for the Calculation Manager


# WOW-bug in grpcio-tools compiler --- "protoc".
it genrates 
import calculation_manager_pb2 as calculation__manager__pb2
Unfortunately, this style of relative path does not work in python3, only works in python2
For now the fix is literally to change the auto generated file manually like so:
from . import calculation_manager_pb2 as calculation__manager__pb2
The file to change is 
/home/ncn/projects/CalculationEngine/CalculationManager/env/lib/python3.8/site-packages/ICalculationManager/calculation_manager_pb2_grpc.py
More info in bug tracking: https://github.com/grpc/grpc/issues/11041
Solution then updated to move proto files into a separate folder to force correct relative paths :)
See solution here: https://github.com/grpc/grpc/issues/9575#issuecomment-293934506

# SOLUTION COPIED HERE:
Nevermind, I found the solution. I will quickly explain it in case anyone else is looking at this.
I now moved my proto files into a directory called proto/some/folder/
Then using the following command, the module names and imports are correct and work as expected in python3:
python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/some/folder/*.proto
Note that the combination of including the root directory (proto/) and directing the output to --python_out=. achieves the desired results:
Generated files end up in some/folder/, also imports are as expected:
import some.folder.someservice_pb2 as some_dot_folder_dot_someservice__pb2
