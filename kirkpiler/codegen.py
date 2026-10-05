from llvmlite import ir
from llvmlite import binding

class LLVMCodeGenerator:

    def __init__(self):
        self.module = ir.Module(name="kirkpiler")

        self.builder = None
        self.function = None

        # Stores variables and their LLVM memory locations
        self.variables = {}

        self.int_type = ir.IntType(32)

    def generate(self, program):
        """
        Generate LLVM IR for the entire program.
        """

        # Create:
        # int main()
        function_type = ir.FunctionType(
            self.int_type,
            []
        )

        self.function = ir.Function(
            self.module,
            function_type,
            name="main"
        )

        # Create entry block
        entry_block = self.function.append_basic_block(
            name="entry"
        )

        self.builder = ir.IRBuilder(entry_block)

        # Generate code for every statement
        for statement in program:
            self.generate_statement(statement)

        # Return 0
        self.builder.ret(
            ir.Constant(self.int_type, 0)
        )

        return str(self.module)

    # --------------------------------------------------
    # STATEMENTS
    # --------------------------------------------------

    def generate_statement(self, statement):

        # let x = expression;
        if statement.__class__.__name__ == "VariableDeclaration":

            value = self.generate_expression(
                statement.value
            )

            # Allocate memory for variable
            variable = self.builder.alloca(
                self.int_type,
                name=statement.name
            )

            # Store initial value
            self.builder.store(
                value,
                variable
            )

            # Remember variable
            self.variables[statement.name] = variable

        # x = expression;
        elif statement.__class__.__name__ == "Assignment":

            if statement.name not in self.variables:
                raise Exception(
                    f"Variable '{statement.name}' "
                    f"has not been declared."
                )

            value = self.generate_expression(
                statement.value
            )

            variable = self.variables[statement.name]

            self.builder.store(
                value,
                variable
            )

        # if (...)
        elif statement.__class__.__name__ == "IfStatement":

            self.generate_if_statement(statement)

        else:
            raise Exception(
                f"Unknown statement: {statement}"
            )

    # --------------------------------------------------
    # EXPRESSIONS
    # --------------------------------------------------

    def generate_expression(self, expression):

        # ----------------------------------------------
        # NumberLiteral
        # ----------------------------------------------

        if expression.__class__.__name__ == "NumberLiteral":

            return ir.Constant(
                self.int_type,
                expression.value
            )

        # ----------------------------------------------
        # Identifier
        # ----------------------------------------------

        if expression.__class__.__name__ == "Identifier":

            if expression.name not in self.variables:
                raise Exception(
                    f"Variable '{expression.name}' "
                    f"has not been declared."
                )

            variable = self.variables[expression.name]

            return self.builder.load(
                variable,
                name=expression.name
            )

        # ----------------------------------------------
        # BinaryExpression
        # ----------------------------------------------

        if expression.__class__.__name__ == "BinaryExpression":

            left = self.generate_expression(
                expression.left
            )

            right = self.generate_expression(
                expression.right
            )

            operator = expression.operator

            # Arithmetic
            if operator == "+":
                return self.builder.add(
                    left,
                    right,
                    name="addtmp"
                )

            elif operator == "-":
                return self.builder.sub(
                    left,
                    right,
                    name="subtmp"
                )

            elif operator == "*":
                return self.builder.mul(
                    left,
                    right,
                    name="multmp"
                )

            elif operator == "/":
                return self.builder.sdiv(
                    left,
                    right,
                    name="divtmp"
                )

            elif operator == "%":
                return self.builder.srem(
                    left,
                    right,
                    name="modtmp"
                )

            # Comparisons
            elif operator == ">":
                return self.builder.icmp_signed(
                    ">",
                    left,
                    right,
                    name="gttmp"
                )

            elif operator == ">=":
                return self.builder.icmp_signed(
                    ">=",
                    left,
                    right,
                    name="getmp"
                )

            elif operator == "<":
                return self.builder.icmp_signed(
                    "<",
                    left,
                    right,
                    name="lttmp"
                )

            elif operator == "<=":
                return self.builder.icmp_signed(
                    "<=",
                    left,
                    right,
                    name="letmp"
                )

            elif operator == "==":
                return self.builder.icmp_signed(
                    "==",
                    left,
                    right,
                    name="eqtmp"
                )

            else:
                raise Exception(
                    f"Unknown operator: {operator}"
                )

        raise Exception(
            f"Unknown expression: {expression}"
        )

    # --------------------------------------------------
    # IF STATEMENT
    # --------------------------------------------------

    def generate_if_statement(self, statement):

        # Generate condition
        condition = self.generate_expression(
            statement.condition
        )

        # Create basic blocks
        then_block = self.function.append_basic_block(
            name="then"
        )

        end_block = self.function.append_basic_block(
            name="endif"
        )

        # Conditional branch
        self.builder.cbranch(
            condition,
            then_block,
            end_block
        )

        # ----------------------------------------------
        # THEN BLOCK
        # ----------------------------------------------

        self.builder.position_at_end(
            then_block
        )

        for body_statement in statement.body:
            self.generate_statement(
                body_statement
            )

        # Jump to end of if
        self.builder.branch(
            end_block
        )

        # ----------------------------------------------
        # END BLOCK
        # ----------------------------------------------

        self.builder.position_at_end(
            end_block
        )
    def validate(self):
        """
        Verify that the generated LLVM IR is valid.
        """

        llvm_module = binding.parse_assembly(
                str(self.module)
        )

        llvm_module.verify()

        print("LLVM IR validation successful!")


    def optimize(self):
        """
        Optimize the generated LLVM IR.
        """

        llvm_module = binding.parse_assembly(
            str(self.module)
        )

        llvm_module.verify()

        # Get the native target
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()

        target = binding.Target.from_default_triple()

        target_machine = target.create_target_machine()

        # Optimization level 2
        pipeline_options = binding.create_pipeline_tuning_options(
            speed_level=2
        )

        # Create LLVM pass builder
        pass_builder = binding.create_pass_builder(
            target_machine,
            pipeline_options
        )

        # Create module optimization pipeline
        pass_manager = pass_builder.getModulePassManager()

        # Run optimization
        pass_manager.run(
            llvm_module,
            pass_builder
        )

        return str(llvm_module)

    def generate_object_file(self, filename="kirkpiler.obj"):
        """
        Generate a native object file from the LLVM IR.
        """

        # Parse LLVM IR
        llvm_module = binding.parse_assembly(
            str(self.module)
        )

        # Verify LLVM IR
        llvm_module.verify()

        # Initialize native target
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()

        # Get native target
        target = binding.Target.from_default_triple()

        # Create target machine
        target_machine = target.create_target_machine()

        # Set target triple
        llvm_module.triple = binding.get_default_triple()

        # Generate object code
        object_code = target_machine.emit_object(
            llvm_module
        )

        # Write object file
        with open(filename, "wb") as file:
            file.write(object_code)

        print(
            f"Object file generated successfully: {filename}"
        )