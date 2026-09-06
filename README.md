# 🇧🇩 BanglaBhasha Compiler

A custom **Bengali programming language compiler** built in Python.

BanglaBhasha allows programmers to write source code using Bangla keywords and Unicode identifiers. The compiler processes the source through a complete compiler pipeline including **lexical analysis, parsing, semantic analysis, symbol-table management, Three-Address Code generation, Python code generation, and execution**.

The project also includes an **interactive web-based compiler playground** where users can write BanglaBhasha code and visually inspect every stage of compilation.

---

## 🚀 Features

### Compiler Features

* ✅ Lexical Analysis
* ✅ Token Generation
* ✅ Recursive-Descent Parsing
* ✅ Abstract Syntax Tree (AST)
* ✅ Semantic Analysis
* ✅ Symbol Table
* ✅ Static Type Checking
* ✅ Three-Address Code (TAC / IR)
* ✅ Python Code Generation
* ✅ Runtime Execution
* ✅ Syntax Error Recovery
* ✅ Semantic Error Reporting
* ✅ Unicode Bangla Identifiers

### Language Features

* ✅ Integer, Float, Boolean and String types
* ✅ Type-inferred variables
* ✅ Arithmetic operations
* ✅ Operator precedence
* ✅ Comparison operators
* ✅ Logical operators
* ✅ `if-else`
* ✅ `while`
* ✅ `break`
* ✅ Functions
* ✅ Return statements
* ✅ Classes
* ✅ Objects
* ✅ Member access
* ✅ Method calls
* ✅ Stack
* ✅ Queue
* ✅ List literals
* ✅ Comments
* ✅ Bangla variable and function names

### Web Playground

The project includes an interactive browser-based IDE with:

* 📝 BanglaBhasha source-code editor
* ▶️ Compile & Run controls
* 🔍 Token viewer
* 🌳 Interactive AST visualization
* 📋 Symbol table viewer
* ⚙️ TAC / Intermediate Representation viewer
* 🐍 Generated Python viewer
* 🖥️ Runtime output console
* ⚠️ Compiler error display
* 📚 Built-in sample programs
* ⌨️ Bangla syntax quick-insert buttons
* 🌗 Light/Dark theme

---

# 🧠 Compiler Pipeline

```text
BanglaBhasha Source Code
          │
          ▼
     ┌─────────┐
     │  Lexer  │
     └────┬────┘
          │ Tokens
          ▼
     ┌─────────┐
     │ Parser  │
     └────┬────┘
          │
          ▼
          AST
          │
          ▼
 ┌───────────────────┐
 │ Semantic Analyzer │
 │   + Symbol Table  │
 └─────────┬─────────┘
           │
           ▼
     ┌───────────┐
     │ TAC / IR  │
     └─────┬─────┘
           │
           ▼
 ┌─────────────────┐
 │ Python Backend  │
 └────────┬────────┘
          │
          ▼
   Generated Python
          │
          ▼
       Execution
          │
          ▼
        Output
```

BanglaBhasha is therefore more than a simple keyword translator. It is structured around the major phases commonly studied in **Compiler Design**.

---

# 📁 Project Structure

```text
BanglaBhasha-Compiler/
│
├── bangla_compiler.py
├── server.py
├── run_demo.bat
├── BanglaBhasha_Compiler.ipynb
├── generated_bangla.py
├── README.md
├── .gitignore
│
├── examples/
│   ├── 01_sum_and_loops.bn
│   ├── 02_factorial.bn
│   ├── 03_fibonacci.bn
│   ├── 04_student_oop.bn
│   ├── 05_stack_and_queue.bn
│   └── 06_prime_checker.bn
│
└── web/
    ├── index.html
    ├── app.js
    └── style.css
```

### `bangla_compiler.py`

Core compiler implementation containing:

* Lexer
* Parser
* AST definitions
* Semantic analyzer
* Symbol table
* TAC generator
* Python backend
* Compiler API

### `server.py`

Zero-dependency local HTTP server used by the interactive web compiler.

