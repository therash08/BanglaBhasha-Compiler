# BanglaBhasha Compiler — a toy Bangla programming language compiler.
# Pipeline: Source -> Lexer -> Parser/AST -> Semantic Analysis -> TAC -> Python

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict, Tuple

# ============================================================
# 1. TOKENS
# ============================================================

@dataclass
class Token:
    kind: str
    lexeme: str
    line: int
    column: int
    value: Any = None
    def __repr__(self):
        return f"Token({self.kind}, {self.lexeme!r}, line={self.line}, col={self.column})"

KEYWORDS = {
    "ধরি": "LET", "পূর্ণসংখ্যা": "TYPE_INT", "দশমিক": "TYPE_FLOAT",
    "বুলিয়ান": "TYPE_BOOL", "স্ট্রিং": "TYPE_STRING", "লেখো": "PRINT",
    "যদি": "IF", "নাহলে": "ELSE", "যতক্ষণ": "WHILE", "ফাংশন": "FUNCTION",
    "ফেরত": "RETURN", "ক্লাস": "CLASS", "নতুন": "NEW", "নিজে": "SELF",
    "সত্য": "TRUE", "মিথ্যা": "FALSE", "স্ট্যাক": "STACK", "কিউ": "QUEUE",
    "ঠেলো": "PUSH", "বের_করো": "POP", "সামনে_দেখো": "PEEK",
    "ঢোকাও": "ENQUEUE", "বের_করো_কিউ": "DEQUEUE", "সামনে_দেখো_কিউ": "FRONT",
    "এবং": "AND", "অথবা": "OR", "নয়": "NOT", "থামো": "BREAK",
    "চালাও": "RUN",
}

TOKEN_SIMPLE = {
    "+":"PLUS", "-":"MINUS", "*":"STAR", "/":"SLASH", "%":"MOD",
    "=":"ASSIGN", "(":"LPAREN", ")":"RPAREN", "{":"LBRACE", "}":"RBRACE",
    ",":"COMMA", ";":"SEMICOLON", ".":"DOT", ":":"COLON",
    "<":"LT", ">":"GT", "!":"NOT", "[":"LBRACKET", "]":"RBRACKET",
}

TWO_CHAR = {"==":"EQ", "!=":"NE", "<=":"LE", ">=":"GE", "&&":"AND", "||":"OR", "->":"ARROW"}

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
        self.errors: List[str] = []

    def current(self):
        return self.source[self.pos] if self.pos < len(self.source) else ""
    def peek(self, n=1):
        p = self.pos + n
        return self.source[p] if p < len(self.source) else ""
    def advance(self):
        ch = self.current()
        if ch:
            self.pos += 1
            if ch == "\n":
                self.line += 1; self.col = 1
            else:
                self.col += 1
        return ch
    def add(self, kind, lexeme, line, col, value=None):
        self.tokens.append(Token(kind, lexeme, line, col, value))

    def tokenize(self):
        while self.pos < len(self.source):
            ch = self.current()
            line, col = self.line, self.col
            if ch in " \t\r":
                self.advance(); continue
            if ch == "\n":
                self.add("NEWLINE", "\\n", line, col); self.advance(); continue
            if ch == "/" and self.peek() == "/":
                while self.current() not in ("", "\n"): self.advance()
                continue
            if ch == "#":
                while self.current() not in ("", "\n"): self.advance()
                continue
            pair = ch + self.peek()
            if pair in TWO_CHAR:
                self.add(TWO_CHAR[pair], pair, line, col); self.advance(); self.advance(); continue
            if ch in TOKEN_SIMPLE:
                kind = TOKEN_SIMPLE[ch]
                # '!' alone is NOT; comparison != was handled above.
                self.add(kind, ch, line, col); self.advance(); continue
            if ch == '"' or ch == "'":
                self._read_string(); continue
            if ch.isdigit():
                self._read_number(); continue
            if self._is_identifier_char(ch):
                self._read_identifier(); continue
            self.errors.append(f"লাইন {line}, কলাম {col}: অজানা চিহ্ন '{ch}'")
            self.advance()
        self.add("EOF", "", self.line, self.col)
        return self.tokens

    def _read_number(self):
        line, col = self.line, self.col
        start = self.pos
        while self.current().isdigit(): self.advance()
        kind = "INT"
        if self.current() == "." and self.peek().isdigit():
            kind = "FLOAT"; self.advance()
            while self.current().isdigit(): self.advance()
        text = self.source[start:self.pos]
        self.add(kind, text, line, col, float(text) if kind == "FLOAT" else int(text))

    def _read_string(self):
        line, col = self.line, self.col
        quote = self.advance(); chars=[]
        escaped=False
        while self.current() and self.current() != quote:
            ch=self.advance()
            if escaped:
                chars.append({"n":"\n","t":"\t","r":"\r","\\":"\\","\"":"\"","'":"'"}.get(ch,ch)); escaped=False
            elif ch == "\\": escaped=True
            else: chars.append(ch)
        if self.current() != quote:
            self.errors.append(f"লাইন {line}: স্ট্রিং বন্ধ করা হয়নি")
            return
        self.advance()
        value="".join(chars)
        self.add("STRING", self.source[max(0,self.pos-len(value)-2):self.pos], line, col, value)

    def _is_identifier_char(self, ch):
        if not ch: return False
        cat=unicodedata.category(ch)
        return ch == "_" or cat[0] in ("L", "M", "N")

    def _read_identifier(self):
        line,col=self.line,self.col; start=self.pos
        while self.current() and self._is_identifier_char(self.current()):
            self.advance()
        word=self.source[start:self.pos]
        self.add(KEYWORDS.get(word,"IDENT"), word, line,col,word)

