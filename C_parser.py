import pytest

from Lexer import *

# Open source file

# Run preprocessor

# looking for lines with # at the start
#include
#define
#undef
#if
#ifdef
#ifndef
#error
#__FILE__
#__LINE__
#__DATE__
#__TIME__
#__TIMESTAMP__
#pragma
# macro operator
## macro operator


#preprocessor--directives, constants, and macros


#In some pre-standard C preprocessors (meaning before 1989), the preprocessors only recognized # at the beginning of the line.
#Since the C89/C90 standards required the preprocessor to recognize the # as the first non-blank character on the line (and the C99 and C11 standards do too), it is now perfectly legitimate to indent the directives, and it has been practical for even portable code to do so for all of this millennium.
#In ISO/IEC 9899:2011 (the C11 standard), Section 6.10 Preprocessing directives says:
#A preprocessing directive consists of a sequence of preprocessing tokens that satisfies the following constraints: The first token in the sequence is a # preprocessing token that (at the start of translation phase 4) is either the first character in the source file (optionally after white space containing no new-line characters) or that follows white space containing at least one new-line character.
#The translation phases are defined in section 5.1.1.2 Translation phases.
#The source file is decomposed into preprocessing tokens 7) and sequences of white-space characters (including comments). A source file shall not end in a partial preprocessing token or in a partial comment. Each comment is replaced by one space character. New-line characters are retained. Whether each nonempty sequence of white-space characters other than new-line is retained or replaced by one space character is implementation-defined.
#Preprocessing directives are executed, macro invocations are expanded, and _Pragma unary operator expressions are executed. If a character sequence that matches the syntax of a universal character name is produced by token concatenation (6.10.3.3), the behavior is undefined. A #include preprocessing directive causes the named header or source file to be processed from phase 1 through phase 4, recursively. All preprocessing directives are then deleted.



#mystack = []



#----------------------------------------------------------------
# Phase 1 consists of replaceing multibyte and trigraph sequences
#-----------------------------------------------------------------
def phase1_replace_multibyte():
    return 1

#----------------------------------------------------------------
# Phase 2 consists of glueing line continuations
#-----------------------------------------------------------------
def phase2_glue_line_continuations( input_data ):

    input_index = 0
    state = "NORMAL"
    output_data = ""

    while input_index < len( input_data ):
    
        mychar = input_data[ input_index ]

        if state == "NORMAL":

            if mychar == '\\':
                state = "LINE_CONTINUATION"
            else:
                output_data = output_data + mychar
                #state = "NORMAL"
                
        else: #state=="LINE_CONTINUATION":
            if mychar == '\n':
                # just eat the backslash and newline sequence by not copying it over to the output stram
                print ("Line Continuation found")
            else:
                #it wasn't a line continuation so put backslash back into the output stream
                output_data = output_data + '\\' + mychar
            state = "NORMAL"
        input_index += 1

    return output_data

#-----------------------------------------------------------
def reduce_digit( new_token, last_token ):
    
    reduce = False

    #if new_token[0] == "DIGIT" and last_token[0] == "DIGIT":    
    #    last_token[1] += new_token[1]
    #    reduce = True

    if last_token[0] == "DIGIT":
        last_token[0] = "PP_NUMBER"
        last_token[1] += new_token[1]
        reduce = True      

    return reduce, last_token
#-----------------------------------------------------------
def reduce_pp_number( new_token, last_token ):

    reduce = False

    if last_token[ 0 ] == "PP_NUMBER" and new_token[ 0 ]== "DIGIT":
        last_token[0] = "PP_NUMBER"
        last_token[1] += new_token[1]
        reduce = True
    elif last_token[ 0 ] == "PP_NUMBER" and new_token[ 0 ]== "PUNCTUATION" and new_token[1] ==".":
        last_token[0] = "PP_NUMBER"
        last_token[1] += new_token[1]
        reduce = True
    elif last_token[ 0 ] == "PP_NUMBER" and new_token[ 0 ]== "PP_NUMBER":
        last_token[0] = "PP_NUMBER"
        last_token[1] += new_token[1]
        reduce = True
    
    return reduce, last_token 
#-----------------------------------------------------------
def reduce_nondigit( new_token, last_token ):
    
    reduce = False
    print("Reduce Nondigit",last_token, new_token)
    if new_token[0] == "NON_DIGIT" or  new_token[0]=="DIGIT":
        last_token[0] = "IDENTIFIER"
        last_token[1] += new_token[1]
        reduce = True
    else:
        last_token[0] = "IDENTIFIER"
        reduce = False
        print("here")

    return reduce, last_token
