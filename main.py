from kirkpiler.lexer import Lexer
from kirkpiler.parser import Parser
from kirkpiler.semantic import SemanticAnalyzer
from kirkpiler.codegen import LLVMCodeGenerator
source="""
let x = 20;
let y = 20;

if x >= y {
    x = x + 1;
}
"""


lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

analyzer = SemanticAnalyzer()
analyzer.analyze(ast)

codegen = LLVMCodeGenerator()

llvm_ir = codegen.generate(ast)

print("\nLLVM IR:")
print(llvm_ir)
codegen.validate()

optimized_ir = codegen.optimize()

print("\nOptimized LLVM IR:")
print(optimized_ir)
codegen.generate_object_file()