
from pgr import core 

# This file is generated by pgr-generator please do not modify it !!!

class ExampleVo1:
    __serialization__ = {
       "strField": core.Types.STRING, 
       "intField": core.Types.INT
    }
    
class ExampleVo2(ExampleVo1):
    __serialization__ = {
       "objField": "pl.simpatico.pgrexample.client.vo.ExampleVo3"
    }                       


class ExampleVo3:
    __serialization__ = {
       "strField": core.Types.STRING,
       "intField": core.Types.INT
    }        