### `web/`

Frontend of the interactive BanglaBhasha compiler playground.

### `BanglaBhasha_Compiler.ipynb`

Jupyter / Google Colab version of the compiler for demonstration and academic presentation.

### `examples/`

Ready-to-run `.bn` BanglaBhasha programs.

---

# ⚡ Quick Start

## 1. Clone the Repository

```bash
git clone https://github.com/therash08/BanglaBhasha-Compiler.git
cd BanglaBhasha-Compiler
```

Python 3 is required.

No third-party Python package is required for the core compiler or local web server.

---

# 🌐 Run the Interactive Web Compiler

Start the server:

```bash
python server.py
```

Then open:

```text
http://localhost:5000
```

You can now write BanglaBhasha code directly in the browser and inspect:

```text
Source
  ↓
Tokens
  ↓
AST
  ↓
Semantic Analysis
  ↓
Symbol Table
  ↓
TAC
  ↓
Generated Python
  ↓
Program Output
```

---

## Windows Quick Start

Windows users can simply run:

```text
run_demo.bat
```

The script starts the compiler server and opens the playground in the browser.

---

# 🐍 Run the Compiler Directly

You can also run:

```bash
python bangla_compiler.py
```

This executes the built-in demonstration program.

---

# 🇧🇩 BanglaBhasha Example

```text
পূর্ণসংখ্যা x = 10;
দশমিক y = 2.5;
স্ট্রিং নাম = "BanglaBhasha";
বুলিয়ান চালু = সত্য;

যদি (x > 5 এবং চালু) {
    লেখো(নাম);
    লেখো(x + 5);
} নাহলে {
    লেখো("শর্ত মিথ্যা");
}
```

Equivalent generated Python is approximately:

```python
x = 10
y = 2.5
নাম = "BanglaBhasha"
চালু = True

if x > 5 and চালু:
    print(নাম)
    print(x + 5)
else:
    print("শর্ত মিথ্যা")
```

---

# 📦 Data Types

BanglaBhasha currently supports four explicitly declared primitive types.

| Bangla Type   | Internal Type | Example                   |
| ------------- | ------------- | ------------------------- |
| `পূর্ণসংখ্যা` | `int`         | `পূর্ণসংখ্যা x = 10;`     |
| `দশমিক`       | `float`       | `দশমিক x = 3.14;`         |
| `বুলিয়ান`     | `bool`        | `বুলিয়ান ok = সত্য;`      |
| `স্ট্রিং`     | `string`      | `স্ট্রিং name = "বাংলা";` |

The compiler also uses internal semantic categories including:

```text
list
stack
queue
void
any
error
```

---

# 📌 Variable Declaration

## Explicit Type

```text
পূর্ণসংখ্যা বয়স = 22;
দশমিক উচ্চতা = 5.8;
বুলিয়ান ছাত্র = সত্য;
স্ট্রিং নাম = "Rahim";
```

---

## Declaration Without Initial Value

```text
পূর্ণসংখ্যা x;
দশমিক y;
বুলিয়ান flag;
স্ট্রিং text;
```

Default values:

```text
পূর্ণসংখ্যা → 0
দশমিক → 0.0
বুলিয়ান → মিথ্যা
স্ট্রিং → ""
```

---

## Type Inference

Use:

```text
ধরি
```

Example:

```text
ধরি x = 100;
ধরি নাম = "বাংলা";
ধরি numbers = [1, 2, 3];
```

The compiler infers the variable type from the expression.

This is invalid:

```text
ধরি x;
```

because a type-inferred declaration requires an initial value.

---

# ✏️ Assignment

```text
পূর্ণসংখ্যা x = 10;

x = 20;
```

The semantic analyzer checks whether the assigned value is compatible with the variable type.

For example:

```text
পূর্ণসংখ্যা x = "hello";
```

produces a semantic type error.

The compiler permits integer-to-float widening:

```text
দশমিক x = 10;
```

---

# 🖨️ Output

BanglaBhasha uses:

```text
লেখো(expression);
```

Examples:

