# BanglaBhasha Compiler

A complete **toy compiler for an originally invented Bangla programming language**, implemented in Python.

> **Project goal:** A user writes source code in BanglaBhasha. The compiler performs lexical analysis, parsing, semantic analysis, generates Three-Address Code (TAC), translates the program into executable Python code, and can then execute the generated Python.

---

## 1. Compiler Pipeline

```text
                 BanglaBhasha Source Code
                           │
                           ▼
                    ┌─────────────┐
                    │    Lexer    │
                    └──────┬──────┘
                           │ Tokens
                           ▼
                    ┌─────────────┐
                    │   Parser    │
                    └──────┬──────┘
                           │ AST
                           ▼
                 ┌───────────────────┐
                 │ Semantic Analyzer │
                 │   + Symbol Table  │
                 └─────────┬─────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │     TAC     │
                    │     / IR     │
                    └──────┬──────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │  Python Backend  │
                 └────────┬─────────┘
                          │
                          ▼
                    Generated .py
                          │
                          ▼
                     Python exec()
                          │
                          ▼
                        Output
```

The implementation is intentionally organized into compiler phases rather than performing simple Bangla-to-Python keyword replacement.

---

# 2. Project Structure

```text
BanglaBhasha_Compiler_Project/
│
├── bangla_compiler.py
├── BanglaBhasha_Compiler.ipynb
└── README_BanglaBhasha.md
```

### `bangla_compiler.py`

The complete compiler in one Python source file.

### `BanglaBhasha_Compiler.ipynb`

Google Colab/Jupyter version of the same compiler, divided into logical cells so that each compiler phase can be demonstrated separately.

---

# 3. Implemented Compiler Features

## 3.1 Lexical Analysis

The lexer recognizes:

- Bangla/Unicode identifiers
- Integer literals
- Floating-point literals
- String literals
- Boolean literals
- Arithmetic operators
- Comparison operators
- Logical operators
- Assignment operator
- Parentheses
- Braces
- Commas
- Semicolons
- Dot/member-access operator
- Square brackets for list literals
- `->` for function return-type syntax
- New lines

### Comments

Both of these comment forms are recognized:

```text
// this is a comment
# this is also a comment
```

---

# 4. Data Types

The language currently supports four explicitly declared data types.

| Bangla type | Internal type | Example |
|---|---|---|
| `পূর্ণসংখ্যা` | `int` | `পূর্ণসংখ্যা x = 10;` |
| `দশমিক` | `float` | `দশমিক x = 3.14;` |
| `বুলিয়ান` | `bool` | `বুলিয়ান ok = সত্য;` |
| `স্ট্রিং` | `string` | `স্ট্রিং name = "Sahabi";` |

The compiler also uses internal types such as:

```text
list
stack
queue
void
any
error
```

These are internal semantic categories rather than additional explicit primitive declarations.

---

# 5. Variable Declaration

## Explicit declaration

```text
পূর্ণসংখ্যা বয়স = 22;
দশমিক উচ্চতা = 5.8;
বুলিয়ান ছাত্র = সত্য;
স্ট্রিং নাম = "Sahabi";
```

## Declaration without an initializer

Typed variables can be declared without an initial value:

```text
পূর্ণসংখ্যা x;
দশমিক y;
বুলিয়ান flag;
স্ট্রিং text;
```

They receive these default values:

```text
পূর্ণসংখ্যা → 0
দশমিক → 0.0
বুলিয়ান → মিথ্যা
স্ট্রিং → ""
```

## Type-inferred declaration

`ধরি` requires an initial value:

```text
ধরি x = 100;
ধরি name = "Bangla";
```

This declaration infers the type from the expression.

This is invalid:

```text
ধরি x;
```

because `ধরি` requires an initial value.

---

# 6. Assignment

After a variable has been declared, assignment can be written as:

```text
x = 20;
name = "BanglaBhasha";
```

The semantic analyzer checks assignments against an existing variable type.

An integer can be assigned to a float variable:

```text
দশমিক x = 10;
```

because the compiler treats:

```text
int → float
```

as a compatible widening conversion.

Other incompatible assignments generate a semantic error.

Example:

```text
পূর্ণসংখ্যা x = "hello";
```

produces a type-mismatch error.

---

# 7. Output

The output statement is:

```text
লেখো(expression);
```

Examples:

```text
লেখো(10);
লেখো(x);
লেখো("Hello");
লেখো(x + 5);
```

It is translated to Python `print(...)`.

---

# 8. Arithmetic Operators

Supported arithmetic operators:

```text
+
-
*
/
%
```

The parser implements operator precedence.

The precedence structure is:

```text
OR
 ↓
AND
 ↓
Equality: == !=
 ↓
Comparison: < <= > >=
 ↓
Term: + -
 ↓
Factor: * / %
 ↓
Unary: - !
 ↓
Postfix: function call / member access
 ↓
Primary: literal / variable / new / list / (...)
```

Therefore:

```text
পূর্ণসংখ্যা x = 2 + 3 * 4;
```

is interpreted as:

```text
2 + (3 * 4)
```

not:

```text
(2 + 3) * 4
```

---

# 9. Comparison Operators

Supported comparisons:

```text
==
!=
<
<=
>
>=
```

Comparison expressions produce a boolean result.

Example:

```text
যদি (x >= 10) {
    লেখো("x is at least 10");
}
```

---

# 10. Boolean Values and Logical Operators

Boolean literals:

```text
সত্য
মিথ্যা
```

Logical operators:

```text
এবং
অথবা
নয়
```

The symbolic form `!` is also recognized as logical NOT. The lexer also recognizes `&&` and `||`, but the current semantic/backend pipeline does not treat those two symbolic forms as supported source-language operators, so use `এবং` and `অথবা` in valid programs.

Example:

```text
বুলিয়ান a = সত্য;
বুলিয়ান b = মিথ্যা;

যদি (a এবং নয় b) {
    লেখো("Condition is true");
}
```

Boolean conditions are required for `যদি` and `যতক্ষণ`.

---

# 11. IF-ELSE

Syntax:

```text
যদি (condition) {
    statements
} নাহলে {
    statements
}
```

Example:

```text
পূর্ণসংখ্যা x = 10;

যদি (x > 5) {
    লেখো("বড়");
} নাহলে {
    লেখো("ছোট");
}
```

The generated Python uses normal Python `if/else` statements.

---

# 12. WHILE Loop

Syntax:

```text
যতক্ষণ (condition) {
    statements
}
```

Example:

```text
পূর্ণসংখ্যা i = 0;

যতক্ষণ (i < 5) {
    লেখো(i);
    i = i + 1;
}
```

The generated Python contains an equivalent `while` loop.

---

# 13. Break

The keyword:

```text
থামো;
```

is translated to Python `break`.

Example:

```text
পূর্ণসংখ্যা i = 0;

যতক্ষণ (i < 10) {
    যদি (i == 5) {
        থামো;
    }
    লেখো(i);
    i = i + 1;
}
```

The semantic analyzer reports an error if `থামো` is used outside a loop.

---

# 14. Functions

Functions can have typed or untyped parameters.

Syntax:

```text
ফাংশন functionName(parameters) -> returnType {
    statements
}
```

Example:

```text
ফাংশন যোগ(পূর্ণসংখ্যা a, পূর্ণসংখ্যা b) -> পূর্ণসংখ্যা {
    ফেরত a + b;
}

লেখো(যোগ(10, 20));
```

A function may also omit the return type:

```text
ফাংশন greet(স্ট্রিং name) {
    লেখো(name);
}
```

The function is translated into a Python `def`.

### Return

```text
ফেরত expression;
```

or:

```text
ফেরত;
```

The semantic analyzer checks a declared function return type against the returned expression.

---

# 15. Classes and Objects

The compiler supports a basic toy class system.

Syntax:

```text
ক্লাস ClassName {
    field declarations

    ফাংশন methodName(নিজে, parameters) {
        statements
    }
}
```

Example:

```text
ক্লাস ব্যক্তি {
    স্ট্রিং নাম = "অজানা";

    ফাংশন নাম_সেট(নিজে, স্ট্রিং নতুননাম) {
        নিজে.নাম = নতুননাম;
    }

    ফাংশন পরিচয়(নিজে) {
        লেখো(নিজে.নাম);
    }
}
```

Object creation:

```text
ব্যক্তি১ = নতুন ব্যক্তি();
```

Method call:

```text
ব্যক্তি১.নাম_সেট("Sahabi");
ব্যক্তি১.পরিচয়();
```

### `নিজে`

Inside a method, the Bangla keyword:

```text
নিজে
```

maps to Python's conventional:

```text
self
```

### Current class scope

This is intentionally a simple toy OOP system.

Currently supported:

- Class declaration
- Class fields
- Methods
- `নিজে`
- Object creation with `নতুন`
- Member access
- Method calls
- Member assignment

Currently **not** implemented:

- Inheritance
- Constructors such as `__init__`
- Access modifiers
- Method overloading
- Interfaces
- Static methods

Therefore object creation should currently be written without constructor arguments:

```text
p = নতুন ব্যক্তি();
```

rather than:

```text
p = নতুন ব্যক্তি("Sahabi");
```

---

# 16. Stack

A built-in stack class is included in the generated Python runtime.

Declaration:

```text
স্ট্যাক s;
```

Operations:

```text
s.ঠেলো(value);
s.বের_করো();
s.সামনে_দেখো();
s.খালি();
s.আকার();
```

Example:

```text
স্ট্যাক s;

s.ঠেলো(100);
s.ঠেলো(200);

লেখো(s.সামনে_দেখো());
লেখো(s.বের_করো());
```

The stack follows LIFO behavior:

```text
Last In → First Out
```

An empty `বের_করো()` or `সামনে_দেখো()` returns `None` rather than crashing.

---

# 17. Queue

A built-in queue class is included in the generated Python runtime.

Declaration:

```text
কিউ q;
```

Operations:

```text
q.ঢোকাও(value);
q.বের_করো_কিউ();
q.সামনে_দেখো_কিউ();
q.খালি();
q.আকার();
```

Example:

```text
কিউ q;

q.ঢোকাও("A");
q.ঢোকাও("B");

লেখো(q.সামনে_দেখো_কিউ());
লেখো(q.বের_করো_কিউ());
```

The queue follows FIFO behavior:

```text
First In → First Out
```

An empty dequeue/front operation returns `None`.

---

# 18. Lists

List literals are supported:

```text
[1, 2, 3]
```

Example:

```text
ধরি numbers = [10, 20, 30];
লেখো(numbers);
```

The current compiler supports list literal creation and output, but it does **not** implement general list indexing or list-specific language keywords.

---

# 19. Identifiers

Bangla/Unicode identifiers are supported.

Examples:

```text
পূর্ণসংখ্যা বয়স = 20;
পূর্ণসংখ্যা সংখ্যা = 100;
স্ট্রিং নাম = "Sahabi";
```

The lexer accepts Unicode letters, combining marks, Unicode numbers, and `_` as identifier characters.

Python 3 also supports Unicode identifiers, allowing many Bangla names to remain unchanged in generated Python.

---

# 20. Statement Termination

A normal statement may end with:

```text
;
```

or a newline.

Examples:

```text
পূর্ণসংখ্যা x = 10;
লেখো(x);
```

Newline termination is also accepted:

```text
পূর্ণসংখ্যা x = 10
লেখো(x)
```

A block is enclosed by:

```text
{
    ...
}
```

---

# 21. Error Handling

The compiler is designed to report errors instead of allowing compiler-stage exceptions to terminate the whole compilation unexpectedly.

## Lexical errors

Example:

```text
পূর্ণসংখ্যা x = 10 @ 5;
```

The lexer reports the unknown character.

## Syntax errors

Example:

```text
পূর্ণসংখ্যা x = ;
```

The parser reports the unexpected token.

The parser has basic error recovery: after a syntax problem it attempts to synchronize at a semicolon, newline, closing brace, or end of file.

## Semantic errors

Example:

```text
পূর্ণসংখ্যা x = "hello";
```

The semantic analyzer reports a type mismatch.

Another example:

```text
লেখো(y);
```

if `y` has not been defined.

The compiler does not generate target Python when lexical, syntax, or semantic errors remain.

---

# 22. Three-Address Code (TAC)

The compiler contains an intermediate representation based on Three-Address Code.

Example source:

```text
পূর্ণসংখ্যা x = 2 + 3 * 4;
```

is represented conceptually as:

```text
t0 = 3 * 4
t1 = 2 + t0
x = t1
```

The TAC generator also represents:

- assignments
- arithmetic operations
- unary operations
- conditional jumps
- labels
- loops
- function calls
- returns
- functions
- classes
- object creation
- stack/queue creation
- method calls
- break

TAC can be displayed with:

```python
print_tac(result.tac)
```

---

# 23. Generated Python

The Python backend converts the validated AST into Python source code.

Example BanglaBhasha:

```text
পূর্ণসংখ্যা x = 10;

যদি (x > 5) {
    লেখো(x);
}
```

is generated approximately as:

```python
x = 10

if x > 5:
    print(x)
```

The actual generated file also contains the runtime definitions needed for the built-in BanglaBhasha stack and queue.

---

# 24. Compiler API

The main user-facing functions are:

```python
compile_source(source)
```

Compile source code and return a `CompilationResult`.

```python
run_source(source)
```

Compile and execute the source.

It returns:

```text
(result, output)
```

```python
save_python(source, filename="generated_bangla.py")
```

Compile the source and save generated Python if compilation succeeds.

```python
show_pipeline(source)
```

Display:

```text
Tokens
AST
Semantic Analysis
TAC
Generated Python
```

---

# 25. Compilation Result

`CompilationResult` stores:

```text
source
tokens
ast
semantic
tac
python_code
errors
warnings
```

Compilation succeeds when:

```python
result.success
```

is `True`.

Otherwise:

```python
result.errors
```

contains the compiler errors.

---

# 26. Complete Example

```text
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
```

---

# 27. Running in Google Colab