#-----------------------------------------------------------
def reduce_p_identifier( new_token, last_token ):

    reduce = False

    if (new_token[0] != "NON_DIGIT") and (new_token[0] != "DIGIT"):
        # reached the end of the identifies
        last_token[0] = "IDENTIFIER"
        reduce = False
    else:
        last_token[0] = "P_IDENTIFIER"
        last_token[1] += new_token[1]
        reduce = True

    return reduce, last_token
#-----------------------------------------------------------
def reduce_identifier_nondigit( new_token, last_token ):
    
    reduce = False
    print("Reduce Identifier Nondigit",last_token, new_token)
    if new_token[0] == "NON_DIGIT" or new_token[0]=="DIGIT":
        last_token[0] = "IDENTIFIER"
        last_token[1] += new_token[1]
        reduce = True
    else:
        print("BUGGER")
    

    return reduce, last_token
#-----------------------------------------------------------
def reduce_identifier( new_token, last_token ):

    keyword_list = [ "include", "define" ]
    
    reduce = False
    print("Reduce Identifier",last_token, new_token)
    if new_token[0] == "NON_DIGIT" or new_token[0]=="DIGIT":
        last_token[0] = "IDENTIFIER"
        last_token[1] += new_token[1]
        reduce = True

    if new_token[0] == "WHITESPACE" and (last_token[1] in keyword_list):
        last_token[0] = "KEYWORD"
        reduce = True        
    elif new_token[0] == "WHITESPACE":
        last_token[0] = "IDENTIFIER"
        reduce = True     

    return reduce, last_token  
#-----------------------------------------------------------
def reduce_punctuation( new_token, last_token ):
   
    reduce = False
    print("Reduce Punctuation",last_token, new_token)
    if last_token[1] == '/' and new_token[1] == '*':
            last_token[0] = "MULTILINE_COMMENT_START"
            last_token[1] = "/*"
            reduce = True
            
    elif last_token[1] == '/' and new_token[1] == '/':
            last_token[0] = "LINE_COMMENT"
            last_token[1] = "//"
            reduce = True

    elif last_token[1]=='"':
            last_token[0]="STRING_LITERAL"
            last_token[1] = new_token[1]
            reduce= True
            
    elif last_token[1] == ".":
            last_token[0]="PP_NUMBER"
            last_token[1] += new_token[1]
            reduce= True

    elif last_token[1] == "<":
            last_token[0]="HEADER_NAME_START"
            last_token[1] = "" # Don't include the < character.
            reduce= False

    elif last_token[1]=="#" and new_token[0]=="KEYWORD":
            last_token[0]="PP_DIRECTIVE"
            last_token[1]= new_token[1]
            reduce=True
    elif new_token[0]=="WHITESPACE":
        reduce=True

    return reduce, last_token
#-----------------------------------------------------------
def reduce_headername_start( new_token, last_token ):

    reduce = False

    if new_token[0]=="PUNCTUATION" and new_token[1]=='>':
        last_token[0]="HEADER_NAME"
        #last_token[1] += new_token[1] Don't include the > character.
        reduce=True

    else:
        last_token[0]="HEADER_NAME_START"
        last_token[1] += new_token[1]
        reduce=True

    return reduce, last_token
#-----------------------------------------------------------
def reduce_string_literal( new_token, last_token ):

    reduce = False

    if last_token[0]=="STRING_LITERAL" and new_token[0]=="PUNCTUATION" and new_token[1]=='"':
        last_token[0]="STRING"
        #last_token[1] += new_token[1]
        reduce=True

    else:
        last_token[0]="STRING_LITERAL"
        last_token[1] += new_token[1]
        reduce=True

    return reduce, last_token
#-----------------------------------------------------------
def reduce_multiline_comment_start( new_token, last_token ):

    reduce = False
    
    if new_token[1]=="*":
         last_token[0] = "MULILINE_COMMENT_BODY"
         last_token[1] += new_token[1]
         reduce = True
    else:
        #last_token[0]="MULTILINE_COMMENT_START"
        #last_token[1] += new_token[1]
        reduce=False

    return reduce, last_token
#-----------------------------------------------------------
def reduce_multiline_comment_body( new_token, last_token ):

    reduce = False
        
    if new_token[0]=="PUNCTUATION" and new_token[1]=="/":
         last_token[0] = "MULTILINE_COMMENT"
         last_token[1] += new_token[1]
         reduce = True
    else:
        last_token[0]="MULTILINE_COMMENT_BODY"
        last_token[1] += new_token[1]
        reduce=True

    return reduce, last_token
#-----------------------------------------------------------
def reduce_multiline_comment( new_token, last_token ):

    reduce = False
    
    if new_token[0]=="PUNCTUATION" and new_token[1]=="*":
         last_token[0] = "MULTILINE_COMMENT_END"
         last_token[1] += new_token[1]
         reduce = True
    else:
        last_token[0]="MULTILINE_COMMENT"
        last_token[1] += new_token[1]
        reduce=True

    return reduce, last_token
