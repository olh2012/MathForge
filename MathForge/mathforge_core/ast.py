"""
抽象语法树（AST）节点定义
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class Node(ABC):
    """所有AST节点的基类"""
    
    @abstractmethod
    def __str__(self) -> str:
        """字符串表示"""
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        """相等性比较"""
        pass
    
    @abstractmethod
    def substitute(self, substitutions: Dict[str, 'Node']) -> 'Node':
        """替换变量"""
        pass
    
    @abstractmethod
    def eval(self, values: Optional[Dict[str, float]] = None) -> float:
        """数值求值"""
        pass
    
    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = Number(other)
        return Add(self, other)
    
    def __radd__(self, other):
        if isinstance(other, (int, float)):
            other = Number(other)
        return Add(other, self)
    
    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = Number(other)
        return Add(self, Mul(Number(-1), other))
    
    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            other = Number(other)
        return Add(other, Mul(Number(-1), self))
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            other = Number(other)
        return Mul(self, other)
    
    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            other = Number(other)
        return Mul(other, self)
    
    def __pow__(self, other):
        if isinstance(other, (int, float)):
            other = Number(other)
        return Pow(self, other)
    
    def __neg__(self):
        return Mul(Number(-1), self)


class Symbol(Node):
    """符号变量"""
    
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Symbol) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def substitute(self, substitutions: Dict[str, Node]) -> Node:
        return substitutions.get(self.name, self)
    
    def eval(self, values: Optional[Dict[str, float]] = None) -> float:
        if values is None:
            raise ValueError(f"需要提供变量 {self.name} 的值")
        if self.name not in values:
            raise ValueError(f"变量 {self.name} 未在值字典中找到")
        return values[self.name]


class Number(Node):
    """数值常量"""
    
    def __init__(self, value: float):
        self.value = float(value)
    
    def __str__(self) -> str:
        if self.value == int(self.value):
            return str(int(self.value))
        return str(self.value)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return abs(self.value - float(other)) < 1e-10
        return isinstance(other, Number) and abs(self.value - other.value) < 1e-10
    
    def __hash__(self):
        return hash(self.value)
    
    def substitute(self, substitutions: Dict[str, Node]) -> Node:
        return self
    
    def eval(self, values: Optional[Dict[str, float]] = None) -> float:
        return self.value


class Add(Node):
    """加法节点"""
    
    def __init__(self, *args: Node):
        self.terms: List[Node] = list(args)
    
    def __str__(self) -> str:
        if not self.terms:
            return "0"
        result = []
        for i, term in enumerate(self.terms):
            term_str = str(term)
            if i > 0 and not term_str.startswith('-'):
                result.append('+')
            result.append(term_str)
        return ''.join(result)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Add):
            return False
        if len(self.terms) != len(other.terms):
            return False
        return set(self.terms) == set(other.terms)
    
    def substitute(self, substitutions: Dict[str, Node]) -> Node:
        return Add(*[term.substitute(substitutions) for term in self.terms])
    
    def eval(self, values: Optional[Dict[str, float]] = None) -> float:
        return sum(term.eval(values) for term in self.terms)


class Mul(Node):
    """乘法节点"""
    
    def __init__(self, *args: Node):
        self.factors: List[Node] = list(args)
    
    def __str__(self) -> str:
        if not self.factors:
            return "1"
        result = []
        for i, factor in enumerate(self.factors):
            if i > 0:
                result.append('*')
            factor_str = str(factor)
            if isinstance(factor, (Add, Pow)) or (isinstance(factor, Function)):
                result.append(f'({factor_str})')
            else:
                result.append(factor_str)
        return ''.join(result)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Mul):
            return False
        if len(self.factors) != len(other.factors):
            return False
        return set(self.factors) == set(other.factors)
    
    def substitute(self, substitutions: Dict[str, Node]) -> Node:
        return Mul(*[factor.substitute(substitutions) for factor in self.factors])
    
    def eval(self, values: Optional[Dict[str, float]] = None) -> float:
        result = 1.0
        for factor in self.factors:
            result *= factor.eval(values)
        return result


class Pow(Node):
    """幂次节点"""
    
    def __init__(self, base: Node, exponent: Node):
        self.base = base
        self.exponent = exponent
    
    def __str__(self) -> str:
        base_str = str(self.base)
        exp_str = str(self.exponent)
        
        if isinstance(self.base, (Add, Mul, Pow, Function)):
            base_str = f'({base_str})'
        
        return f'{base_str}^{exp_str}'
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Pow) and self.base == other.base and self.exponent == other.exponent
    
    def substitute(self, substitutions: Dict[str, Node]) -> Node:
        return Pow(self.base.substitute(substitutions), self.exponent.substitute(substitutions))
    
    def eval(self, values: Optional[Dict[str, float]] = None) -> float:
        return self.base.eval(values) ** self.exponent.eval(values)


class Function(Node):
    """函数节点基类"""
    
    def __init__(self, name: str, arg: Node):
        self.name = name
        self.arg = arg
    
    def __str__(self) -> str:
        arg_str = str(self.arg)
        if isinstance(self.arg, (Add, Mul, Pow)):
            arg_str = f'({arg_str})'
        return f'{self.name}({arg_str})'
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Function) and self.name == other.name and self.arg == other.arg
    
    def substitute(self, substitutions: Dict[str, Node]) -> Node:
        return type(self)(self.arg.substitute(substitutions))
    
    def eval(self, values: Optional[Dict[str, float]] = None) -> float:
        return self._eval_func(self.arg.eval(values))
    
    @abstractmethod
    def _eval_func(self, x: float) -> float:
        """具体的函数求值"""
        pass


class Sin(Function):
    """正弦函数"""
    
    def __init__(self, arg: Node):
        super().__init__('sin', arg)
    
    def _eval_func(self, x: float) -> float:
        import math
        return math.sin(x)


class Cos(Function):
    """余弦函数"""
    
    def __init__(self, arg: Node):
        super().__init__('cos', arg)
    
    def _eval_func(self, x: float) -> float:
        import math
        return math.cos(x)


class Tan(Function):
    """正切函数"""
    
    def __init__(self, arg: Node):
        super().__init__('tan', arg)
    
    def _eval_func(self, x: float) -> float:
        import math
        return math.tan(x)


class Exp(Function):
    """指数函数 e^x"""
    
    def __init__(self, arg: Node):
        super().__init__('exp', arg)
    
    def _eval_func(self, x: float) -> float:
        import math
        return math.exp(x)


class Log(Function):
    """自然对数函数"""
    
    def __init__(self, arg: Node):
        super().__init__('log', arg)
    
    def _eval_func(self, x: float) -> float:
        import math
        return math.log(x)


class Sqrt(Function):
    """平方根函数"""
    
    def __init__(self, arg: Node):
        super().__init__('sqrt', arg)
    
    def _eval_func(self, x: float) -> float:
        import math
        return math.sqrt(x)