1. Open Google Colab.
2. Upload:

```text
BanglaBhasha_Compiler.ipynb
```

3. Run the cells from top to bottom.
4. Modify `DEMO_SOURCE` with your own BanglaBhasha program.
5. Run the compile/run cell.

The notebook also contains small regression tests for:

- arithmetic precedence
- type checking
- boolean conditions
- while loops
- functions
- classes
- type errors

No third-party Python package is required.

---

# 28. Running as a Python File

With Python 3 installed:

```bash
python bangla_compiler.py
```

The file contains a built-in demonstration program.

You can also use the compiler from another Python program:

```python
from bangla_compiler import compile_source, run_source

source = """
পূর্ণসংখ্যা x = 10;
লেখো(x + 5);
"""

result, output = run_source(source)

if result.success:
    print(output)
else:
    print("\n".join(result.errors))
```

---

# 29. Language Keyword Reference

| Keyword | Meaning |
|---|---|
| `ধরি` | type-inferred variable declaration |
| `পূর্ণসংখ্যা` | integer type |
| `দশমিক` | floating-point type |
| `বুলিয়ান` | boolean type |
| `স্ট্রিং` | string type |
| `লেখো` | print |
| `যদি` | if |
| `নাহলে` | else |
| `যতক্ষণ` | while |
| `থামো` | break |
| `ফাংশন` | function |
| `ফেরত` | return |
| `ক্লাস` | class |
| `নতুন` | object creation |
| `নিজে` | method self reference |
| `সত্য` | true |
| `মিথ্যা` | false |
| `স্ট্যাক` | stack declaration |
| `কিউ` | queue declaration |
| `ঠেলো` | stack push |
| `বের_করো` | stack pop |
| `সামনে_দেখো` | stack peek |
| `ঢোকাও` | queue enqueue |
| `বের_করো_কিউ` | queue dequeue |
| `সামনে_দেখো_কিউ` | queue front |
| `এবং` | logical AND |
| `অথবা` | logical OR |
| `নয়` | logical NOT |

---

# 30. Current Scope and Deliberate Limitations

This is a **toy compiler for a Compiler Design course**, not a production programming language.

The current implementation does not provide:

- inheritance
- constructors with arguments
- access modifiers
- exception syntax in Bangla
- for loops
- switch/case
- general list indexing
- list mutation syntax
- modules/imports
- a full standard library
- static method support
- method overloading
- full function-argument type checking
- a separate machine-code/runtime implementation

These are suitable candidates for future versions rather than requirements of the current implementation.

---

# 31. Design Rationale

The project is deliberately structured around classical compiler concepts:

```text
Lexical Analysis
       ↓
Syntax Analysis
       ↓
Abstract Syntax Tree
       ↓
Semantic Analysis
       ↓
Intermediate Representation
       ↓
Target Code Generation
       ↓
Execution
```

This makes the project demonstrable as a **compiler construction project**, rather than only as a translator.

The Bangla syntax is the user-facing language layer; Python is the target language.

---

# 32. Suggested Demonstration Order

For a project presentation/demo, a practical sequence is:

### Demo 1 — Basic program

```text
পূর্ণসংখ্যা x = 10;
লেখো(x + 5);
```

Show:

```text
Bangla Source
      ↓
Tokens
      ↓
AST
      ↓
TAC
      ↓
Generated Python
      ↓
15
```

### Demo 2 — Type checking

```text
পূর্ণসংখ্যা x = "hello";
```

Show the semantic error.

### Demo 3 — IF-ELSE

```text
যদি (x > 5) {
    লেখো("YES");
} নাহলে {
    লেখো("NO");
}
```

### Demo 4 — WHILE

Show a loop printing several values.

### Demo 5 — Function

Show:

```text
ফাংশন যোগ(...) -> পূর্ণসংখ্যা
```

and the generated Python `def`.

### Demo 6 — Advanced feature

Show either:

```text
স্ট্যাক
```

or:

```text
ক্লাস + অবজেক্ট
```

This gives the audience a clear progression from the required compiler features to the advanced features.

---

# 33. Project Status

### Minimum compiler requirements

- [x] Multiple data types
- [x] Type checking
- [x] Arithmetic operations
- [x] Operator precedence
- [x] Assignment
- [x] IF-ELSE
- [x] WHILE
- [x] Syntax error recovery
- [x] Graceful compiler errors
- [x] Executable Python target generation

### Advanced features

- [x] Functions
- [x] Return statements
- [x] Classes
- [x] Objects
- [x] Stack
- [x] Queue
- [x] Boolean operators
- [x] Lists
- [x] Break
- [x] Bangla Unicode identifiers
- [x] Comments

---

# 34. License / Academic Use

This project is intended as an academic Compiler Design project.