# ============================================================
# 2. AST
# ============================================================

class AST: pass
@dataclass
class Program(AST): statements: List[AST]
@dataclass
class Literal(AST): value: Any; type_name: str
@dataclass
class Var(AST): name: str
@dataclass
class Binary(AST): left: AST; op: str; right: AST
@dataclass
class Unary(AST): op: str; operand: AST
@dataclass
class Assign(AST): name: str; expr: AST; declared_type: Optional[str]=None
@dataclass
class Print(AST): expr: AST
@dataclass
class ExprStmt(AST): expr: AST
@dataclass
class Block(AST): statements: List[AST]
@dataclass
class If(AST): condition: AST; then_block: Block; else_block: Optional[Block]=None
@dataclass
class While(AST): condition: AST; body: Block
@dataclass
class Break(AST): pass
@dataclass
class Return(AST): expr: Optional[AST]
@dataclass
class Function(AST): name: str; params: List[Tuple[str,Optional[str]]]; body: Block; return_type: Optional[str]=None
@dataclass
class Call(AST): callee: AST; args: List[AST]
@dataclass
class Member(AST): object: AST; name: str
@dataclass
class MethodCall(AST): object: AST; name: str; args: List[AST]
@dataclass
class New(AST): class_name: str; args: List[AST]
@dataclass
class ClassDef(AST): name: str; fields: List[Assign]; methods: List[Function]
@dataclass
class StackCreate(AST): name: str
@dataclass
class QueueCreate(AST): name: str
@dataclass
class StackOp(AST): object: AST; op: str; args: List[AST]
@dataclass
class ListLiteral(AST): elements: List[AST]

# ============================================================
# 3. PARSER
# ============================================================

TYPE_TOKENS = {"TYPE_INT":"int","TYPE_FLOAT":"float","TYPE_BOOL":"bool","TYPE_STRING":"string"}

