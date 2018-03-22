def verify_string(input_string):
    if input_string.count('(') != input_string.count(')'):
        if debug: print("Number of begin parenthesis does not match number of end parenthesis.")
        print("\n!!!!! Equation Check Failed !!!!!")
        return False
    if " " in input_string: input_string = input_string.replace(" ", "")
    input_string += "          "
    def string_walk(string):
        debug = True
        super_debug = True
        if super_debug: print("\nTesting string '" + string.replace(" ","") + "'")
        list_advanced_operators = ("np.sin", "np.cos", "np.tan", "np.pi", "np.asin", "np.acos", "np.atan", "np.log", "np.exp", "complex", "abs")
        list_basic_operators = ("+", "-", "*", "/")
        variables_and_constants = ("Z", "C", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        list_of_numbers = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        count = 0
        begins_minus_ends = 0
        next_can_be_basic_operator = False
        next_must_be_begin_parenthesis = False
        skip_for_exponent_operator = False
        while count < len(string):
            if super_debug: print("nested string walk count: " + str(count))
            character = string[count]
            if skip_for_exponent_operator:
                if super_debug: print("check 1")
                count += 1
                skip_for_exponent_operator = False
            elif character == "(":
                if super_debug: print("check 2")
                begins_minus_ends += 1
                count += 1
                substring_start = count
                substring_end = count
                while not ((substring_end >= len(string)) or begins_minus_ends == 0):
                    if string[substring_end] == "(":
                        begins_minus_ends += 1
                    elif string[substring_end] == ")":
                        begins_minus_ends -= 1
                    if begins_minus_ends != 0:
                        substring_end += 1
                    count += 1
                if super_debug:
                    print("substring start and end: " + str(substring_start) + ", " + str(substring_end))
                    print("count after parenthesis: " + str(count))
                if not string_walk(string[substring_start:substring_end]):
                    print("\n!!!!! Equation Check Failed !!!!!")
                    return False
                next_can_be_basic_operator = True
                next_must_be_begin_parenthesis = False
            elif (character in variables_and_constants) and (not next_must_be_begin_parenthesis):
                if super_debug: print("check 3")
                next_can_be_basic_operator = True
                count += 1
            elif character == "-" and (not next_can_be_basic_operator) and (not next_must_be_begin_parenthesis): #handles case of "-" serving as a negative sign in front of a number
                if super_debug: print("check 14")
                if not ((string[count+1] in list_of_numbers) or (string[count+1] == ".")):
                    print("\n!!!!! Equation Check Failed !!!!!")
                    return False
                else: count += 1
            elif (character in list_basic_operators) and next_can_be_basic_operator and (not next_must_be_begin_parenthesis):
                if super_debug: print("check 4")
                if count + 1 < len(string):
                    if character == "*" and string[count+1] == "*":
                        skip_for_exponent_operator = True
                count += 1
                next_can_be_basic_operator = False
            elif character == ".":
                if super_debug: print("check 12")
                subcount = count - 1
                if count != 0:
                    while True:
                        if string[subcount] not in list_of_numbers:
                            if (string[subcount] != "(") and (string[subcount] not in list_basic_operators):
                                print("\n!!!!! Equation Check Failed !!!!!")
                                return False
                            else: break
                        else: subcount -= 1
                    count += 1
                    if string[count] not in list_of_numbers:
                        print("\n!!!!! Equation Check Failed !!!!!")
                        return False
                else: count += 1
            elif string[count:count+3] in list_advanced_operators and not next_must_be_begin_parenthesis:
                if super_debug: print("check 5")
                count += 3
                next_can_be_basic_operator = False
                next_must_be_begin_parenthesis = True
            elif string[count:count+7] in list_advanced_operators and not next_must_be_begin_parenthesis:
                if super_debug: print("check 6")
                if string[count:count+7] == 'math.pi': next_must_be_begin_parenthesis = False
                else: next_must_be_begin_parenthesis = True
                count += 7
                next_can_be_basic_operator = False
            elif string[count:count+6] in list_advanced_operators and not next_must_be_begin_parenthesis:
                if super_debug: print("check 6.5")
                if string[count:count+6] == 'math.pi': next_must_be_begin_parenthesis = False
                else: next_must_be_begin_parenthesis = True
                count += 6
                next_can_be_basic_operator = False
            elif string[count:count+8] in list_advanced_operators and not next_must_be_begin_parenthesis:
                if super_debug: print("check 7")
                count += 8
                next_can_be_basic_operator = False
                next_must_be_begin_parenthesis = True
            elif string[count:count+9] in list_advanced_operators and not next_must_be_begin_parenthesis:
                if super_debug: print("check 8")
                count += 9
                next_can_be_basic_operator = False
                next_must_be_begin_parenthesis = True
            elif string[count:count+10] in list_advanced_operators and not next_must_be_begin_parenthesis:
                if super_debug: print("check 13")
                count += 10
                next_can_be_basic_operator = False
                next_must_be_begin_parenthesis = True
            elif character == ")":
                if super_debug: print("check 9")
                if debug: print("Found unexpected end ')'")
                print("\n!!!!! Equation Check Failed !!!!!")
                return False #in valid strings, these should all be caught by the earlier 'if' condition, where parenthetic expressions are handled recursively
            elif character == " ":
                string = input_string.replace(" ", "")
            else:
                if super_debug: print("check 10")
                if debug:
                    print("\nEquation debugging:\nError handling character at position " + str(count) + " of string '" + string.replace(" ","") + "': '" + character + "'")
                    print("next_can_be_basic_operator:     " + str(next_can_be_basic_operator))
                    print("next_must_be_begin_parenthesis: " + str(next_must_be_begin_parenthesis))
                    print("skip_for_exponent_operator:     " + str(skip_for_exponent_operator))
                print("\n!!!!! Equation Check Failed !!!!!")
                return False
            if (next_must_be_begin_parenthesis or (character in list_basic_operators)) and count >= len(string):
                if super_debug: print("check 11")
                if debug: print("Incomplete or erroneous expression at end of string!")
                print("\n!!!!! Equation Check Failed !!!!!")
                return False
        print("\n!!!!! Equation Seems Valid !!!!!")
        return True
    return string_walk(input_string)

def codify_equation(equation):
        starting_equation = equation
        target_operators=("np.sin",
                          "np.cos",
                          "np.tan",
                          "np.pi",
                          "np.asin",
                          "np.acos",
                          "np.atan",
                          "np.log",
                          "np.exp")
        possible_input_operators = (("sin",),
                                   ("cos",),
                                   ("tan",),
                                   ("pi",),
                                   ("asin","arcsin"),
                                   ("acos","arccos"),
                                   ("atan","arctan"),
                                   ("log","ln"),
                                   ("exp","e^","e**"))
        equation = equation.replace("^","**")
        for i, op_set in enumerate(possible_input_operators):
            for operator in op_set:
                print("operator: " + str(operator))
                if operator in equation:
                    equation = equation.replace(target_operators[i],"~")
                    equation = equation.replace(operator,target_operators[i])
                    equation = equation.replace("~",target_operators[i])
        return equation

string = "C*(sin(Z)+ cos(Z))*(Z^3+Z+C)"
verify_string(codify_equation(string))