```text
লেখো(10);
লেখো(x);
লেখো("Hello BanglaBhasha");
লেখো(x + 5);
```

This is translated into Python:

```python
print(...)
```

---

# ➕ Arithmetic Operators

Supported operators:

```text
+
-
*
/
%
```

Example:

```text
পূর্ণসংখ্যা x = 2 + 3 * 4;
```

Operator precedence means it is interpreted as:

```text
2 + (3 * 4)
```

---

# ⚙️ Operator Precedence

```text
OR
 ↓
AND
 ↓
Equality
== !=
 ↓
Comparison
< <= > >=
 ↓
Addition / Subtraction
+ -
 ↓
Multiplication / Division / Modulo
* / %
 ↓
Unary
- !
 ↓
Function / Method Call
 ↓
Primary Expression
```

---

# 🔎 Comparison Operators

Supported comparison operators:

```text
==
!=
<
<=
>
>=
```

Example:

```text
যদি (x >= 10) {
    লেখো("x is at least 10");
}
```

Comparison expressions evaluate to Boolean values.

---

# 🔘 Boolean Values

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

Example:

```text
বুলিয়ান a = সত্য;
বুলিয়ান b = মিথ্যা;

যদি (a এবং নয় b) {
    লেখো("Condition is true");
}
```

---

# 🔀 IF-ELSE

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

---

# 🔄 WHILE Loop

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

---

# 🛑 Break

Use:

```text
থামো;
```

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

Using `থামো` outside a loop generates a semantic error.

---

# 🧩 Functions

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

Functions may also omit an explicit return type:

```text
ফাংশন greet(স্ট্রিং name) {
    লেখো(name);
}
```

---

# ↩️ Return

Return a value:

```text
ফেরত expression;
```

Example:

```text
ফেরত a + b;
```

Or return without a value:

```text
ফেরত;
```

The semantic analyzer checks declared function return types.

---

# 🏛️ Classes and Objects

BanglaBhasha includes a simple object-oriented programming system.

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

Create an object:

```text
ব্যক্তি১ = নতুন ব্যক্তি();
```

Call methods:

```text
ব্যক্তি১.নাম_সেট("Rahim");
ব্যক্তি১.পরিচয়();
```

---

## `নিজে`

Inside methods:

```text
নিজে
```

corresponds conceptually to Python's:

```python
self
```

---

## Current OOP Support

Supported:

* Class declaration
* Fields
* Methods
* Object creation
* Member access
* Member assignment
* Method calls
* `নিজে`

Not currently implemented:

* Inheritance
* Constructor arguments
* Access modifiers
* Interfaces
* Method overloading
* Static methods

---

# 📚 Stack

Declare a stack:

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

The stack follows:

```text
LIFO
Last In → First Out
```

---

# 📥 Queue

Declare a queue:

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

The queue follows:

```text
FIFO
First In → First Out
```

---

# 📋 Lists

List literals are supported.

```text
ধরি numbers = [10, 20, 30];

লেখো(numbers);
```

General list indexing and list mutation syntax are not currently implemented.

---

# 🔤 Unicode Identifiers

Bangla identifiers can be used directly.

Example:

```text
পূর্ণসংখ্যা বয়স = 20;
পূর্ণসংখ্যা সংখ্যা = 100;
স্ট্রিং নাম = "বাংলাভাষা";
```

The lexer supports Unicode letters, combining marks, numbers and underscores.

---

# 💬 Comments

Two comment styles are supported.

```text
// comment
```

and:

```text
# comment
```

Example:

```text
# একটি সংখ্যা তৈরি করছি
পূর্ণসংখ্যা x = 10;

// ফলাফল দেখাও
লেখো(x);
```

---

# 🔚 Statement Termination

Statements may be terminated using:

```text
;
```

Example:

```text
পূর্ণসংখ্যা x = 10;
লেখো(x);
```

Newlines are also supported in many normal statement contexts:

```text
পূর্ণসংখ্যা x = 10
লেখো(x)
```

Blocks use braces:

```text
{
    ...
}
```

---

# ⚠️ Error Handling

The compiler attempts to produce understandable compiler errors instead of crashing unexpectedly.

### Lexical Error

```text
পূর্ণসংখ্যা x = 10 @ 5;
```

The lexer reports the unknown character.

### Syntax Error

```text
পূর্ণসংখ্যা x = ;
```

The parser reports an unexpected token.

### Semantic Error

```text
পূর্ণসংখ্যা x = "hello";
```

The semantic analyzer reports a type mismatch.

Undefined variables are also detected:

```text
লেখো(y);
```

If compilation contains errors, target Python code is not executed normally.

---

# ⚙️ Three-Address Code

BanglaBhasha generates an intermediate representation based on **Three-Address Code**.

Example:

```text
পূর্ণসংখ্যা x = 2 + 3 * 4;
```

Conceptually becomes:

```text
t0 = 3 * 4
t1 = 2 + t0
x = t1
```

The TAC generator represents operations including:

* Assignments
* Arithmetic
* Unary operations
* Conditional jumps
* Labels
* Loops
* Function calls
* Returns
* Classes
* Object creation
* Stack / Queue operations
* Method calls
* Break statements

---

# 🐍 Python Code Generation

After successful semantic analysis, the compiler converts the AST into executable Python.

BanglaBhasha:

```text
পূর্ণসংখ্যা x = 10;

যদি (x > 5) {
    লেখো(x);
}
```

Generated Python:

```python
x = 10

if x > 5:
    print(x)
```

---

# 🔌 Compiler API

The compiler can also be imported from another Python program.

```python
from bangla_compiler import compile_source, run_source
```

---

## `compile_source`

```python
result = compile_source(source)
```

Compiles BanglaBhasha source and returns a `CompilationResult`.

---

## `run_source`

```python
result, output = run_source(source)
```

Compiles and executes the source code.

Example:

```python
from bangla_compiler import run_source

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

## `save_python`

```python
save_python(source, filename="generated_bangla.py")
```

Compiles the BanglaBhasha program and saves generated Python code.

---

## `show_pipeline`

```python
show_pipeline(source)
```

Displays compiler stages including:

```text
Tokens
AST
Semantic Analysis
TAC
Generated Python
```

---

# 📊 Compilation Result

A compilation result can contain:

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

Check compilation success:

```python
result.success
```

Compiler errors are available through:

```python
result.errors
```

---

# 🧪 Example Programs

The repository contains several ready-made BanglaBhasha programs.

| File                    | Demonstrates                            |
| ----------------------- | --------------------------------------- |
| `01_sum_and_loops.bn`   | Variables, arithmetic and loops         |
| `02_factorial.bn`       | Factorial calculation                   |
| `03_fibonacci.bn`       | Fibonacci sequence                      |
| `04_student_oop.bn`     | Classes and object-oriented programming |
| `05_stack_and_queue.bn` | Stack and Queue data structures         |
| `06_prime_checker.bn`   | Prime-number checking                   |

These files can be used for testing, classroom demonstrations and project presentations.

---

# 📓 Google Colab / Jupyter Notebook

The repository includes:

```text
BanglaBhasha_Compiler.ipynb
```

To use it:

1. Open Google Colab or Jupyter Notebook.
2. Upload/open the notebook.
3. Run the cells from top to bottom.
4. Modify the demo BanglaBhasha source.
5. Run the compiler.

The notebook is useful for explaining individual compiler phases during an academic presentation.

---

# 🔑 Language Keyword Reference

| Bangla Keyword   | Meaning                |
| ---------------- | ---------------------- |
| `ধরি`            | Type-inferred variable |
| `পূর্ণসংখ্যা`    | Integer                |
| `দশমিক`          | Float                  |
| `বুলিয়ান`        | Boolean                |
| `স্ট্রিং`        | String                 |
| `লেখো`           | Print                  |
| `যদি`            | If                     |
| `নাহলে`          | Else                   |
| `যতক্ষণ`         | While                  |
| `থামো`           | Break                  |
| `ফাংশন`          | Function               |
| `ফেরত`           | Return                 |
| `ক্লাস`          | Class                  |
| `নতুন`           | New object             |
| `নিজে`           | Self reference         |
| `সত্য`           | True                   |
| `মিথ্যা`         | False                  |
| `স্ট্যাক`        | Stack                  |
| `কিউ`            | Queue                  |
| `ঠেলো`           | Stack push             |
| `বের_করো`        | Stack pop              |
| `সামনে_দেখো`     | Stack peek             |
| `ঢোকাও`          | Queue enqueue          |
| `বের_করো_কিউ`    | Queue dequeue          |
| `সামনে_দেখো_কিউ` | Queue front            |
| `এবং`            | Logical AND            |
| `অথবা`           | Logical OR             |
| `নয়`             | Logical NOT            |

---

# 📌 Current Limitations

BanglaBhasha is currently an academic / educational compiler rather than a production programming language.

Features not currently implemented include:

* `for` loops
* `switch/case`
* inheritance
* constructor arguments
* access modifiers
* interfaces
* method overloading
* static methods
* modules/import system
* exception syntax
* general list indexing
* advanced list mutation
* full standard library
* native machine-code generation
* dedicated virtual machine/runtime

These provide possible directions for future development.

---

# 🎓 Academic Purpose

BanglaBhasha was designed as a **Compiler Design project** to demonstrate the classical phases of compiler construction using an original Bangla-based programming language.

The project demonstrates:

```text
Lexical Analysis
       ↓