class Parser:
    def __init__(self,tokens):
        self.tokens=tokens; self.pos=0; self.errors=[]
    def cur(self): return self.tokens[self.pos]
    def peek(self,n=1): return self.tokens[min(self.pos+n,len(self.tokens)-1)]
    def at(self,kind): return self.cur().kind==kind
    def advance(self):
        t=self.cur()
        if self.pos < len(self.tokens)-1: self.pos+=1
        return t
    def match(self,*kinds):
        if self.cur().kind in kinds: return self.advance()
        return None
    def expect(self,kind,msg=None):
        if self.at(kind): return self.advance()
        t=self.cur(); self.error(t,msg or f"'{kind}' প্রত্যাশিত, পাওয়া গেছে '{t.lexeme}'")
        return Token(kind,"",t.line,t.column)
    def error(self,t,msg): self.errors.append(f"লাইন {t.line}, কলাম {t.column}: {msg}")
    def sync(self):
        while not self.at("EOF") and not self.at("SEMICOLON") and not self.at("NEWLINE") and not self.at("RBRACE"): self.advance()
        self.match("SEMICOLON","NEWLINE")
    def skip_lines(self):
        while self.match("NEWLINE","SEMICOLON"): pass

    def parse(self):
        stmts=[]; self.skip_lines()
        while not self.at("EOF"):
            try:
                s=self.statement()
                if s is not None: stmts.append(s)
            except Exception as e:
                self.error(self.cur(),f"পার্সিং সমস্যা: {e}"); self.sync()
            self.skip_lines()
        return Program(stmts)

    def statement(self):
        k=self.cur().kind
        if k in TYPE_TOKENS or k=="LET": return self.var_decl()
        if k=="PRINT":
            self.advance(); e=self.expression(); self.end_stmt(); return Print(e)
        if k=="IF": return self.if_stmt()
        if k=="WHILE": return self.while_stmt()
        if k=="BREAK": self.advance(); self.end_stmt(); return Break()
        if k=="RETURN":
            self.advance(); e=None if self.at("SEMICOLON") or self.at("NEWLINE") or self.at("RBRACE") else self.expression(); self.end_stmt(); return Return(e)
        if k=="FUNCTION": return self.function_def()
        if k=="CLASS": return self.class_def()
        if k=="STACK": return self.stack_decl()
        if k=="QUEUE": return self.queue_decl()
        if k=="IDENT" and self.peek().kind=="ASSIGN":
            name=self.advance().lexeme; self.advance(); e=self.expression(); self.end_stmt(); return Assign(name,e)
        # member assignment: obj.field = expr
        if k in {"IDENT","SELF"} and self.peek().kind=="DOT" and self.peek(2).kind in {"IDENT","PUSH","POP","PEEK","ENQUEUE","DEQUEUE","FRONT"} and self.peek(3).kind=="ASSIGN":
            obj=self.advance().lexeme; self.advance(); field=self.advance().lexeme; self.advance(); e=self.expression(); self.end_stmt(); return Assign(f"{obj}.{field}",e)
        # expression statement, mainly method/function calls such as s.ঠেলো(10);
        if k=="IDENT":
            e=self.expression(); self.end_stmt(); return ExprStmt(e)
        self.error(self.cur(),f"অপ্রত্যাশিত statement শুরু '{self.cur().lexeme}'"); self.sync(); return None

    def var_decl(self):
        tok=self.advance(); declared=TYPE_TOKENS.get(tok.kind)
        if tok.kind=="LET": declared=None
        name=self.expect("IDENT","ভেরিয়েবলের নাম প্রত্যাশিত").lexeme
        if self.match("ASSIGN"):
            expr=self.expression()
        else:
            if declared:
                defaults={"int":0,"float":0.0,"bool":False,"string":""}
                expr=Literal(defaults[declared],declared)
            else:
                self.error(self.cur(),"'ধরি' declaration-এ initial value দিতে হবে")
                expr=Literal(None,"error")
        self.end_stmt(); return Assign(name,expr,declared)

    def stack_decl(self):
        self.advance(); name=self.expect("IDENT","স্ট্যাকের নাম প্রত্যাশিত").lexeme; self.end_stmt(); return StackCreate(name)
    def queue_decl(self):
        self.advance(); name=self.expect("IDENT","কিউয়ের নাম প্রত্যাশিত").lexeme; self.end_stmt(); return QueueCreate(name)

    def if_stmt(self):
        self.advance(); self.expect("LPAREN","if-এর condition-এর আগে '(' দরকার"); c=self.expression(); self.expect("RPAREN", "condition-এর পরে ')' দরকার"); b=self.block(); eb=None
        self.skip_lines()
        if self.match("ELSE"): eb=self.block()
        return If(c,b,eb)
    def while_stmt(self):
        self.advance(); self.expect("LPAREN","while-এর condition-এর আগে '(' দরকার"); c=self.expression(); self.expect("RPAREN","condition-এর পরে ')' দরকার"); return While(c,self.block())
    def block(self):
        self.expect("LBRACE","'{' প্রত্যাশিত"); self.skip_lines(); ss=[]
        while not self.at("RBRACE") and not self.at("EOF"):
            try:
                s=self.statement()
                if s: ss.append(s)
            except Exception as e:
                self.error(self.cur(),f"block parsing সমস্যা: {e}"); self.sync()
            self.skip_lines()
        self.expect("RBRACE","'}' প্রত্যাশিত"); return Block(ss)

    def function_def(self):
        self.advance(); name=self.expect("IDENT","ফাংশনের নাম প্রত্যাশিত").lexeme; self.expect("LPAREN","'(' প্রত্যাশিত"); params=[]
        if not self.at("RPAREN"):
            while True:
                pt=None
                if self.cur().kind in TYPE_TOKENS: pt=TYPE_TOKENS[self.advance().kind]
                if self.at("SELF"):
                    pn=self.advance().lexeme
                else:
                    pn=self.expect("IDENT","parameter-এর নাম প্রত্যাশিত").lexeme
                params.append((pn,pt))
                if not self.match("COMMA"): break
        self.expect("RPAREN","')' প্রত্যাশিত")
        rt=None
        if self.match("ARROW"):
            if self.cur().kind in TYPE_TOKENS: rt=TYPE_TOKENS[self.advance().kind]
            else: rt=self.expect("IDENT").lexeme
        return Function(name,params,self.block(),rt)

    def class_def(self):
        self.advance(); name=self.expect("IDENT","class-এর নাম প্রত্যাশিত").lexeme; self.expect("LBRACE","'{' প্রত্যাশিত"); self.skip_lines(); fields=[]; methods=[]
        while not self.at("RBRACE") and not self.at("EOF"):
            if self.at("FUNCTION"): methods.append(self.function_def())
            elif self.cur().kind in TYPE_TOKENS or self.at("LET"):
                fields.append(self.var_decl())
            else:
                self.error(self.cur(),"class-এর ভিতরে field declaration বা function দরকার"); self.sync()
            self.skip_lines()
        self.expect("RBRACE","'}' প্রত্যাশিত"); return ClassDef(name,fields,methods)

    def end_stmt(self):
        if self.match("SEMICOLON"): self.match("NEWLINE"); return
        if self.match("NEWLINE"): return
        if self.at("RBRACE") or self.at("EOF"): return
        self.error(self.cur(),"statement-এর শেষে ';' বা নতুন লাইন দরকার")
        self.sync()

    # expression precedence: or -> and -> equality -> comparison -> term -> factor -> unary -> postfix -> primary
    def expression(self): return self.parse_or()
    def parse_or(self):
        e=self.parse_and()
        while self.match("OR"): e=Binary(e,"অথবা",self.parse_and())
        return e
    def parse_and(self):
        e=self.parse_equality()
        while self.match("AND"): e=Binary(e,"এবং",self.parse_equality())
        return e
    def parse_equality(self):
        e=self.parse_comparison()
        while self.at("EQ") or self.at("NE"):
            op=self.advance().lexeme; e=Binary(e,op,self.parse_comparison())
        return e
    def parse_comparison(self):
        e=self.parse_term()
        while self.at("LT") or self.at("LE") or self.at("GT") or self.at("GE"):
            op=self.advance().lexeme; e=Binary(e,op,self.parse_term())
        return e
    def parse_term(self):
        e=self.parse_factor()
        while self.at("PLUS") or self.at("MINUS"):
            op=self.advance().lexeme; e=Binary(e,op,self.parse_factor())
        return e
    def parse_factor(self):
        e=self.parse_unary()
        while self.at("STAR") or self.at("SLASH") or self.at("MOD"):
            op=self.advance().lexeme; e=Binary(e,op,self.parse_unary())
        return e
    def parse_unary(self):
        if self.at("MINUS") or self.at("NOT"):
            op=self.advance().lexeme; return Unary(op,self.parse_unary())
        return self.parse_postfix()
    def parse_postfix(self):
        e=self.primary()
        while True:
            if self.match("LPAREN"):
                args=[]
                if not self.at("RPAREN"):
                    while True:
                        args.append(self.expression())
                        if not self.match("COMMA"): break
                self.expect("RPAREN"); e=Call(e,args)
            elif self.match("DOT"):
                name=self.member_name()
                if self.match("LPAREN"):
                    args=[]
                    if not self.at("RPAREN"):
                        while True:
                            args.append(self.expression())
                            if not self.match("COMMA"): break
                    self.expect("RPAREN"); e=MethodCall(e,name,args)
                else: e=Member(e,name)
            else: break
        return e
    def member_name(self):
        t=self.cur()
        allowed={"IDENT","PUSH","POP","PEEK","ENQUEUE","DEQUEUE","FRONT","PRINT","SELF","STACK","QUEUE","BREAK"}
        if t.kind in allowed:
            self.advance(); return t.lexeme
        self.error(t,"member name দরকার"); self.advance(); return t.lexeme

    def primary(self):
        t=self.cur()
        if self.match("INT"): return Literal(t.value,"int")
        if self.match("FLOAT"): return Literal(t.value,"float")
        if self.match("STRING"): return Literal(t.value,"string")
        if self.match("TRUE"): return Literal(True,"bool")
        if self.match("FALSE"): return Literal(False,"bool")
        if self.match("IDENT") or self.match("SELF"): return Var(t.lexeme)
        if self.match("NEW"):
            name=self.expect("IDENT","class name দরকার").lexeme; self.expect("LPAREN","'(' দরকার"); args=[]
            if not self.at("RPAREN"):
                while True:
                    args.append(self.expression())
                    if not self.match("COMMA"): break
            self.expect("RPAREN"); return New(name,args)
        if self.match("LPAREN"):
            e=self.expression(); self.expect("RPAREN", "')' দরকার"); return e
        if self.match("LBRACKET"):
            els=[]
            if not self.at("RBRACKET"):
                while True:
                    els.append(self.expression())
                    if not self.match("COMMA"): break
            self.expect("RBRACKET"); return ListLiteral(els)
        self.error(t,f"expression-এ অপ্রত্যাশিত token '{t.lexeme}'"); self.advance(); return Literal(None,"error")