#-----------------------------------------------------------
def reduce_multiline_comment_end( new_token, last_token ):

    reduce = False
    
    if new_token[0]=="PUNCTUATION" and new_token[1]=="/":
         last_token[0] = "COMMENT"
         last_token[1] += new_token[1]
         reduce = True
    else:
        last_token[0]="MULTILINE_COMMENT"
        last_token[1] += new_token[1]
        reduce=True

    return reduce, last_token
#-----------------------------------------------------------
def reduce_line_comment( new_token, last_token ):

    reduce = False

    print("reduce line comment:", last_token, new_token)

    if last_token[0]=="LINE_COMMENT" and new_token[0]=="WHITESPACE" and new_token[1]=='\n':
         last_token[0] = "COMMENT"
         reduce = True
    else:
        last_token[0]="LINE_COMMENT"
        last_token[1] += new_token[1]
        reduce=True

    return reduce, last_token
#-----------------------------------------------------------
def reduce_comment( new_token, last_token ):

    reduce=False
    end3 = last_token[1][-1:] #peek at the last character added
    
    if new_token[0]=="PUNCTUATION" and new_token[1]=="/" and end3=="*":
        last_token[0] = "COMMENT"
        last_token[1] += new_token[1]
        reduce = True
        
    return reduce, last_token
    
#----------------------------------------------------------------
def reduce_PP_DIRECTIVE( new_token, last_token ):

    reduce=False
    print ("reduce PP_DIRECTIVE: last:",last_token, "new:", new_token)

    if new_token[0] == "STRING":
        last_token[0]="PP_INCLUDE"
        last_token[1] = new_token[1]
        last_token.append("LOCAL_INCLUDE")
        reduce = True
    elif new_token[0] == "HEADER_NAME":
        last_token[0]="PP_INCLUDE"
        last_token[1] = new_token[1]
        last_token.append("STANDARD_INCLUDE")
        reduce = True
    #elif new_token[0] == "IDENTIFIER":
     #   last_token[0] ="PP_DIRECTIVE"
      #  last_token.append(new_token[1])
       # reduce = True
     
    return reduce, last_token
#----------------------------------------------------------------
def reduce_KEYWORD( new_token, last_token ):

    reduce=False
    print("reduce keyword", last_token, new_token)
    if new_token[1]=="include" and last_token[0] == "PUNCTUATION" and last_token[1]=="#":
        last_token[0]= "PP_DIRECTIVE"
        reduce = True
    elif new_token[1]=="define" and last_token[0] == "PUNCTUATION" and last_token[1]=="#":
        last_token[0]= "PP_DIRECTIVE"
        reduce = True
    
    return reduce, last_token

#----------------------------------------------------------------
def myError( new_token, last_token ):

    print("ERROR: no reduction function for these tokens:", new_token, last_token)
    
    return False, last_token
#----------------------------------------------------------------
jump_table = { "DIGIT"               : reduce_digit,
               "PP_NUMBER"           : reduce_pp_number,
               "NON_DIGIT"           : reduce_nondigit,
               "PUNCTUATION"         : reduce_punctuation,
               "MULTILINE_COMMENT"   : reduce_multiline_comment,
               "MULTILINE_COMMENT_START"   : reduce_multiline_comment,
               "MULTILINE_COMMENT_BODY"    : reduce_multiline_comment_body,
               "MULTILINE_COMMENT_END"    : reduce_multiline_comment_end,
               "LINE_COMMENT"        : reduce_line_comment,
               "COMMENT"             : reduce_comment,
               "STRING_LITERAL"      : reduce_string_literal,
               "IDENTIFIER_NONDIGIT" : reduce_identifier_nondigit,
               "IDENTIFIER"          : reduce_identifier,
               "HEADER_NAME_START"   : reduce_headername_start,
               "PP_DIRECTIVE"        : reduce_PP_DIRECTIVE,
               "KEYWORD"             : reduce_KEYWORD,
               "P_IDENTIFIER"        : reduce_p_identifier
                              }


