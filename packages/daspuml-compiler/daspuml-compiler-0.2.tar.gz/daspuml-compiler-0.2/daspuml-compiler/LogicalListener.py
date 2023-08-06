import logging

from DaspumlListener import DaspumlListener
from DaspumlParser import DaspumlParser
from exceptions import *


class LogicalListener(DaspumlListener):
    def __init__(self, register):
        self.register = register
        self.output = ""
        self.scopeName = None
        self.isInFunDeclaration = False
        self.isInPtr = False
        self.logger = logging.getLogger(__name__)

    def enterStart(self, ctx: DaspumlParser.StartContext):
        pass

    def exitStart(self, ctx: DaspumlParser.StartContext):
        if self.output == "":
            raise EmptyUmlGraphException()
        with open("output.txt", 'w+') as fp:
            fp.write(self.output.rstrip())
        # print(self.output)

    def exitObj_list(self, ctx: DaspumlParser.Obj_listContext):
        obj_list = ctx.NAME()
        tmp = []
        for o in obj_list:
            tmp.append(o.getText())
        ctx.INSIDE = tmp

    def exitIdx_list(self, ctx: DaspumlParser.Idx_listContext):
        idx_list = ctx.INDEX()
        tmp = []

        for i in idx_list:
            tmp.append(i.getText())
        ctx.INSIDE = tmp

    def exitAutonumber(self, ctx: DaspumlParser.AutonumberContext):
        self.output += "autonumber \n"

    def enterFun_declaration(self, ctx: DaspumlParser.Fun_declarationContext):
        self.isInFunDeclaration = True

    def exitFun_declaration(self, ctx: DaspumlParser.Fun_declarationContext):
        self.isInFunDeclaration = False

    def enterPattern(self, ctx: DaspumlParser.PatternContext):
        self.isInPtr = True

    def exitPattern(self, ctx: DaspumlParser.PatternContext):
        self.isInPtr = False
        if self.isInFunDeclaration:
            return
        if ctx.obj_list():
            obj_list = ctx.obj_list().INSIDE
        else:
            obj_list = self.register.get_variable(ctx.variable().NAME().getText(), self.scopeName).INSIDE
        idx_list = ctx.idx_list()[0].INSIDE

        case_flag = False
        if len(ctx.idx_list()) > 1:
            case_list = ctx.idx_list()[1].INSIDE
            case_flag = True

        preset_case = None
        case_i = 0
        for i in range(len(obj_list) - 1):
            if case_flag:
                preset_case = case_list[case_i]

                case_i += 1
                if case_i > len(case_list) - 1:
                    case_i = 0

            for body in ctx.pattern_body():
                if body.CASE() is None:
                    # loop without cases

                    connection = body.pattern_connection()
                    if connection.pattern_direction() is None:
                        # normal connections

                        if connection.direction() is None:
                            # normal index
                            self.exitDirection(connection.connection().direction())
                            self.exitConnection(connection.connection())

                        else:
                            # index as stp
                            self.exitDirection(connection.direction())
                            self.output += ": " + idx_list[i][1:-1] + "\n"

                    else:
                        # connection with pattern_direction
                        if connection.pattern_direction().OUT_ARR() is None:

                            if connection.pattern_direction().SET()[0].getText() == "pre":
                                var = obj_list[i]
                            elif connection.pattern_direction().SET()[0].getText() == "nxt":
                                var = obj_list[i + 1]
                            else:
                                var = connection.pattern_direction().SET()[0].getText()
                            if var in self.register.object_register.keys() and self.register.object_register[var][1] == "u":
                                direction = connection.pattern_direction().IN_ARR().getText()
                                if direction == "<-":
                                    self.output += var + "->" + var
                                elif direction == "<--":
                                    self.output += var + "-->" + var
                                elif direction == "<..":
                                    self.output += var + "-->" + var
                            else:
                                if var in self.register.object_register.keys():
                                    raise ObjectNotDeclaredException(var)
                                else:
                                    raise ObjectNotStartedException(var)

                        else:
                            if connection.pattern_direction().SET()[0].getText() == "pre":
                                var_fst = obj_list[i]
                            elif connection.pattern_direction().SET()[0].getText() == "nxt":
                                var_fst = obj_list[i + 1]
                            else:
                                var_fst = connection.pattern_direction().SET()[0].getText()
                            if connection.pattern_direction().SET()[1].getText() == "pre":
                                var_snd = obj_list[i]
                            elif connection.pattern_direction().SET()[1].getText() == "nxt":
                                var_snd = obj_list[i + 1]
                            else:
                                var_snd = connection.pattern_direction().SET()[1].getText()

                            if var_fst not in self.register.object_register.keys():
                                raise ObjectNotDeclaredException(var_fst)
                            if var_snd not in self.register.object_register.keys():
                                raise ObjectNotDeclaredException(var_snd)

                            if self.register.object_register[var_fst][1] == "u":
                                direction = connection.pattern_direction().OUT_ARR().getText()
                                if direction != "..>":
                                    self.output += var_fst + connection.pattern_direction().OUT_ARR().getText() + var_snd
                                else:
                                    self.output += var_fst + "-->" + var_snd
                            else:
                                raise ObjectNotStartedException(self.register.object_register[var_fst][0])

                        if connection.STP() is None:
                            # normal index
                            self.output += ": " + connection.INDEX().getText() + "\n"

                        else:
                            # index as stp
                            self.output += ": " + idx_list[i][1:-1] + "\n"

                else:
                    # Loop with cases
                    if preset_case is None:
                        raise NoCaseDeclarationInPatternException()
                    if body.INDEX().getText() == preset_case:
                        connection = body.pattern_connection()
                        if connection.pattern_direction() is None:
                            # normal connections

                            if connection.direction() is None:
                                # normal index
                                self.exitDirection(connection.connection().direction())
                                self.exitConnection(connection.connection())

                            else:
                                # index as stp
                                self.exitDirection(connection.direction())
                                self.output += ": " + idx_list[i][1:-1] + "\n"

                        else:
                            # connection with pattern_direction
                            if connection.pattern_direction().OUT_ARR() is None:

                                if connection.pattern_direction().SET()[0].getText() == "pre":
                                    var = obj_list[i]
                                elif connection.pattern_direction().SET()[0].getText() == "nxt":
                                    var = obj_list[i + 1]
                                else:
                                    var = connection.pattern_direction().SET()[0].getText()
                                if var in self.register.object_register.keys() and self.register.object_register[var][
                                    1] == "u":
                                    direction = connection.pattern_direction().IN_ARR().getText()
                                    if direction == "<-":
                                        self.output += var + "->" + var
                                    elif direction == "<--":
                                        self.output += var + "-->" + var
                                    elif direction == "<..":
                                        self.output += var + "-->" + var
                                else:
                                    if var in self.register.object_register.keys():
                                        raise ObjectNotDeclaredException(var)
                                    else:
                                        raise ObjectNotStartedException(var)

                            else:
                                if connection.pattern_direction().SET()[0].getText() == "pre":
                                    var_fst = obj_list[i]
                                elif connection.pattern_direction().SET()[0].getText() == "nxt":
                                    var_fst = obj_list[i + 1]
                                else:
                                    var_fst = connection.pattern_direction().SET()[0].getText()
                                if connection.pattern_direction().SET()[1].getText() == "pre":
                                    var_snd = obj_list[i]
                                elif connection.pattern_direction().SET()[1].getText() == "nxt":
                                    var_snd = obj_list[i + 1]
                                else:
                                    var_snd = connection.pattern_direction().SET()[1].getText()

                                if var_fst not in self.register.object_register.keys():
                                    raise ObjectNotDeclaredException(var_fst)
                                if var_snd not in self.register.object_register.keys():
                                    raise ObjectNotDeclaredException(var_snd)

                                if self.register.object_register[var_fst][1] == "u":
                                    direction = connection.pattern_direction().OUT_ARR().getText()
                                    if direction != "..>":
                                        self.output += var_fst + connection.pattern_direction().OUT_ARR().getText() + var_snd
                                    else:
                                        self.output += var_fst + "-->" + var_snd
                                else:
                                    raise ObjectNotStartedException(self.register.object_register[var_fst][0])

                            if connection.STP() is None:
                                # normal index
                                self.output += ": " + connection.INDEX().getText() + "\n"

                            else:
                                # index as stp
                                self.output += ": " + idx_list[i][1:-1] + "\n"
                    else:
                        # Pass cases
                        pass

    def exitStart_point(self, ctx: DaspumlParser.Start_pointContext):
        var = ctx.NAME().getText()
        if var in self.register.object_register.keys() and self.register.object_register[var][1] == "r":
            self.register.object_register[var][1] = "u"
            self.output += "activate " + var + "\n"
        else:
            raise ObjectEndedException(var)



    def exitEnd_point(self, ctx: DaspumlParser.End_pointContext):
        var = ctx.NAME().getText()
        if var in self.register.object_register.keys() and self.register.object_register[var][1] == "u":
            self.register.object_register[var][1] = "d"
            self.output += "deactivate " + var + "\n"
        else:
            raise ObjectNotStartedException(var)



    def exitConnection(self, ctx: DaspumlParser.ConnectionContext):
        if self.isInFunDeclaration:
            return
        if not self.isInPtr:
            self.output += ": " + ctx.INDEX().getText()[1:-1] + "\n"

    def exitDirection(self, ctx: DaspumlParser.DirectionContext):
        if self.isInFunDeclaration:
            return
        if not self.isInPtr:
            if ctx.OUT_ARR() is None:
                var = ctx.NAME()[0].getText()
                if var in self.register.object_register.keys() and self.register.object_register[var][1] == "u":
                    direction = ctx.IN_ARR().getText()
                    if direction == "<-":
                        self.output += var + "->" + var
                    elif direction == "<--":
                        self.output += var + "-->" + var
                    elif direction == "<..":
                        self.output += var + "-->" + var
                else:
                    if var in self.register.object_register.keys():
                        raise ObjectNotDeclaredException(var)
                    else:
                        raise ObjectNotStartedException(var)
            else:
                var_fst = ctx.NAME()[0].getText()
                var_snd = ctx.NAME()[1].getText()

                if var_fst not in self.register.object_register.keys():
                    raise ObjectNotDeclaredException(var_fst)
                if var_snd not in self.register.object_register.keys():
                    raise ObjectNotDeclaredException(var_snd)

                if self.register.object_register[var_fst][1] == "u":
                    direction = ctx.OUT_ARR().getText()
                    if direction != "..>":
                        self.output += var_fst + ctx.OUT_ARR().getText() + var_snd
                    else:
                        self.output += var_fst + "-->" + var_snd
                else:
                    raise ObjectNotStartedException(var_fst)

    def enterCall_fun(self, ctx: DaspumlParser.Call_funContext):
        self.scopeName = ctx.NAME().getText()
        for elem in self.register.get_function_to_call(ctx.NAME().getText()):
            if elem.pattern():
                self.exitPattern(elem.pattern())
            if elem.start_point():
                self.exitStart_point(elem.start_point())
            if elem.end_point():
                self.exitStart_point(elem.end_point())
            if elem.connection():
                self.exitDirection(elem.connection().direction())
                self.exitConnection(elem.connection())

    def exitCall_fun(self, ctx: DaspumlParser.Call_funContext):
        self.scopeName = None

    def exitOperation(self, ctx: DaspumlParser.OperationContext):
        if ctx.call_fun():
            i = 0
            for elem in ctx.parentCtx.operation():
                if elem is ctx:
                    break
                i += 1

            ctx.parentCtx.operation()[i] = self.register.function_register[ctx.call_fun().NAME().getText()][0]


del DaspumlParser