# ============================================================
# 4. SEMANTIC ANALYSIS + SYMBOL TABLE
# ============================================================

@dataclass
class Symbol:
    type_name: str
    initialized: bool=True

class SemanticAnalyser:
    def __init__(self):
        self.scopes=[{}]; self.functions={}; self.classes={}; self.errors=[]; self.loop_depth=0; self.current_return=None
    @property
    def table(self): return self.scopes[-1]
    def push(self): self.scopes.append({})
    def pop(self): self.scopes.pop()
    def define(self,n,t): self.table[n]=Symbol(t)
    def lookup(self,n):
        for s in reversed(self.scopes):
            if n in s: return s[n].type_name
        return None
    def compatible(self,expected,actual):
        if expected==actual: return True
        return expected=="float" and actual=="int"
    def analyse(self,program):
        for s in program.statements:
            if isinstance(s,Function): self.functions[s.name]=s
            if isinstance(s,ClassDef): self.classes[s.name]=s
        for s in program.statements: self.stmt(s)
        return self
    def err(self,msg): self.errors.append(msg)
    def stmt(self,n):
        if isinstance(n,Assign):
            actual=self.expr(n.expr)
            if n.declared_type:
                if not self.compatible(n.declared_type,actual): self.err(f"টাইপ mismatch: '{n.name}'-এর জন্য {n.declared_type} দরকার, কিন্তু পাওয়া গেছে {actual}")
                t=n.declared_type
            else:
                old=self.lookup(n.name)
                if old and not self.compatible(old,actual): self.err(f"টাইপ mismatch: '{n.name}' ছিল {old}, নতুন মান {actual}")
                t=old or actual
            self.define(n.name,t)
        elif isinstance(n,Print): self.expr(n.expr)
        elif isinstance(n,ExprStmt): self.expr(n.expr)
        elif isinstance(n,Block):
            self.push(); [self.stmt(x) for x in n.statements]; self.pop()
        elif isinstance(n,If):
            c=self.expr(n.condition)
            if c!="bool": self.err(f"if condition-এ bool দরকার, পাওয়া গেছে {c}")
            self.stmt(n.then_block)
            if n.else_block: self.stmt(n.else_block)
        elif isinstance(n,While):
            c=self.expr(n.condition)
            if c!="bool": self.err(f"while condition-এ bool দরকার, পাওয়া গেছে {c}")
            self.loop_depth+=1; self.stmt(n.body); self.loop_depth-=1
        elif isinstance(n,Break):
            if self.loop_depth==0: self.err("'থামো' শুধু loop-এর ভিতরে ব্যবহার করা যাবে")
        elif isinstance(n,Return):
            t="void" if n.expr is None else self.expr(n.expr)
            if self.current_return and not self.compatible(self.current_return,t): self.err(f"return type mismatch: {self.current_return} বনাম {t}")
        elif isinstance(n,Function):
            self.push()
            for p,t in n.params: self.define(p,t or "any")
            old=self.current_return; self.current_return=n.return_type
            self.stmt(n.body); self.current_return=old; self.pop()
        elif isinstance(n,ClassDef):
            # Validate field defaults and method bodies; method parameters create their own scope.
            self.push()
            for f in n.fields: self.stmt(f)
            for m in n.methods: self.stmt(m)
            self.pop()
        elif isinstance(n,(StackCreate,QueueCreate)): self.define(n.name,"stack" if isinstance(n,StackCreate) else "queue")
        else:
            self.expr(n)
    def expr(self,n):
        if isinstance(n,Literal): return n.type_name
        if isinstance(n,Var):
            t=self.lookup(n.name)
            if t is None: self.err(f"variable '{n.name}' আগে define করা হয়নি")
            return t or "error"
        if isinstance(n,ListLiteral):
            for x in n.elements: self.expr(x)
            return "list"
        if isinstance(n,Unary):
            t=self.expr(n.operand)
            if n.op=="-" and t not in ("int","float"): self.err("unary '-' এর operand numeric হতে হবে")
            if n.op=="!" and t!="bool": self.err("'!' এর operand bool হতে হবে")
            return "bool" if n.op=="!" else t
        if isinstance(n,Binary):
            a,b=self.expr(n.left),self.expr(n.right)
            if n.op in ("+","-","*","/","%"):
                if n.op=="+" and a==b=="string": return "string"
                if a not in ("int","float") or b not in ("int","float"): self.err(f"operator '{n.op}'-এ numeric operand দরকার, পাওয়া গেছে {a}, {b}"); return "error"
                return "float" if "float" in (a,b) or n.op=="/" else "int"
            if n.op in ("<","<=",">",">=","==","!="): return "bool"
            if n.op in ("এবং","অথবা"): 
                if a!="bool" or b!="bool": self.err(f"'{n.op}'-এ bool operand দরকার")
                return "bool"
        if isinstance(n,Call):
            for a in n.args:self.expr(a)
            if isinstance(n.callee,Var) and n.callee.name in self.functions:
                f=self.functions[n.callee.name]
                if len(f.params)!=len(n.args): self.err(f"function '{f.name}'-এ {len(f.params)}টি argument দরকার")
                return f.return_type or "any"
            return "any"
        if isinstance(n,New):
            for a in n.args:self.expr(a)
            return n.class_name
        if isinstance(n,Member):
            return "any"
        if isinstance(n,MethodCall):
            ot=self.expr(n.object)
            for a in n.args:self.expr(a)
            return "any"
        return "any"

