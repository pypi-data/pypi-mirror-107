import logging

if __name__ is not None and "." in __name__:
    from .DaspumlListener import DaspumlListener
    from .DaspumlParser import DaspumlParser
    from .Register import Register
else:
    from DaspumlListener import DaspumlListener
    from DaspumlParser import DaspumlParser
    from Register import Register


class IndexingListener(DaspumlListener):
    def __init__(self, register):
        self.register = register
        self.scopeName = None
        self.logger = logging.getLogger(__name__)

    def exitStart(self, ctx: DaspumlParser.StartContext):
        self.logger.debug("Object register: {}".format(self.register.object_register))
        self.logger.debug("Variable register: {}".format(self.register.variable_register))
        self.logger.debug("Function register: {}".format(self.register.function_register))

    def enterVar_declaration(self, ctx: DaspumlParser.Var_declarationContext):
        if self.scopeName:
            self.register.variable_register[self.scopeName][ctx.variable().NAME().getText()] = ctx.obj_list()
        else:
            self.register.variable_register[Register.global_scope_name][ctx.variable().NAME().getText()] = ctx.obj_list()

    def enterFun_declaration(self, ctx: DaspumlParser.Fun_declarationContext):
        self.register.variable_register[ctx.NAME().getText()] = {}
        self.scopeName = ctx.NAME().getText()
        self.register.function_register[ctx.NAME().getText()] = ctx.declaration_body()

    def exitFun_declaration(self, ctx: DaspumlParser.Fun_declarationContext):
        self.scopeName = None

    def enterObj_declaration(self, ctx: DaspumlParser.Obj_declarationContext):
        variable = ctx.NAME().getText()
        info = ["obj", "r"]
        self.register.object_register.update({variable: info})


del DaspumlParser