#----------------------------------------------------------------
# Phase 3 consists of decomposing into preprocessing tokens and replacing
#         comments with single white space
# in this phase we will detect // and /* and */ for comments
#-----------------------------------------------------------------
def phase3_decompose_preprocessing_tokens2( mylexer ):

    token_stack = []
    
    token = ["","","",""]
    result = False
    reduced_token = ["",""]

    token = mylexer.get_next_token()

    while ( token[0] != "EOF" ):

        print ("token:",token,"\n")

        something_changed = True
        while (something_changed == True):
            
            # now reduce the stack
            if len( token_stack ) > 0:
               last_token = token_stack.pop()

               print("calling:",jump_table.get( last_token[ 0 ], myError))

               result, reduced_token = jump_table.get( last_token[ 0 ], myError)( token, last_token )
                
               if result == True:
                   print("Reduced: (prev)", last_token,"(new):", token, "reduced to:",reduced_token)
                   token_stack.append( reduced_token )
                   something_changed = True
                   print ( "stack:",token_stack )
                   token = token_stack.pop()
                   

               else:
                   print("Appending:", last_token, token)
                   token_stack.append( last_token )
                   token_stack.append( token )
                   something_changed=False
                   print ( "stack:",token_stack )
               
            else:
                token_stack.append( token )
                something_changed=False
                print ( "stack:",token_stack )

        token = mylexer.get_next_token()
            
    return token_stack

#----------------------------------------------------------------
# phase3_alternative

def update_token( token_type, previous_token, new_token ):

    previous_token[0] = token_type
    previous_token[1] += new_token[1]
    previous_token[2] = new_token[2]
    previous_token[3] = new_token[3]

    return previous_token

def phase3_decompose_preprocessing_tokens( mylexer ):

    token_stack = []
    state = "start"
    output_token = ["","","",""]
    complete_token = False

    token = mylexer.get_next_token() # this returns a token of type NON-DIGIT, DIGIT, PUNCTUATION or WHITESPACE


    # State table is based on a multiple ley dictionary (a list for the key and value). The key list uses the current state
    # and the input character to determine which next_state and action are to be executed.

    #               current_state  Input_char             next_state    action    token_type
    
    state_table = { ( "start", "NON-DIGIT" )        :   ( "identifier", "update", "IDENTIFIER" ),
                    ( "start","DIGIT" )             :   ( "constant", "update", "PP_NUMBER"),
                    ( "start", "PERIOD" )           :   ( "constant-start", "", "PP_NUMBER" ),
                    ( "start", "QUOTE" )            :   ( "string", "", "STRING" ),
                    ( "start", "FORWARD_SLASH" )    :   ( "comment-start", "", "COMMENT" ),
                    ( "start", "WHITESPACE" )       :   ( "start", "eat", "" ),
                    ( "start", "PUNCTUATION" )      :   ( "start", "issue", "PUNCTUATION" ),
    
                    ( "identifier", "PUNCTUATION")  :   ( "start", "issue",""),
                    ( "identifier", "WHITESPACE")   :   ( "start", "issue", ""),
                    ( "identifier", "NON_DIGIT")    :   ( "identifier", "update", "IDENTIFIER"),
                    ( "identifier", "DIGIT")        :   ( "identifier", "update", "IDENTIFIER"),
                    ( "identifier", "EOF")          :   ( "start", "issue", ""),

                    ( "constant-start", "DIGIT")    :   ( "constant", "update", "PP_NUMBER"),
                    ( "constant-start", "NON_DIGIT"):   ( "identifier", "issue_push", "PUNCTUATION"),
                    
                    ( "constant", "DIGIT")          :   ( "constant", "update", "PP_NUMBER"),
                    ( "constant", "PERIOD")         :   ( "constant", "update", "PP_NUMBER"),
                    ( "constant", "NON-DIGIT")      :   ( "start", "error", ""),
                    ( "constant", "PUNCTUATION")    :   ( "start", "issue_push", ""),
                    ( "constant", "WHITESPACE")     :   ( "start", "issue", ""),
                    ( "constant", "EOF")            :   ( "start", "issue", ""),
    
                    ( "string", "PUNCTUATION")      :   ( "start", "issue", ""),
    
                    ( "comment", "PUNCTUATION")     :   ( "start", "issue", ""),
    
                    ( "header", "PUNCTUATION")      :   ( "start", "issue", "")
                  }

    error_action = ["error","error",""]
                     
    # Tokens that need to be identified:   "  <  /  \  *  -  + . "
    finish = False

    previous_lexeme = ["","","",""]
    while ( finish != True ):

        if token[0]=="PUNCTUATION" and token[1]==".":
            token[0]="PERIOD"

        print("token:",token)
        actions = state_table.get( (state , token[0]), error_action )
        state = actions[0]
        print("actions:",actions, "state:",state)
        
        if ( actions[1] == "update" ):
            token = update_token( actions[2], previous_lexeme, token )
            print("updated token:",token)
            
        elif ( actions[1] == "issue" ):
            token_stack.append(previous_lexeme)
            print("appending token stack:",token_stack)
            token[1] = "" # to obliterate prior to setting previous_lexeme.
            
        elif ( actions[1] == "push" ):
            mylexer.push_back_token()
            
        elif ( actions[1]=="error" ):
            token[0]="ERROR"
            token[1] = previous_lexeme[1] + token[1]
            print("Error:", token[1] , " at line:", token[2], " at position:",token[3])
            token_stack.append(token)
            break # 8-/
        
        elif ( actions[1] == "issue_push" ):
            token_stack.append(previous_lexeme)
            print("appending (with pushback) token stack:",token_stack, "push:", token, "state:", state, "previous lexeme",previous_lexeme)
            mylexer.push_back_token()
            token[1] = "" # to obliterate prior to setting previous_lexeme.

        previous_lexeme = token

        if token[0] == "EOF":
            finish= True

        token = mylexer.get_next_token()

                
    print ("final stack:",token_stack)
    return token_stack