# ============================================================
# 5. TAC / IR
# ============================================================

@dataclass
class TAC:
    op:str; args:tuple=(); result:Optional[str]=None; extra:Any=None
    def __str__(self):
        if self.op=="LABEL": return f"{self.args[0]}:"
        if self.op=="JUMP": return f"goto {self.args[0]}"
        if self.op=="CJUMP": return f"if {self.args[0]} goto {self.args[1]} else {self.args[2]}"
        if self.op=="BINOP": return f"{self.result} = {self.args[0]} {self.args[1]} {self.args[2]}"
        if self.op=="UNARY": return f"{self.result} = {self.args[0]} {self.args[1]}"
        if self.op=="ASSIGN": return f"{self.result} = {self.args[0]}"
        if self.op=="PRINT": return f"print {self.args[0]}"
        if self.op=="CALL": return f"{self.result or '_'} = call {self.args[0]}({', '.join(self.args[1])})"
        if self.op=="RETURN": return f"return {self.args[0] if self.args else ''}".rstrip()
        if self.op=="FUNC": return f"function {self.args[0]}({', '.join(self.args[1])})"
        if self.op=="CLASS": return f"class {self.args[0]}"
        if self.op=="STACK": return f"{self.result} = stack()"
        if self.op=="QUEUE": return f"{self.result} = queue()"
        if self.op=="METHOD": return f"{self.result or '_'} = {self.args[0]}.{self.args[1]}({', '.join(self.args[2])})"
        if self.op=="NEW": return f"{self.result} = new {self.args[0]}({', '.join(self.args[1])})"
        if self.op=="EXPR": return str(self.args[0])
        if self.op=="BREAK": return "break"
        if self.op=="ENDFUNC": return "end function"
        return self.op

