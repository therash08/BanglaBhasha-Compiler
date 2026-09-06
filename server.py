# -*- coding: utf-8 -*-
"""
BanglaBhasha Compiler — Interactive Live Demo Backend Server
Zero-dependency HTTP server using Python standard library.
"""

import sys
import io
import os
import time
import json
import traceback
import contextlib
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# Ensure UTF-8 stdout/stderr
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Import compiler from local project
import bangla_compiler
from bangla_compiler import (
    Compiler, Program, Assign, Print, ExprStmt, Block, If, While,
    Break, Return, Function, Call, Member, MethodCall, New, ClassDef,
    StackCreate, QueueCreate, StackOp, ListLiteral, Literal, Var, Binary, Unary
)

PORT = 5000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


def ast_to_text(node, indent=0) -> str:
    """Format AST to indented textual representation."""
    if node is None:
        return ""
    p = "  " * indent
    lines = []
    if isinstance(node, Program):
        lines.append(p + "Program")
        for s in node.statements:
            lines.append(ast_to_text(s, indent + 1))
    elif isinstance(node, Assign):
        decl = f", declared={node.declared_type}" if node.declared_type else ""
        lines.append(p + f"Assign({node.name}{decl})")
        lines.append(ast_to_text(node.expr, indent + 1))
    elif isinstance(node, Print):
        lines.append(p + "Print")
        lines.append(ast_to_text(node.expr, indent + 1))
    elif isinstance(node, ExprStmt):
        lines.append(p + "ExprStmt")
        lines.append(ast_to_text(node.expr, indent + 1))
    elif isinstance(node, Literal):
        lines.append(p + f"Literal({node.value!r}, type={node.type_name})")
    elif isinstance(node, Var):
        lines.append(p + f"Var({node.name})")
    elif isinstance(node, Binary):
        lines.append(p + f"Binary('{node.op}')")
        lines.append(ast_to_text(node.left, indent + 1))
        lines.append(ast_to_text(node.right, indent + 1))
    elif isinstance(node, Unary):
        lines.append(p + f"Unary('{node.op}')")
        lines.append(ast_to_text(node.operand, indent + 1))
    elif isinstance(node, If):
        lines.append(p + "If")
        lines.append(p + "  Condition:")
        lines.append(ast_to_text(node.condition, indent + 2))
        lines.append(p + "  Then:")
        lines.append(ast_to_text(node.then_block, indent + 2))
        if node.else_block:
            lines.append(p + "  Else:")
            lines.append(ast_to_text(node.else_block, indent + 2))
    elif isinstance(node, While):
        lines.append(p + "While")
        lines.append(p + "  Condition:")
        lines.append(ast_to_text(node.condition, indent + 2))
        lines.append(p + "  Body:")
        lines.append(ast_to_text(node.body, indent + 2))
    elif isinstance(node, Block):
        lines.append(p + "Block")
        for s in node.statements:
            lines.append(ast_to_text(s, indent + 1))
    elif isinstance(node, Function):
        params_str = ", ".join(f"{p}:{t}" if t else p for p, t in node.params)
        ret_str = f" -> {node.return_type}" if node.return_type else ""
        lines.append(p + f"Function({node.name}({params_str}){ret_str})")
        lines.append(ast_to_text(node.body, indent + 1))
    elif isinstance(node, Return):
        lines.append(p + "Return")
        if node.expr:
            lines.append(ast_to_text(node.expr, indent + 1))
    elif isinstance(node, Break):
        lines.append(p + "Break")
    elif isinstance(node, Call):
        lines.append(p + f"Call")
        lines.append(ast_to_text(node.callee, indent + 1))
        for arg in node.args:
            lines.append(ast_to_text(arg, indent + 2))
    elif isinstance(node, Member):
        lines.append(p + f"Member(.{node.name})")
        lines.append(ast_to_text(node.object, indent + 1))
    elif isinstance(node, MethodCall):
        lines.append(p + f"MethodCall(.{node.name}())")
        lines.append(ast_to_text(node.object, indent + 1))
        for arg in node.args:
            lines.append(ast_to_text(arg, indent + 2))
    elif isinstance(node, New):
        lines.append(p + f"New({node.class_name})")
        for arg in node.args:
            lines.append(ast_to_text(arg, indent + 1))
    elif isinstance(node, ClassDef):
        lines.append(p + f"ClassDef({node.name})")
        for f in node.fields:
            lines.append(ast_to_text(f, indent + 1))
        for m in node.methods:
            lines.append(ast_to_text(m, indent + 1))
    elif isinstance(node, StackCreate):
        lines.append(p + f"StackCreate({node.name})")
    elif isinstance(node, QueueCreate):
        lines.append(p + f"QueueCreate({node.name})")
    elif isinstance(node, ListLiteral):
        lines.append(p + "ListLiteral")
        for el in node.elements:
            lines.append(ast_to_text(el, indent + 1))
    else:
        lines.append(p + type(node).__name__)
    return "\n".join(l for l in lines if l)