#----------------------------------------------------------------
# Phase 4 execute preprocessing directives. Macros are expanded.
#          #includes are pasted in (running phase 1-4 on each).
#          remove preprocessing directives.
#-----------------------------------------------------------------
def phase4_execute_preprocessing_directives():
    return 1

#----------------------------------------------------------------
# Phase 5 escaped characters are replaced 
#-----------------------------------------------------------------
def phase5_replace_escaped_chars():
    return 1

#----------------------------------------------------------------
# Phase 6 adjacent string literals are concatenated
#-----------------------------------------------------------------
def phase6_concatenate_strings():
    return 1

#----------------------------------------------------------------
# Phase 7 convert preprocessing tokens to tokens.
#       remove white space tokens
#-----------------------------------------------------------------
def phase7_convert_preprocessing_tokens_to_tokens():
    return 1

#----------------------------------------------------------------
# Phase 8 Link
#-----------------------------------------------------------------
def phase8_link():
    return 1

#--------------------------------
#  Main Routine
#--------------------------------

#init()
#myfile = open("kb_types.h")
#process()
#shutdown()
#myfile.close()

#----------------------------------------------
# Test Cases
#----------------------------------------------

#------------------------------------------------------------------------------------
# Test case Phase 2 1 
# Description: Test Phase 2 of the compiler
#------------------------------------------------------------------------------------
def test_phase2_1():

    test_input = "some line \\\nanother line"
    output = phase2_glue_line_continuations( test_input )
    assert output=="some line another line"

#------------------------------------------------------------------------------------
# Test case Phase 2 2 
# Description: Test Phase 2 of the compiler
#------------------------------------------------------------------------------------
def test_phase2_2():

    test_input = "some line \\another line"
    output = phase2_glue_line_continuations( test_input )
    assert output=="some line \\another line"
#------------------------------------------------------------------------------------
# Test case Phase 2 3
# Description: Test Phase 2 of the compiler
#------------------------------------------------------------------------------------
def test_phase2_3():

    test_input = "some line \nanother line"
    output = phase2_glue_line_continuations( test_input )
    assert output=="some line \nanother line"