class TACGenerator:
    def __init__(self): self.code=[]; self.temp=0; self.label=0
    def new_temp(self): x=f"t{self.temp}"; self.temp+=1; return x
    def new_label(self,p="L"): x=f"{p}{self.label}"; self.label+=1; return x
    def emit(self,*a,**kw): self.code.append(TAC(*a,**kw))
    def generate(self,p):
        for s in p.statements:self.stmt(s)
        return self.code
    def stmt(self,n):
        if isinstance(n,Assign): self.emit("ASSIGN",(self.expr(n.expr),),n.name)
        elif isinstance(n,Print): self.emit("PRINT",(self.expr(n.expr),))
        elif isinstance(n,ExprStmt): self.emit("EXPR",(self.expr(n.expr),))
        elif isinstance(n,StackCreate): self.emit("STACK",result=n.name)
        elif isinstance(n,QueueCreate): self.emit("QUEUE",result=n.name)
        elif isinstance(n,Block):
            for s in n.statements:self.stmt(s)
        elif isinstance(n,If):
            c=self.expr(n.condition); lt=self.new_label("THEN"); le=self.new_label("ELSE"); end=self.new_label("ENDIF")
            self.emit("CJUMP",(c,lt,le))
            self.emit("LABEL",(lt,)); self.stmt(n.then_block); self.emit("JUMP",(end,))
            self.emit("LABEL",(le,))
            if n.else_block:self.stmt(n.else_block)
            self.emit("LABEL",(end,))
        elif isinstance(n,While):
            start=self.new_label("WHILE"); body=self.new_label("WHILE_BODY"); end=self.new_label("ENDWHILE")
            self.emit("LABEL",(start,)); c=self.expr(n.condition); self.emit("CJUMP",(c,body,end)); self.emit("LABEL",(body,)); self.stmt(n.body); self.emit("JUMP",(start,)); self.emit("LABEL",(end,))
        elif isinstance(n,Break): self.emit("BREAK")
        elif isinstance(n,Return): self.emit("RETURN",() if n.expr is None else (self.expr(n.expr),))
        elif isinstance(n,Function):
            self.emit("FUNC",(n.name,[p[0] for p in n.params]),extra=n.body)
            # generate body separately for inspection
            sub=TACGenerator(); body=sub.generate(n.body); self.code.extend(body)
            self.emit("ENDFUNC")
        elif isinstance(n,ClassDef):
            self.emit("CLASS",(n.name,),extra=n)
        else: self.expr(n)
    def expr(self,n):
        if isinstance(n,Literal): return repr(n.value) if n.type_name=="string" else ("সত্য" if n.value is True else "মিথ্যা" if n.value is False else str(n.value))
        if isinstance(n,Var): return n.name
        if isinstance(n,ListLiteral): return "["+", ".join(self.expr(x) for x in n.elements)+"]"
        if isinstance(n,Unary):
            x=self.expr(n.operand); t=self.new_temp(); self.emit("UNARY",(n.op,x),t); return t
        if isinstance(n,Binary):
            a,b=self.expr(n.left),self.expr(n.right); t=self.new_temp(); self.emit("BINOP",(a,n.op,b),t); return t
        if isinstance(n,Call):
            callee=self.expr(n.callee); args=[self.expr(x) for x in n.args]; t=self.new_temp(); self.emit("CALL",(callee,args),t); return t
        if isinstance(n,New):
            args=[self.expr(x) for x in n.args]; t=self.new_temp(); self.emit("NEW",(n.class_name,args),t); return t
        if isinstance(n,Member): return f"{self.expr(n.object)}.{n.name}"
        if isinstance(n,MethodCall):
            obj=self.expr(n.object); args=[self.expr(x) for x in n.args]; t=self.new_temp(); self.emit("METHOD",(obj,n.name,args),t); return t
        return "None"

# ============================================================
# 6. PYTHON BACKEND
# ============================================================

PY_KEYWORDS = set(__import__('keyword').kwlist)

def py_name(name):
    # Python 3 supports Unicode identifiers, so Bangla names can be preserved.
    # The language keyword "নিজে" maps to Python's conventional "self" inside methods.
    if name == "নিজে": return "self"
    return f"_v_{name}" if name in PY_KEYWORDS else name

def replace_expr_text(s):
    # IR textual literals/operators -> Python syntax.
    s=s.replace("এবং","and").replace("অথবা","or").replace("সত্য","True").replace("মিথ্যা","False")
    # unary নয় is tokenized as NOT with lexeme '!' in the current syntax; both are supported.
    return s

RUNTIME = '''class স্ট্যাক:
    def __init__(self): self._data = []
    def ঠেলো(self, value): self._data.append(value)
    def বের_করো(self): return self._data.pop() if self._data else None
    def সামনে_দেখো(self): return self._data[-1] if self._data else None
    def খালি(self): return len(self._data) == 0
    def আকার(self): return len(self._data)

class কিউ:
    def __init__(self): self._data = []
    def ঢোকাও(self, value): self._data.append(value)
    def বের_করো_কিউ(self): return self._data.pop(0) if self._data else None
    def সামনে_দেখো_কিউ(self): return self._data[0] if self._data else None
    def খালি(self): return len(self._data) == 0
    def আকার(self): return len(self._data)
'''

