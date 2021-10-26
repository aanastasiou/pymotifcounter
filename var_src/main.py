"""

    A set of experiments to get familiar with click.Option objects
    
    
:author: Athanasios Anastasiou
:date: Oct 2021

class Process:
    parameters: List[Parameter]
    binarylocation: Path
    raw_output
    
    __call__()
        ctx = before_run()
        ctx = run(ctx)
        ctx = after_run(ctx) #ctx must also contain the entire file returned by the algorithm
        return ctx    
    
class Parameter
    tag
    docstr
    type
    is_required
    

class MotifResultParser


class MotifResult

    
class MotifCounter
    Process process
    MotifResultParser parser
        
    __call__()
    Run process
    run motifresultparser on the result of process
    return a MotifResult   

"""    
from dataclasses import dataclass

@dataclass(repr=False)
class Parameter:
    """
    Represents a parameter that is used to pass data to an external program.
    """
    name: str
    long_name: str | None
    help_str: str
    param_type: str
    is_required: bool
    param_value: str = None
    
    def __repr__(self):
        return f"-{name} {param_value}"
    
    
if __name__ == "__main__":
    pass
    
    