#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 1 - checking PP_Number
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p1():

    #initial test to check tokens are correctly builts
    mylexer = Lexer( "1234" )
    output = phase3_decompose_preprocessing_tokens( mylexer )
    assert output[0] == ["PP_NUMBER", "1234", 1, 3]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 2 - checking PP_Number
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p2():

    #initial test to check tokens are correctly builts
    test_input = Lexer("1.234")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1.234", 1, 4]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 3 - checking PP_Number
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p3():

    #initial test to check tokens are correctly builts
    test_input = Lexer("0.234")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "0.234", 1, 4]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 4 - checking PP_Number
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p4():

    #initial test to check tokens are correctly builts
    test_input = Lexer(".234")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", ".234", 1, 3]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 5 - checking PP_Number - malformed
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p5():

    #initial test to check tokens are correctly builts
    test_input = Lexer(".A34")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PERIOD", ".", 1, 0]
    assert output[1] == ["IDENTIFIER", "A34", 1, 3]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 6 - checking PP_Number - malformed
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p6():

    #initial test to check tokens are correctly builts
    test_input = Lexer("0.A34")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["ERROR", "0.A", 1, 2]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 7 - checking PP_Number - malformed
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p7():

    #initial test to check tokens are correctly builts
    test_input = Lexer("0.1A34")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["ERROR", "0.1A", 1, 3]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 8 - checking PP_Number - malformed
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p8():

    #initial test to check tokens are correctly builts
    test_input = Lexer("0.1!34")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "0.1", 1, 2]
    assert output[1] == ["PUNCTUATION", "!", 1, 3]
    assert output[2] == ["PP_NUMBER", "34", 1, 4]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 9 - checking PP_Number - punctuation terminated
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p9():

    #initial test to check tokens are correctly builts
    test_input = Lexer("0.1234;")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", ".234", 1, 0]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 10 - checking PP_Number - space seperator
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p10():

    #initial test to check tokens are correctly builts
    test_input = Lexer("0.1 234;")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", ".234", 1, 0]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req 11 - checking PP_Number - newline seperator
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_p11():

    #initial test to check tokens are correctly builts
    test_input = Lexer("0.1\n234;")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", ".234", 1, 0]     
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req B1 - checking  String Literals
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_B1():

    #initial test to check tokens are correctly builts
    test_input = Lexer("a=\"some string\";")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "a", 1, 0]
    assert output[1] == ["PUNCTUATION", "=", 1, 1]
    assert output[2] == ["STRING", "some string", 1, 2]
    assert output[3] == ["PUNCTUATION", ";", 1, 15]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C1 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C1():

    #initial test to check tokens are correctly builts
    test_input = Lexer("a=35")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "a",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 1]
    assert output[2] == ["PP_NUMBER", "35",1,2]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C1b - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C1b():

    #initial test to check tokens are correctly builts
    test_input = Lexer("a/35")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "a",1, 0]
    assert output[1] == ["PUNCTUATION", "/",1, 1]
    assert output[2] == ["PP_NUMBER", "35",1,2]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C2 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C2():

    #initial test to check tokens are correctly builts
    test_input = Lexer("_a=35")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "_a",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 2]
    assert output[2] == ["PP_NUMBER", "35",1, 3]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C3 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C3():

    #initial test to check tokens are correctly builts
    test_input = Lexer("aa=35")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "aa",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 2]
    assert output[2] == ["PP_NUMBER", "35",1, 3]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C4 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C4():

    #initial test to check tokens are correctly builts
    test_input = Lexer("a25 =35")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "a25",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 4]
    assert output[2] == ["PP_NUMBER", "35",1, 5]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C5 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C5():

    #initial test to check tokens are correctly builts
    test_input = Lexer("aa25 =bb25 ")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "aa25",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 5]
    assert output[2] == ["IDENTIFIER", "bb25",1, 6]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C6 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C6():

    #initial test to check tokens are correctly builts
    test_input = Lexer("aa25 = bb25 ")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "aa25",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 5]
    assert output[2] == ["IDENTIFIER", "bb25",1, 7]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C7 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C7():

    #initial test to check tokens are correctly builts
    test_input = Lexer("aa25 = bb25;")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "aa25",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 5]
    assert output[2] == ["IDENTIFIER", "bb25",1, 7]
    assert output[3] == ["PUNCTUATION", ";",1, 11]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C8 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C8():

    #initial test to check tokens are correctly builts
    test_input = Lexer("aa25!=bb25;")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "aa25",1, 0]
    assert output[1] == ["PUNCTUATION", "!",1, 4]
    assert output[2] == ["PUNCTUATION", "=",1, 5]
    assert output[3] == ["IDENTIFIER", "bb25",1, 6]
    assert output[4] == ["PUNCTUATION", ";",1, 10]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C9 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C9():

    #initial test to check tokens are correctly builts
    test_input = Lexer("aa25/bb25;")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "aa25",1, 0]
    assert output[1] == ["PUNCTUATION", "/",1, 4]
    assert output[2] == ["IDENTIFIER", "bb25",1, 5]
    assert output[3] == ["PUNCTUATION", ";",1, 9]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C10 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C10():

    #initial test to check tokens are correctly builts
    test_input = Lexer("aa25+=bb25;")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "aa25",1, 0]
    assert output[1] == ["PUNCTUATION", "+",1, 4]
    assert output[2] == ["PUNCTUATION", "=",1, 5]
    assert output[3] == ["IDENTIFIER", "bb25",1, 6]
    assert output[4] == ["PUNCTUATION", ";",1, 10]
#------------------------------------------------------------------------------------
# Test case Phase 3 pre-req C11 - checking  Identifiers
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_C11():

    #initial test to check tokens are correctly builts
    test_input = Lexer("aa25(int bb25);")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "aa25",1, 0]
    assert output[1] == ["PUNCTUATION", "(",1, 4]
    assert output[2] == ["IDENTIFIER", "int",1, 5]
    assert output[3] == ["IDENTIFIER", "bb25",1, 9]
    assert output[4] == ["PUNCTUATION", ")",1, 13]
    assert output[5] == ["PUNCTUATION", ";",1, 14]
#------------------------------------------------------------------------------------
# Test case Phase 3 1
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_1():

    #initial test to just push a bunch of tokens into a token stream
    #test_input = "/* comment */comment"
    test_input = Lexer("1234 a word;")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["WHITESPACE"," ",1, 4]
    assert output[2] == ["IDENTIFIER","a",1, 5]
    assert output[3] == ["WHITESPACE"," ",1, 6]
    assert output[4] == ["IDENTIFIER","word",1, 7]