class PythonBackend:
    def __init__(self): self.lines=[]; self.indent=0; self.temp_names=set(); self.loop_depth=0
    def emit(self,s=""): self.lines.append("    "*self.indent+s)
    def expr(self,n):
        if isinstance(n,Literal):
            if n.type_name=="string": return repr(n.value)
            if n.type_name=="bool": return "True" if n.value else "False"
            if n.type_name=="null": return "None"
            return repr(n.value)
        if isinstance(n,Var): return py_name(n.name)
        if isinstance(n,ListLiteral): return "["+", ".join(self.expr(x) for x in n.elements)+"]"
        if isinstance(n,Unary): return ("not " if n.op in ("!","নয়") else n.op)+self.expr(n.operand)
        if isinstance(n,Binary):
            op={"এবং":"and","অথবা":"or"}.get(n.op,n.op)
            return f"({self.expr(n.left)} {op} {self.expr(n.right)})"
        if isinstance(n,Call): return f"{self.expr(n.callee)}({', '.join(self.expr(a) for a in n.args)})"
        if isinstance(n,Member): return f"{self.expr(n.object)}.{n.name}"
        if isinstance(n,MethodCall): return f"{self.expr(n.object)}.{n.name}({', '.join(self.expr(a) for a in n.args)})"
        if isinstance(n,New): return f"{py_name(n.class_name)}({', '.join(self.expr(a) for a in n.args)})"
        return "None"
    def stmt(self,n):
        if isinstance(n,Assign):
            # field assignment such as obj.field = x
            target=".".join(py_name(x) for x in n.name.split("."))
            self.emit(f"{target} = {self.expr(n.expr)}")
        elif isinstance(n,Print): self.emit(f"print({self.expr(n.expr)})")
        elif isinstance(n,ExprStmt): self.emit(self.expr(n.expr))
        elif isinstance(n,StackCreate): self.emit(f"{py_name(n.name)} = স্ট্যাক()")
        elif isinstance(n,QueueCreate): self.emit(f"{py_name(n.name)} = কিউ()")
        elif isinstance(n,Block):
            for s in n.statements:self.stmt(s)
        elif isinstance(n,If):
            self.emit(f"if {self.expr(n.condition)}:"); self.indent+=1
            if n.then_block.statements:
                for s in n.then_block.statements:self.stmt(s)
            else:self.emit("pass")
            self.indent-=1
            if n.else_block:
                self.emit("else:"); self.indent+=1
                if n.else_block.statements:
                    for s in n.else_block.statements:self.stmt(s)
                else:self.emit("pass")
                self.indent-=1
        elif isinstance(n,While):
            self.emit(f"while {self.expr(n.condition)}:"); self.indent+=1
            if n.body.statements:
                for s in n.body.statements:self.stmt(s)
            else:self.emit("pass")
            self.indent-=1
        elif isinstance(n,Break): self.emit("break")
        elif isinstance(n,Return): self.emit("return" if n.expr is None else f"return {self.expr(n.expr)}")
        elif isinstance(n,Function):
            params=", ".join(py_name(p[0]) for p in n.params)
            self.emit(f"def {py_name(n.name)}({params}):"); self.indent+=1
            if n.body.statements:
                for s in n.body.statements:self.stmt(s)
            else:self.emit("pass")
            self.indent-=1; self.emit()
        elif isinstance(n,ClassDef):
            self.emit(f"class {py_name(n.name)}:"); self.indent+=1
            if not n.fields and not n.methods: self.emit("pass")
            # Fields become defaults at class level; methods are emitted normally.
            for f in n.fields:
                target=py_name(f.name)
                self.emit(f"{target} = {self.expr(f.expr)}")
            for m in n.methods:
                params=m.params[:]
                # 'নিজে' is a natural Bangla self parameter, map to self.
                ptxt=[]
                for pn,_ in params: ptxt.append("self" if pn=="নিজে" else py_name(pn))
                self.emit(f"def {py_name(m.name)}({', '.join(ptxt)}):"); self.indent+=1
                if m.body.statements:
                    for s in m.body.statements:self.stmt(s)
                else:self.emit("pass")
                self.indent-=1; self.emit()
            self.indent-=1; self.emit()
    def generate(self,p):
        self.lines=[]
        self.emit("# Generated by BanglaBhasha Compiler")
        self.emit("# Source language: BanglaBhasha")
        self.emit()
        self.lines.extend(RUNTIME.splitlines())
        self.emit()
        for s in p.statements:self.stmt(s)
        return "\n".join(self.lines)+"\n"

# ============================================================
# 7. COMPILER DRIVER / ERROR RECOVERY
# ============================================================

class CompilationResult:
    def __init__(self,source):
        self.source=source; self.tokens=[]; self.ast=None; self.semantic=None; self.tac=[]; self.python_code=""; self.errors=[]; self.warnings=[]
    @property
    def success(self): return not self.errors

class Compiler:
    def compile(self,source):
        r=CompilationResult(source)
        lex=Lexer(source); r.tokens=lex.tokenize(); r.errors.extend(lex.errors)
        parser=Parser(r.tokens); r.ast=parser.parse(); r.errors.extend(parser.errors)
        if r.errors: return r
        sem=SemanticAnalyser().analyse(r.ast); r.semantic=sem; r.errors.extend(sem.errors)
        if r.errors: return r
        r.tac=TACGenerator().generate(r.ast)
        r.python_code=PythonBackend().generate(r.ast)
        return r
    def compile_and_run(self,source):
        r=self.compile(source)
        if not r.success:return r,None
        namespace={"__name__":"__bangla_generated__"}
        try:
            import contextlib,io
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf): exec(r.python_code,namespace,namespace)
            return r,buf.getvalue()
        except Exception as e:
            r.errors.append(f"Runtime error: {type(e).__name__}: {e}")
            return r,None