Syntax Analysis
       ↓
Abstract Syntax Tree
       ↓
Semantic Analysis
       ↓
Symbol Table
       ↓
Intermediate Representation
       ↓
Target Code Generation
       ↓
Execution
```

Python is currently used as the target language.

---

# 🗺️ Possible Future Improvements

Possible future versions could include:

* `for` loop support
* Array / list indexing
* User-defined constructors
* Inheritance
* Exception handling
* Module system
* Standard library
* More advanced static type checking
* Optimized TAC
* Compiler optimization passes
* Bytecode backend
* Virtual machine
* Command-line compiler
* Package manager
* Syntax highlighting
* Online deployment of the web playground

---

# ✅ Project Status

### Core Compiler

* [x] Lexer
* [x] Parser
* [x] AST
* [x] Semantic analysis
* [x] Symbol table
* [x] Type checking
* [x] TAC generation
* [x] Python backend
* [x] Runtime execution
* [x] Error handling

### Language

* [x] Multiple primitive types
* [x] Variables
* [x] Type inference
* [x] Arithmetic
* [x] Comparisons
* [x] Logical operators
* [x] IF-ELSE
* [x] WHILE
* [x] Break
* [x] Functions
* [x] Return
* [x] Classes
* [x] Objects
* [x] Stack
* [x] Queue
* [x] Lists
* [x] Comments
* [x] Unicode identifiers

### Development Tools

* [x] Python compiler
* [x] Jupyter / Colab notebook
* [x] Interactive Web IDE
* [x] AST visualization
* [x] Symbol-table viewer
* [x] TAC viewer
* [x] Generated Python viewer
* [x] Example programs

---

# 🤝 Contributing

Contributions, improvements and suggestions are welcome.

You can:

1. Fork the repository.
2. Create a new branch.
3. Implement your improvement.
4. Test the compiler.
5. Submit a Pull Request.

Example:

```bash
git checkout -b feature/new-feature
git commit -m "Add new BanglaBhasha feature"
git push origin feature/new-feature
```

---

# 📄 License / Academic Use

This repository is currently intended primarily for educational and academic use.

If the project is going to be distributed or reused publicly, adding a dedicated `LICENSE` file such as the **MIT License** is recommended.

---

# 👨‍💻 Repository

**BanglaBhasha Compiler**

https://github.com/therash08/BanglaBhasha-Compiler

---

<p align="center">
  🇧🇩 <b>Programming concepts in Bangla — from source code to compiler pipeline.</b>
</p>