def ast_to_tree_node(node) -> dict:
    """Format AST to interactive tree node dict for UI visualization."""
    if node is None:
        return {"name": "None", "badge": "null", "children": []}
    
    t = type(node).__name__
    badge = "node"
    name = t
    detail = ""
    children = []

    if isinstance(node, Program):
        name = "প্রোগ্রাম (Program)"
        badge = "root"
        children = [ast_to_tree_node(s) for s in node.statements]
    elif isinstance(node, Assign):
        decl = f": {node.declared_type}" if node.declared_type else " (ধরি)"
        name = f"এসাইন = {node.name}{decl}"
        badge = "assign"
        children = [ast_to_tree_node(node.expr)]
    elif isinstance(node, Print):
        name = "লেখো (Print)"
        badge = "io"
        children = [ast_to_tree_node(node.expr)]
    elif isinstance(node, Literal):
        name = f"মান: {node.value!r}"
        detail = node.type_name
        badge = "literal"
    elif isinstance(node, Var):
        name = f"ভেরিয়েবল: {node.name}"
        badge = "ident"
    elif isinstance(node, Binary):
        name = f"অপারেশন '{node.op}'"
        badge = "op"
        children = [ast_to_tree_node(node.left), ast_to_tree_node(node.right)]
    elif isinstance(node, Unary):
        name = f"ইউনারি '{node.op}'"
        badge = "op"
        children = [ast_to_tree_node(node.operand)]
    elif isinstance(node, If):
        name = "যদি (If)"
        badge = "flow"
        cond = {"name": "শর্ত (Condition)", "badge": "cond", "children": [ast_to_tree_node(node.condition)]}
        then_b = {"name": "তাহলে (Then)", "badge": "block", "children": [ast_to_tree_node(node.then_block)]}
        children = [cond, then_b]
        if node.else_block:
            children.append({"name": "নাহলে (Else)", "badge": "block", "children": [ast_to_tree_node(node.else_block)]})
    elif isinstance(node, While):
        name = "যতক্ষণ (While)"
        badge = "flow"
        children = [
            {"name": "শর্ত (Condition)", "badge": "cond", "children": [ast_to_tree_node(node.condition)]},
            {"name": "লুপ বডি (Body)", "badge": "block", "children": [ast_to_tree_node(node.body)]}
        ]
    elif isinstance(node, Block):
        name = "ব্লক { ... }"
        badge = "block"
        children = [ast_to_tree_node(s) for s in node.statements]
    elif isinstance(node, Function):
        params_str = ", ".join(f"{p}:{t}" if t else p for p, t in node.params)
        ret_str = f" -> {node.return_type}" if node.return_type else ""
        name = f"ফাংশন {node.name}({params_str}){ret_str}"
        badge = "func"
        children = [ast_to_tree_node(node.body)]
    elif isinstance(node, Return):
        name = "ফেরত (Return)"
        badge = "flow"
        if node.expr:
            children = [ast_to_tree_node(node.expr)]
    elif isinstance(node, Break):
        name = "থামো (Break)"
        badge = "flow"
    elif isinstance(node, Call):
        name = "ফাংশন কল"
        badge = "call"
        children = [ast_to_tree_node(node.callee)] + [ast_to_tree_node(a) for a in node.args]
    elif isinstance(node, Member):
        name = f"মেম্বার .{node.name}"
        badge = "member"
        children = [ast_to_tree_node(node.object)]
    elif isinstance(node, MethodCall):
        name = f"মেথড কল .{node.name}()"
        badge = "call"
        children = [ast_to_tree_node(node.object)] + [ast_to_tree_node(a) for a in node.args]
    elif isinstance(node, New):
        name = f"নতুন (New) {node.class_name}()"
        badge = "oop"
        children = [ast_to_tree_node(a) for a in node.args]
    elif isinstance(node, ClassDef):
        name = f"ক্লাস {node.name}"
        badge = "class"
        children = [ast_to_tree_node(f) for f in node.fields] + [ast_to_tree_node(m) for m in node.methods]
    elif isinstance(node, StackCreate):
        name = f"স্ট্যাক তৈরি: {node.name}"
        badge = "ds"
    elif isinstance(node, QueueCreate):
        name = f"কিউ তৈরি: {node.name}"
        badge = "ds"
    else:
        name = str(node)

    return {"name": name, "detail": detail, "badge": badge, "children": children}