def print_tokens(tokens):
    for t in tokens: print(t)
def print_tac(tac):
    for i,x in enumerate(tac): print(f"{i:03}: {x}")
def ast_to_text(node,indent=0):
    p="  "*indent
    if isinstance(node,Program):
        print(p+"Program"); [ast_to_text(x,indent+1) for x in node.statements]
    elif isinstance(node,Assign): print(p+f"Assign({node.name}, declared={node.declared_type})"); ast_to_text(node.expr,indent+1)
    elif isinstance(node,Print): print(p+"Print"); ast_to_text(node.expr,indent+1)
    elif isinstance(node,Literal): print(p+f"Literal({node.value!r}, {node.type_name})")
    elif isinstance(node,Var): print(p+f"Var({node.name})")
    elif isinstance(node,Binary): print(p+f"Binary({node.op})"); ast_to_text(node.left,indent+1); ast_to_text(node.right,indent+1)
    elif isinstance(node,Unary): print(p+f"Unary({node.op})"); ast_to_text(node.operand,indent+1)
    elif isinstance(node,If): print(p+"If"); ast_to_text(node.condition,indent+1); ast_to_text(node.then_block,indent+1); (ast_to_text(node.else_block,indent+1) if node.else_block else None)
    elif isinstance(node,While): print(p+"While"); ast_to_text(node.condition,indent+1); ast_to_text(node.body,indent+1)
    elif isinstance(node,Block): print(p+"Block"); [ast_to_text(x,indent+1) for x in node.statements]
    elif isinstance(node,Function): print(p+f"Function({node.name})"); ast_to_text(node.body,indent+1)
    elif isinstance(node,ClassDef): print(p+f"Class({node.name})")
    else: print(p+type(node).__name__)

# ============================================================
# 8. USER-FACING HELPERS
# ============================================================

def compile_source(source):
    """Compile BanglaBhasha source and return a CompilationResult."""
    return Compiler().compile(source)

def run_source(source):
    """Compile and execute source; returns (result, output)."""
    return Compiler().compile_and_run(source)

def save_python(source, filename="generated_bangla.py"):
    """Compile source and save generated Python code if compilation succeeds."""
    result=compile_source(source)
    if not result.success:
        return result
    with open(filename,"w",encoding="utf-8") as f:
        f.write(result.python_code)
    return result

def show_pipeline(source):
    """Display tokens, AST, semantic result, TAC and generated Python."""
    result=compile_source(source)
    print("="*72); print("1. TOKENS"); print("="*72); print_tokens(result.tokens)
    print("\n"+"="*72); print("2. AST"); print("="*72); ast_to_text(result.ast)
    print("\n"+"="*72); print("3. SEMANTIC ANALYSIS"); print("="*72)
    if result.errors:
        print("Errors:"); print("\n".join("- "+e for e in result.errors))
        return result
    print("No semantic errors.")
    print("\n"+"="*72); print("4. THREE-ADDRESS CODE (TAC)"); print("="*72); print_tac(result.tac)
    print("\n"+"="*72); print("5. GENERATED PYTHON"); print("="*72); print(result.python_code)
    return result

# ============================================================
# 8. DEMO
# ============================================================

DEMO_SOURCE = '''
পূর্ণসংখ্যা x = 10;
দশমিক y = 2.5;
স্ট্রিং নাম = "BanglaBhasha";
বুলিয়ান চালু = সত্য;

ফাংশন যোগ(পূর্ণসংখ্যা a, পূর্ণসংখ্যা b) -> পূর্ণসংখ্যা {
    ফেরত a + b;
}

যদি (x > 5 এবং চালু) {
    লেখো(নাম);
    লেখো(যোগ(x, 5));
} নাহলে {
    লেখো("শর্ত মিথ্যা");
}

যতক্ষণ (x < 13) {
    লেখো(x);
    x = x + 1;
}

স্ট্যাক s;
s.ঠেলো(100);
s.ঠেলো(200);
লেখো(s.সামনে_দেখো());
লেখো(s.বের_করো());

কিউ q;
q.ঢোকাও("A");
q.ঢোকাও("B");
লেখো(q.সামনে_দেখো_কিউ());
লেখো(q.বের_করো_কিউ());

ক্লাস ব্যক্তি {
    স্ট্রিং নাম = "অজানা";
    ফাংশন নাম_সেট(নিজে, স্ট্রিং নতুননাম) {
        নিজে.নাম = নতুননাম;
    }
    ফাংশন পরিচয়(নিজে) {
        লেখো(নিজে.নাম);
    }
}

ব্যক্তি১ = নতুন ব্যক্তি();
ব্যক্তি১.নাম_সেট("বাংলা প্রোগ্রামার");
ব্যক্তি১.পরিচয়();
'''

if __name__ == "__main__":
    c=Compiler(); result,out=c.compile_and_run(DEMO_SOURCE)
    if not result.success:
        print("Compilation failed:")
        print("\n".join(result.errors))
    else:
        print("=== OUTPUT ==="); print(out)
        print("=== GENERATED PYTHON ==="); print(result.python_code)