#------------------------------------------------------------------------------------
# Test case Phase 3 2
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_2():

    test_input = Lexer("1234/* comment */ a word ")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["COMMENT","/* comment */",1, 4]
    assert output[2] == ["WHITESPACE"," ",1, 17]
    assert output[3] == ["IDENTIFIER","a",1, 18]
    assert output[4] == ["WHITESPACE"," ",1, 19]
    assert output[5] == ["IDENTIFIER","word",1, 20]

#------------------------------------------------------------------------------------
# Test case Phase 3 3
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_3():

    test_input = Lexer("1234/* comment /* a word")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["MULTILINE_COMMENT","/* comment /* a word",1, 4]

#------------------------------------------------------------------------------------
# Test case Phase 3 4
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_4():

    test_input = Lexer("1234/**/")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["COMMENT","/**/",1, 4]

#------------------------------------------------------------------------------------
# Test case Phase 3 5
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_5():

    test_input = Lexer("1234/* some text" + '\n' +  "more text */")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["COMMENT","/* some text" + '\n' +  "more text */",1, 4]

#------------------------------------------------------------------------------------
# Test case Phase 3 6
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_6():

    test_input = Lexer("1234// some text\n") 
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["COMMENT","// some text",1, 4]
#------------------------------------------------------------------------------------
# Test case Phase 3 7
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_7():

    test_input = Lexer("1234// /*some text\n") 
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["COMMENT","// /*some text",1, 4]

#------------------------------------------------------------------------------------
# Test case Phase 3 8
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_8():

    test_input = Lexer("1234// /*some text */\n") 
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["COMMENT","// /*some text */",1, 4]
#------------------------------------------------------------------------------------
# Test case Phase 3 9
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_9():

    test_input = Lexer("1234// */some text */\n") 
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["DIGIT", "1234",1, 0]
    assert output[1] == ["COMMENT","// */some text */",1, 4]

#------------------------------------------------------------------------------------
# Test case Phase 3 9
# Description: Test Phase 3 of the compiler
#------------------------------------------------------------------------------------
def test_phase3_9():

    test_input = Lexer("1234// */some text */\n") 
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_NUMBER", "1234",1, 0]
    assert output[1] == ["COMMENT","// */some text */",1, 4]
#------------------------------------------------------------------------------------
# Test case Phase 3 10
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_10():

    test_input = Lexer("\"a//b\"") 
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["STRING", "a//b",1, 0]

#------------------------------------------------------------------------------------
# Test case Phase 3 11
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_11():

    test_input = Lexer("#include \"//e\"" )
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "//e",1, 0,"LOCAL_INCLUDE"]
        
#------------------------------------------------------------------------------------
# Test case Phase 3 12
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_12():

    test_input = Lexer( "// */\n" )
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["COMMENT", "// */",1, 0]    
#------------------------------------------------------------------------------------
# Test case Phase 3 13
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_13():

    test_input = Lexer("f=g/**//h;\n" )
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "f",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 1]
    assert output[2] == ["IDENTIFIER", "g",1, 2]
    assert output[3] == ["COMMENT", "/**/",1, 3]
    assert output[4] == ["PUNCTUATION", "/",1, 7]
    assert output[5] == ["IDENTIFIER", "h",1, 8]
    assert output[6] == ["PUNCTUATION", ";",1, 9]
    assert output[7] == ["WHITESPACE", "\n",1, 10]
    
#------------------------------------------------------------------------------------
# Test case Phase 3 14
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_14():

    test_input = "/\\\n/ j();\n" #part of a two line comment
    p2_output = phase2_glue_line_continuations(test_input)
    output = phase3_decompose_preprocessing_tokens( Lexer(p2_output) )
    assert output[0] == ["COMMENT", "// j();",1, 0]
#------------------------------------------------------------------------------------
# Test case Phase 3 15
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_15():

    test_input = "//\\\ni();\n" 
    p2_output = phase2_glue_line_continuations(test_input)
    output = phase3_decompose_preprocessing_tokens( Lexer(p2_output)  )
    assert output[0] == ["COMMENT", "//i();",1, 0]
#------------------------------------------------------------------------------------
# Test case Phase 3 16
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_16():

    test_input = Lexer("/*//*/ l();" )
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["COMMENT", "/*//*/",1, 0]
    assert output[1] == ["WHITESPACE"," ",1, 6]
    assert output[2] == ["IDENTIFIER","l",1, 7]
    assert output[3] == ["PUNCTUATION","(",1, 8]
    assert output[4] == ["PUNCTUATION",")",1, 9]
    assert output[5] == ["PUNCTUATION",";",1, 10]