SAMPLE_PROGRAMS = {
    "full_demo": {
        "title": "🚀 সম্পূর্ণ ডেমো (Full Language Demo)",
        "desc": "ভেরিয়েবল, ফাংশন, কন্ডিশন, লুপ, স্ট্যাক, কিউ এবং অবজেক্ট ওরিয়েন্টেড ক্লাস সহ সম্পূর্ণ প্রোগ্রাম।",
        "code": '''পূর্ণসংখ্যা x = 10;
দশমিক y = 2.5;
স্ট্রিং নাম = "বাংলাভাষা";
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
q.ঢোকাও("প্রথম");
q.ঢোকাও("দ্বিতীয়");
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
    },
    "math_functions": {
        "title": "🧮 ফাংশন ও গণিত (Functions & Arithmetic)",
        "desc": "ফাংশন ডিক্লেয়ারেশন, প্যারামিটার টাইপ এবং গাণিতিক হিসাব।",
        "code": '''পূর্ণসংখ্যা গুণফল = 1;

ফাংশন গুণ(পূর্ণসংখ্যা a, পূর্ণসংখ্যা b) -> পূর্ণসংখ্যা {
    ফেরত a * b;
}

ফাংশন ক্ষেত্রফল(দশমিক ব্যাসার্ধ) -> দশমিক {
    ফেরত 3.1416 * ব্যাসার্ধ * ব্যাসার্ধ;
}

লেখো("৫ x ৪ এর গুণফল:");
লেখো(গুণ(5, 4));

দশমিক বৃত্ত = ক্ষেত্রফল(5.0);
লেখো("৫.০ ব্যাসার্ধের ক্ষেত্রফল:");
লেখো(বৃত্ত);
'''
    },
    "loops_and_conditionals": {
        "title": "🔄 শর্ত ও লুপ (If-Else & While Loops)",
        "desc": "নেস্টেড কন্ডিশনাল ব্রাঞ্চিং এবং হোয়াইল লুপ দিয়ে ক্রমবৃদ্ধি ও ব্রেক।",
        "code": '''পূর্ণসংখ্যা সংখ্যা = 1;
পূর্ণসংখ্যা সীমা = 5;

লেখো("১ থেকে ৫ পর্যন্ত প্রিন্ট:");
যতক্ষণ (সংখ্যা <= সীমা) {
    যদি (সংখ্যা % 2 == 0) {
        লেখো("জোড় সংখ্যা:");
        লেখো(সংখ্যা);
    } নাহলে {
        লেখো("বিজোড় সংখ্যা:");
        লেখো(সংখ্যা);
    }
    সংখ্যা = সংখ্যা + 1;
}
'''
    },
    "data_structures": {
        "title": "📚 স্ট্যাক ও কিউ (Stack & Queue Data Structures)",
        "desc": "ইন-বিল্ট LIFO স্ট্যাক এবং FIFO কিউ মেথডস (ঠেলো, বের_করো, ঢোকাও)।",
        "code": '''// স্ট্যাক পরীক্ষা (LIFO)
স্ট্যাক বইয়ের_তাক;
বইয়ের_তাক.ঠেলো("বই ১");
বইয়ের_তাক.ঠেলো("বই ২");
বইয়ের_তাক.ঠেলো("বই ৩");

লেখো("স্ট্যাকের উপরের বই:");
লেখো(বইয়ের_তাক.সামনে_দেখো());

লেখো("স্ট্যাক থেকে বের করা হলো:");
লেখো(বইয়ের_তাক.বের_করো());
লেখো(বইয়ের_তাক.বের_করো());

// কিউ পরীক্ষা (FIFO)
কিউ লাইনের_টিকিট;
লাইনের_টিকিট.ঢোকাও("যাত্রী ক");
লাইনের_টিকিট.ঢোকাও("যাত্রী খ");

লেখো("কিউ এর সামনে:");
লেখো(লাইনের_টিকিট.সামনে_দেখো_কিউ());
লেখো("টিকিট পেলেন:");
লেখো(লাইনের_টিকিট.বের_করো_কিউ());
'''
    },
    "oop_classes": {
        "title": "🏛️ অবজেক্ট ও ক্লাস (Classes, OOP & Self)",
        "desc": "বাংলায় অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং: ক্লাস ডিফিনিশন, ফিল্ড, মেথড ও ইনস্ট্যান্স তৈরি।",
        "code": '''ক্লাস গাড়ি {
    স্ট্রিং মডেল = "করোলা";
    পূর্ণসংখ্যা গতি = 0;

    ফাংশন গতি_বাড়ালে(নিজে, পূর্ণসংখ্যা পরিমাণ) {
        নিজে.গতি = নিজে.গতি + পরিমাণ;
    }

    ফাংশন অবস্থা(নিজে) {
        লেখো("গাড়ির বর্তমান গতি:");
        লেখো(নিজে.গতি);
    }
}

আমার_গাড়ি = নতুন গাড়ি();
আমার_গাড়ি.গতি_বাড়ালে(60);
আমার_গাড়ি.গতি_বাড়ালে(25);
আমার_গাড়ি.অবস্থা();
'''
    },
    "type_error_demo": {
        "title": "⚠️ টাইপ চেকিং ও এরর ডায়াগনস্টিকস (Semantic Errors)",
        "desc": "টাইপ মিসম্যাচ ও আনডিক্লেয়ার্ড ভেরিয়েবল শনাক্তকরণের ডেমো।",
        "code": '''পূর্ণসংখ্যা বয়স = "বাইশ"; // টাইপ মিসম্যাচ ত্রুটি
দশমিক উচ্চতা = 5.9;
উচ্চতা = "ভুল স্ট্রিং";     // টাইপ মিসম্যাচ

লেখো(অজানা_ভেরিয়েবল);   // আনডিফাইন্ড ভেরিয়েবল
'''
    }
}


class CompilerRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/examples":
            self.send_json_response(SAMPLE_PROGRAMS)
            return
        elif parsed.path == "/api/health":
            self.send_json_response({"status": "ok", "version": "1.0.0"})
            return
        
        # Serve static assets
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")

        try:
            payload = json.loads(post_data) if post_data else {}
        except Exception as e:
            self.send_json_response({"success": False, "errors": [f"Invalid JSON payload: {e}"]}, status=400)
            return

        source = payload.get("source", "")

        if parsed.path == "/api/compile":
            self.handle_compile(source, execute=False)
        elif parsed.path == "/api/run":
            self.handle_compile(source, execute=True)
        else:
            self.send_json_response({"error": "Endpoint not found"}, status=404)

    def handle_compile(self, source: str, execute: bool = False):
        start_time = time.perf_counter()
        compiler = Compiler()
        result = compiler.compile(source)

        # Tokens serialization
        tokens_data = []
        if result.tokens:
            for t in result.tokens:
                tokens_data.append({
                    "kind": t.kind,
                    "lexeme": t.lexeme,
                    "line": t.line,
                    "col": t.column,
                    "value": None if t.value is None else str(t.value)
                })

        # AST serialization
        ast_text = ast_to_text(result.ast) if result.ast else ""
        ast_tree = ast_to_tree_node(result.ast) if result.ast else None

        # Symbols & Semantics
        symbols_list = []
        functions_list = []
        classes_list = []

        if result.semantic:
            for scope_idx, scope in enumerate(result.semantic.scopes):
                for var_name, sym in scope.items():
                    symbols_list.append({
                        "name": var_name,
                        "type": sym.type_name,
                        "scope": "Global" if scope_idx == 0 else f"Scope-{scope_idx}",
                        "initialized": sym.initialized
                    })
            for fname, fnode in result.semantic.functions.items():
                params_formatted = [f"{p}:{t or 'any'}" for p, t in fnode.params]
                functions_list.append({
                    "name": fname,
                    "params": params_formatted,
                    "return_type": fnode.return_type or "any"
                })
            for cname, cnode in result.semantic.classes.items():
                classes_list.append({
                    "name": cname,
                    "fields": [f.name for f in cnode.fields],
                    "methods": [m.name for m in cnode.methods]
                })

        # TAC
        tac_lines = [str(x) for x in result.tac] if result.tac else []

        # Generated Python Code
        python_code = result.python_code or ""

        # Runtime execution if requested
        output = ""
        runtime_error = None
        if execute and result.success:
            namespace = {"__name__": "__bangla_generated__"}
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(python_code, namespace, namespace)
                output = buf.getvalue()
            except Exception as e:
                runtime_error = f"{type(e).__name__}: {e}"
                result.errors.append(f"রানটাইম ত্রুটি: {runtime_error}")

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)

        response_data = {
            "success": result.success and not runtime_error,
            "errors": result.errors,
            "tokens": tokens_data,
            "ast_text": ast_text,
            "ast_tree": ast_tree,
            "symbols": symbols_list,
            "functions": functions_list,
            "classes": classes_list,
            "tac": tac_lines,
            "python_code": python_code,
            "output": output,
            "elapsed_ms": elapsed_ms
        }
        self.send_json_response(response_data)

    def send_json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run_server(port=PORT):
    os.makedirs(WEB_DIR, exist_ok=True)
    server_address = ("", port)
    httpd = HTTPServer(server_address, CompilerRequestHandler)
    print(f"==================================================")
    print(f"🇧🇩 BanglaBhasha Compiler Live Demo Server")
    print(f"📍 Local URL: http://localhost:{port}")
    print(f"📂 Static Dir: {WEB_DIR}")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)
