import ast
import operator
import tkinter as tk


class SafeEvaluator(ast.NodeVisitor):
    _bin_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_ops = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_BinOp(self, node):
        op_type = type(node.op)
        if op_type not in self._bin_ops:
            raise ValueError("Operation nicht erlaubt.")
        return self._bin_ops[op_type](self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node):
        op_type = type(node.op)
        if op_type not in self._unary_ops:
            raise ValueError("Operation nicht erlaubt.")
        return self._unary_ops[op_type](self.visit(node.operand))

    def visit_Constant(self, node):
        if not isinstance(node.value, (int, float)):
            raise ValueError("Nur Zahlen erlaubt.")
        return node.value

    def generic_visit(self, node):
        raise ValueError("Ungueltiger Ausdruck.")


def safe_eval(expr: str) -> float:
    tree = ast.parse(expr, mode="eval")
    return SafeEvaluator().visit(tree)


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Grafischer Taschenrechner")
        self.root.geometry("320x420")
        self.root.resizable(False, False)

        self.display_var = tk.StringVar(value="")
        self.display = tk.Entry(
            root,
            font=("Arial", 20),
            justify="right",
            textvariable=self.display_var,
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+",
            "(", ")", "⌫", "C",
        ]

        row = 1
        col = 0
        for label in buttons:
            tk.Button(
                root,
                text=label,
                font=("Arial", 16),
                command=lambda b=label: self.click(b),
            ).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(1, 7):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

        root.bind("<Return>", lambda _e: self.calculate())
        root.bind("<BackSpace>", lambda _e: self.backspace())
        root.bind("<Escape>", lambda _e: self.clear())

    def click(self, key):
        if key == "=":
            self.calculate()
            return
        if key == "C":
            self.clear()
            return
        if key == "⌫":
            self.backspace()
            return
        self.display_var.set(self.display_var.get() + key)

    def calculate(self):
        expr = self.display_var.get().strip()
        if not expr:
            return
        try:
            result = safe_eval(expr)
            self.display_var.set(str(result))
        except ZeroDivisionError:
            self.display_var.set("Fehler: Division durch 0")
        except Exception:
            self.display_var.set("Fehler")

    def clear(self):
        self.display_var.set("")

    def backspace(self):
        current = self.display_var.get()
        self.display_var.set(current[:-1])


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
