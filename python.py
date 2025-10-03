"""Simple safe calculator CLI

Usage:
  - Run interactively: python python.py
  - Evaluate one expression: python python.py -e "2 + 2 * sin(pi/2)"

This evaluator parses the expression with ast and only allows a small safe
subset of nodes and names (math functions/constants and a few builtins).
"""
from __future__ import annotations

import argparse
import ast
import math
import operator
import sys
from typing import Any, Dict


class SafeEvaluator(ast.NodeVisitor):
	"""Validate an AST to ensure it only contains safe constructs."""

	ALLOWED_BINOPS = (
		ast.Add,
		ast.Sub,
		ast.Mult,
		ast.Div,
		ast.Mod,
		ast.Pow,
		ast.FloorDiv,
	)
	ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)

	def __init__(self, names: Dict[str, Any]):
		self.names = names

	def visit(self, node):
		method = 'visit_' + node.__class__.__name__
		visitor = getattr(self, method, self.generic_visit)
		return visitor(node)

	def visit_Expression(self, node: ast.Expression) -> None:
		self.visit(node.body)

	def visit_BinOp(self, node: ast.BinOp) -> None:
		if not isinstance(node.op, self.ALLOWED_BINOPS):
			raise ValueError(f"Operator {node.op.__class__.__name__} not allowed")
		self.visit(node.left)
		self.visit(node.right)

	def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
		if not isinstance(node.op, self.ALLOWED_UNARYOPS):
			raise ValueError(f"Unary operator {node.op.__class__.__name__} not allowed")
		self.visit(node.operand)

	def visit_Call(self, node: ast.Call) -> None:
		# Only allow simple name calls (no attribute access, no kwargs)
		if not isinstance(node.func, ast.Name):
			raise ValueError("Only direct function calls are allowed")
		func_name = node.func.id
		if func_name not in self.names:
			raise ValueError(f"Function '{func_name}' is not allowed")
		if node.keywords:
			raise ValueError("Keyword arguments are not allowed")
		for arg in node.args:
			self.visit(arg)

	def visit_Name(self, node: ast.Name) -> None:
		if node.id not in self.names:
			raise ValueError(f"Name '{node.id}' is not allowed")

	def visit_Constant(self, node: ast.Constant) -> None:
		if not isinstance(node.value, (int, float, complex)):
			raise ValueError("Only numeric constants are allowed")

	# For Python <3.8 where Num exists
	def visit_Num(self, node: ast.Num) -> None:
		return

	def visit_Attribute(self, node: ast.Attribute) -> None:
		raise ValueError("Attribute access is not allowed")

	def generic_visit(self, node):
		# Reject any other node types explicitly
		allowed = (
			ast.Expression,
			ast.BinOp,
			ast.UnaryOp,
			ast.Call,
			ast.Name,
			ast.Load,
			ast.Constant,
			ast.Num,
		)
		if isinstance(node, allowed):
			return super().generic_visit(node)
		raise ValueError(f"Node type {node.__class__.__name__} not allowed")


def build_safe_names() -> Dict[str, Any]:
	names: Dict[str, Any] = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
	# Add a few safe builtins
	names.update({'abs': abs, 'round': round, 'min': min, 'max': max})
	return names


def safe_eval(expression: str, names: Dict[str, Any]) -> Any:
	"""Evaluate a numeric expression safely using AST validation.

	Raises ValueError or SyntaxError for invalid input.
	"""
	tree = ast.parse(expression, mode='eval')
	SafeEvaluator(names).visit(tree)
	code = compile(tree, '<expr>', 'eval')
	return eval(code, {'__builtins__': None}, names)


def repl(names: Dict[str, Any]) -> None:
	try:
		import readline  # optional, improves UX on many systems
	except Exception:
		pass

	prompt = 'calc> '
	while True:
		try:
			line = input(prompt).strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if not line:
			continue
		if line.lower() in ('quit', 'exit'):
			break
		try:
			result = safe_eval(line, names)
		except Exception as exc:
			print('Error:', exc)
		else:
			print(result)


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description='Safe calculator')
	parser.add_argument('-e', '--expr', help='Evaluate a single expression')
	args = parser.parse_args(argv)

	names = build_safe_names()

	if args.expr:
		try:
			out = safe_eval(args.expr, names)
		except Exception as exc:
			print('Error:', exc, file=sys.stderr)
			return 2
		else:
			print(out)
			return 0

	repl(names)
	return 0


if __name__ == '__main__':
	raise SystemExit(main())

