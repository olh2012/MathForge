"""
表达式解析器（Lexer + Parser）
将字符串表达式解析为AST
"""

import re
from typing import List, Optional
from .ast import Node, Symbol, Number, Add, Mul, Pow, Function, Sin, Cos, Tan, Exp, Log, Sqrt


class Token:
    """词法单元"""
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Lexer:
    """词法分析器"""
    
    TOKEN_PATTERNS = [
        (r'\s+', None),  # 空白字符
        (r'\d+\.?\d*', 'NUMBER'),  # 数字
        (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),  # 标识符
        (r'\+', 'PLUS'),
        (r'-', 'MINUS'),
        (r'\*', 'MULTIPLY'),
        (r'/', 'DIVIDE'),
        (r'\^', 'POWER'),
        (r'\(', 'LPAREN'),
        (r'\)', 'RPAREN'),
        (r',', 'COMMA'),
    ]
    
    FUNCTION_NAMES = {
        'sin': Sin, 'cos': Cos, 'tan': Tan,
        'exp': Exp, 'log': Log, 'sqrt': Sqrt
    }
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """词法分析"""
        while self.pos < len(self.text):
            matched = False
            for pattern, token_type in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    if token_type:  # 忽略空白字符
                        self.tokens.append(Token(token_type, match.group()))
                    self.pos = match.end()
                    matched = True
                    break
            
            if not matched:
                raise ValueError(f"无法识别的字符: {self.text[self.pos]}")
        
        return self.tokens


class Parser:
    """语法分析器（递归下降）"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> Node:
        """解析表达式"""
        if not self.tokens:
            raise ValueError("表达式为空")
        expr = self.parse_expression()
        if self.pos < len(self.tokens):
            raise ValueError(f"未预期的token: {self.tokens[self.pos]}")
        return expr
    
    def parse_expression(self) -> Node:
        """解析表达式（处理加减）"""
        left = self.parse_term()
        
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token.type == 'PLUS':
                self.pos += 1
                right = self.parse_term()
                left = Add(left, right)
            elif token.type == 'MINUS':
                self.pos += 1
                right = self.parse_term()
                left = Add(left, Mul(Number(-1), right))
            else:
                break
        
        return left
    
    def parse_term(self) -> Node:
        """解析项（处理乘除）"""
        left = self.parse_power()
        
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token.type == 'MULTIPLY':
                self.pos += 1
                right = self.parse_power()
                left = Mul(left, right)
            elif token.type == 'DIVIDE':
                self.pos += 1
                right = self.parse_power()
                left = Mul(left, Pow(right, Number(-1)))
            else:
                break
        
        return left
    
    def parse_power(self) -> Node:
        """解析幂次（右结合）"""
        left = self.parse_factor()
        
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'POWER':
            self.pos += 1
            right = self.parse_power()  # 右结合
            return Pow(left, right)
        
        return left
    
    def parse_factor(self) -> Node:
        """解析因子（处理函数、括号）"""
        token = self.tokens[self.pos]
        
        if token.type == 'NUMBER':
            self.pos += 1
            return Number(float(token.value))
        
        elif token.type == 'IDENTIFIER':
            self.pos += 1
            name = token.value
            
            # 检查是否是函数调用
            if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'LPAREN':
                self.pos += 1  # 跳过 '('
                arg = self.parse_expression()
                if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'RPAREN':
                    raise ValueError("缺少右括号")
                self.pos += 1  # 跳过 ')'
                
                # 创建函数节点
                func_class = Lexer.FUNCTION_NAMES.get(name)
                if func_class:
                    return func_class(arg)
                else:
                    raise ValueError(f"未知函数: {name}")
            
            # 普通符号
            return Symbol(name)
        
        elif token.type == 'LPAREN':
            self.pos += 1
            expr = self.parse_expression()
            if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'RPAREN':
                raise ValueError("缺少右括号")
            self.pos += 1
            return expr
        
        elif token.type == 'MINUS':
            self.pos += 1
            return Mul(Number(-1), self.parse_factor())
        
        else:
            raise ValueError(f"意外的token: {token}")


def parse(expr: str) -> Node:
    """
    解析字符串表达式为AST
    
    Args:
        expr: 数学表达式字符串
        
    Returns:
        AST节点
        
    Examples:
        >>> parse("x^2 + 3*x")
        Add(Pow(Symbol('x'), Number(2)), Mul(Number(3), Symbol('x')))
    """
    lexer = Lexer(expr)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