#------------------------------------------------------------------------------------
# Test case Phase 3 17
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_17():

    test_input = Lexer("m=n//**/o\n +p;\n" )
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["IDENTIFIER", "m",1, 0]
    assert output[1] == ["PUNCTUATION", "=",1, 1]
    assert output[2] == ["IDENTIFIER", "n",1, 2]
    assert output[3] == ["COMMENT", "//**/o",1, 3]
    assert output[4] == ["WHITESPACE", " ",2, 0]
    assert output[5] == ["PUNCTUATION", "+",2, 1]
    assert output[6] == ["IDENTIFIER", "p",2, 2]
    assert output[7] == ["PUNCTUATION", ";",2, 3]
    assert output[8] == ["WHITESPACE", "\n",2, 4]
#----------------------------------------------------------------------------------------------------------------

                        # include tests
        
#------------------------------------------------------------------------------------
# Test case Phase 3 D1a - Header names
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_D1a():

    test_input = Lexer("#include <myfile.h>" )
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"STANDARD_INCLUDE"]
#------------------------------------------------------------------------------------
# Test case Phase 3 D1b - Header names - malformed start (not first position) However C11 states that it is now legal to except
#                                        # after any number of whitespace (as long at least one new line exists).
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_D1b():

    test_input = Lexer(" #include <myfile.h>" )
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[1] == ["PP_INCLUDE", "myfile.h",1,1,"STANDARD_INCLUDE"]

#------------------------------------------------------------------------------------
# Test case Phase 3 D2 - Header names
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_D2():

    test_input = Lexer("#include \"myfile.h\"" )
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]
#---------------------------------------------------------------------------------------------------------------

                            # Define tests
 
#------------------------------------------------------------------------------------
# Test case Phase 3 E1a - #DEFINE correctly formed single replacement token
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E1a():

    test_input = Lexer("#define TRUE 1\n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_DIRECTIVE", "define",1,0,"TRUE","1"]
#------------------------------------------------------------------------------------
# Test case Phase 3 E1b - #DEFINE correctly formed single replacement token
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E1b():

    test_input = Lexer("#define TRUE false\n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]
#------------------------------------------------------------------------------------
# Test case Phase 3 E1c - #DEFINE correctly formed single replacement token
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E1c():

    test_input = Lexer("#define TRUE (0x1)\n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]   
#------------------------------------------------------------------------------------
# Test case Phase 3 E2a - #DEFINE correctly formed multiple token replacement
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E2a():

    test_input = Lexer("#define TRUE some_text more_text\n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]    
#------------------------------------------------------------------------------------
# Test case Phase 3 E2b - #DEFINE correctly formed multiple token replacement
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E2b():

    test_input = Lexer("#define TRUE some_text 51\n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]    
#------------------------------------------------------------------------------------
# Test case Phase 3 E2c - #DEFINE correctly formed multiple token replacement
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E2c():

    test_input = Lexer("#define TRUE some_text (51)\n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]    

#------------------------------------------------------------------------------------
# Test case Phase 3 E2d - #DEFINE malformed (no new line at end)
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E2d():

    test_input = Lexer("#define TRUE some_text more_text")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]
#------------------------------------------------------------------------------------
# Test case Phase 3 E3a - #DEFINE with single parameter
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E3a():

    test_input = Lexer("#define TRUE( p1 ) some_text p1 more_text\n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]
#------------------------------------------------------------------------------------
# Test case Phase 3 E3b - #DEFINE with multiple parameters
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E3b():

    test_input = Lexer("#define TRUE(p1, p2) p1+p2 \n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]
#------------------------------------------------------------------------------------
# Test case Phase 3 E3c - #DEFINE with multiple parameters and replacement in brackets
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E3c():

    test_input = Lexer("#define TRUE(p1, p2) ((p1)+(p2)) \n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]

#------------------------------------------------------------------------------------
# Test case Phase 3 E3d - #DEFINE with multiple parameters and multiple replacement token (parameters not used)
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E3d():

    test_input = Lexer("#define TRUE(p1,p2) some_text more_text\n")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]
#------------------------------------------------------------------------------------
# Test case Phase 3 E3e - #DEFINE with multiple parameters and multiple replacement token but malformed end
# Description: Test Phase 3 of the compiler (test case from the C Standard:2007
#------------------------------------------------------------------------------------
def test_phase3_E3e():

    test_input = Lexer("#define TRUE(p1, p2 ) some_text more_text")
    output = phase3_decompose_preprocessing_tokens( test_input )
    assert output[0] == ["PP_INCLUDE", "myfile.h",1,0,"LOCAL_INCLUDE"]
    
