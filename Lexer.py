### Lexer class


class Lexer:

    lookup_symbol = {'0'  : "DIGIT",
                     '1'  : "DIGIT",
                     '2'  : "DIGIT",
                     '3'  : "DIGIT",
                     '4'  : "DIGIT",
                     '5'  : "DIGIT",
                     '6'  : "DIGIT",
                     '7'  : "DIGIT",
                     '8'  : "DIGIT",
                     '9'  : "DIGIT",
                    
                     'a'  : "NON_DIGIT",
                     'b'  : "NON_DIGIT",
                     'c'  : "NON_DIGIT",
                     'd'  : "NON_DIGIT",
                     'e'  : "NON_DIGIT",
                     'f'  : "NON_DIGIT",
                     'g'  : "NON_DIGIT",
                     'h'  : "NON_DIGIT",
                     'i'  : "NON_DIGIT",
                     'j'  : "NON_DIGIT",
                     'k'  : "NON_DIGIT",
                     'l'  : "NON_DIGIT",
                     'm'  : "NON_DIGIT",
                     'n'  : "NON_DIGIT",
                     'o'  : "NON_DIGIT",
                     'p'  : "NON_DIGIT",
                     'q'  : "NON_DIGIT",
                     'r'  : "NON_DIGIT",
                     's'  : "NON_DIGIT",
                     't'  : "NON_DIGIT",
                     'u'  : "NON_DIGIT",
                     'v'  : "NON_DIGIT",
                     'w'  : "NON_DIGIT",
                     'x'  : "NON_DIGIT",
                     'y'  : "NON_DIGIT",
                     'z'  : "NON_DIGIT",

                    'A'  : "NON_DIGIT",
                    'B'  : "NON_DIGIT",
                    'C'  : "NON_DIGIT",
                    'D'  : "NON_DIGIT",
                    'E'  : "NON_DIGIT",
                    'F'  : "NON_DIGIT",
                    'G'  : "NON_DIGIT",
                    'H'  : "NON_DIGIT",
                    'I'  : "NON_DIGIT",
                    'J'  : "NON_DIGIT",
                    'K'  : "NON_DIGIT",
                    'L'  : "NON_DIGIT",
                    'M'  : "NON_DIGIT",
                    'N'  : "NON_DIGIT",
                    'O'  : "NON_DIGIT",
                    'P'  : "NON_DIGIT",
                    'Q'  : "NON_DIGIT",
                    'R'  : "NON_DIGIT",
                    'S'  : "NON_DIGIT",
                    'T'  : "NON_DIGIT",
                    'U'  : "NON_DIGIT",
                    'V'  : "NON_DIGIT",
                    'W'  : "NON_DIGIT",
                    'X'  : "NON_DIGIT",
                    'Y'  : "NON_DIGIT",
                    'Z'  : "NON_DIGIT",

                    '_'  : "NON_DIGIT",

                    ' '  : "WHITESPACE",
                    '\t' : "WHITESPACE",
                    '\n' : "WHITESPACE",
                    '\v' : "WHITESPACE",

                    '!'  : "PUNCTUATION",
                    '"'  : "PUNCTUATION",
                    '#'  : "PUNCTUATION",
                    '$'  : "PUNCTUATION",
                    '%'  : "PUNCTUATION",
                    '&'  : "PUNCTUATION",
                    '\''  : "PUNCTUATION",
                    '('  : "PUNCTUATION",
                    ')'  : "PUNCTUATION",
                    '*'  : "PUNCTUATION",
                    '+'  : "PUNCTUATION",
                    ','  : "PUNCTUATION",
                    '-'  : "PUNCTUATION",
                    '.'  : "PUNCTUATION",
                    '/'  : "PUNCTUATION",
                    
                    
                    ':'  : "PUNCTUATION",
                    ';'  : "PUNCTUATION",
                    '<'  : "PUNCTUATION",
                    '='  : "PUNCTUATION",
                    '>'  : "PUNCTUATION",
                    '?'  : "PUNCTUATION",
                    '@'  : "PUNCTUATION",

                    '['  : "PUNCTUATION",
                    '\\'  : "PUNCTUATION",
                    ']'  : "PUNCTUATION",
                    '^'  : "PUNCTUATION",

                    '{'  : "PUNCTUATION",
                    '|'  : "PUNCTUATION",
                    '}'  : "PUNCTUATION",
                    '~'  : "PUNCTUATION"     
                }

    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.line_count = 1
        self.line_position = 0
        self.line_index = 0
        self.size = len (input_stream)
        self.state = "start"
        self.lexem = ""
        self.current_token = [ "","",0,0 ]

    def get_next_token2( self ):



        if self.line_index < self.size:

            mychar = self.input_stream[ self.line_index ]

            token_type = lookup_symbol.get( mychar, "ERROR" )
            token =  [token_type, mychar, self.line_count, self.line_position ]
        
            if mychar == '\n':
                self.line_count += 1
                self.line_position = -1

            self.line_index += 1
            self.line_position += 1
            
        else:
            token = ["EOF", "" , self.line_count, self.line_position]
            
        return token

            
    #--------------------------------------------------------------------------------------
    # These are the state machines
    def build_lexeme( self, char , next_char):

        lexeme_found = False
        print ("INP state:",self.state, " char:",char, " next char:",next_char, "type:",self.lookup_symbol.get( char, "ERROR" ))
        if ( self.state == "start" ):

            if ( ( self.lookup_symbol.get( char, "ERROR" ) == "NON_DIGIT" ) or ( char == "_" )):

                self.current_token[ 0 ] = "Identifier"
                self.current_token[ 1 ] = char
                self.current_token[ 2 ] = self.line_count
                self.current_token[ 3 ] = self.line_position
                if ( (self.lookup_symbol.get( next_char, "ERROR" ) != "PUNCTUATION" ) and (self.lookup_symbol.get( next_char, "ERROR" ) != "WHITESPACE" )):
                    self.state = "identifier"
                else:
                    self.state = "start"
                    lexeme_found = True
            elif ( self.lookup_symbol.get( char, "ERROR" ) == "DIGIT" ):
                self.current_token[ 0 ] = "pp-number"
                self.current_token[ 1 ] = char
                self.current_token[ 2 ] = self.line_count
                self.current_token[ 3 ] = self.line_position
                if ( (self.lookup_symbol.get( next_char, "ERROR" ) != "PUNCTUATION" ) and (self.lookup_symbol.get( next_char, "ERROR" ) != "WHITESPACE" )):
                    self.state = "pp-number"
                else:
                    self.state = "start"
                    lexeme_found = True
            elif ( char == "/" and next_char == "*" ):
                self.current_token[ 0 ] = "comment"
                self.current_token[ 1 ] = char
                self.current_token[ 2 ] = self.line_count
                self.current_token[ 3 ] = self.line_position
                self.state = "comment"
            elif ( char=="/" and next_char=="/" ):
                self.current_token[ 0 ] = "line-comment"
                self.current_token[ 1 ] = char
                self.current_token[ 2 ] = self.line_count
                self.current_token[ 3 ] = self.line_position
                self.state = "line-comment"
            elif (char == "EOF"):
                self.current_token[ 0 ] = "EOF"
                self.current_token[ 1 ] = ""
                self.current_token[ 2 ] = self.line_count
                self.current_token[ 3 ] = self.line_position
                self.state = "start"
                lexeme_found = True
            elif ( self.lookup_symbol.get( char, "ERROR" ) == "PUNCTUATION" ):
                self.current_token[ 0 ] = "PUNCTUATION"
                self.current_token[ 1 ] = char
                self.current_token[ 2 ] = self.line_count
                self.current_token[ 3 ] = self.line_position
                self.state = "start"
                lexeme_found = True
            else:
                state="start"
                # just eat this token.

        elif ( self.state == "identifier" ):
            
            if (( self.lookup_symbol.get( char, "ERROR" ) == "NON_DIGIT" ) or ( self.lookup_symbol.get( char, "ERROR" ) == "DIGIT" ) or (char=="_")):
                self.current_token[ 0 ] = "Identifier"
                self.current_token[ 1 ] += char
                if ( self.lookup_symbol.get( next_char, "ERROR")=="PUNCTUATION"  or self.lookup_symbol.get( next_char, "ERROR")=="WHITESPACE" ):
                    self.state="start"
                    lexeme_found = True
            elif (char == "EOF" or self.lookup_symbol.get( next_char, "ERROR")=="PUNCTUATION" ):
                self.state = "start"
                lexeme_found = True
            else:
                state="start"
                lexeme_found = True

        elif ( self.state == "pp-number" ):
            if ( self.lookup_symbol.get( char, "ERROR" ) == "DIGIT" ):
                self.state = "pp-number"
                self.current_token[ 1 ] += char
                if ( self.lookup_symbol.get( next_char, "ERROR")=="PUNCTUATION"  or self.lookup_symbol.get( next_char, "ERROR")=="WHITESPACE" ):
                    self.state="start"
                    lexeme_found = True
            else:
                self.state="start"
                lexeme_found = True

        elif ( self.state == "comment" ):
            if ( char == "*" and next_char == "/" ):
                self.current_token[1] += "*/"
                self.state="start"
                lexeme_found = True
                self.line_index += 1
            else:
                self.state = "comment"
                self.current_token[ 1 ] += char
        elif ( self.state =="line-comment" ):
            if ( char =="\n" or char=="EOF"):
                self.state="start"
                lexeme_found = True
            else:
                self.current_token[ 1 ] += char

        print("RET state:",self.state, " char:",char, " next char:",next_char, "found:",lexeme_found, "idx:",self.line_index)
        return lexeme_found

    #--------------------------------------------------------------------------------------
    # Get_next_token() will return a token containing the whole lexeme from an input stream.
    #--------------------------------------------------------------------------------------
    def get_next_token( self ):
        print("Get_Next_Token() called")
        lexeme_found = False

        while ( lexeme_found == False ):
    
            if ( self.line_index < self.size ):
                mychar = self.input_stream[ self.line_index ]
            else:
                mychar = "EOF"
                
            if (self.line_index + 1 < self.size ):
                next_char = self.input_stream[ self.line_index + 1 ]
            else:
                next_char = "EOF"

            print ("input:",mychar," type:",self.lookup_symbol.get( mychar, "ERROR" ))
            
            lexeme_found = self.build_lexeme( mychar, next_char )

            if ( mychar != "EOF"):
                self.update_position( mychar )

        print ("token:", self.current_token )    

        return self.current_token
    
    #--------------------------------------------------------------------------------------
    # update_position() - as characters are read from the input stream the location pointers
    # column and row must be updated. These can be used for locating lexemes in the input file.
    #--------------------------------------------------------------------------------------
    def update_position( self, char ):
        
        if char == '\n':
            self.line_count += 1
            self.line_position = 0
            self.line_index += 1
        else:
            self.line_index += 1
            self.line_position += 1
        print("incr position:", self.line_count, self.line_position )
        
    #--------------------------------------------------------------------------------------     
    def push_back_token( self ):

        self.line_index -=1
        self.line_position -=1

#------------------------------------------------------------------------------------
# Test get_token_type pase 3 utility function
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Test case gnt 1 - checking zero length input stream
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_1():

     mylexer = Lexer( "" )
     assert mylexer.get_next_token() == ["EOF","",1,0]
     assert mylexer.get_next_token() == ["EOF","",1,0]
     assert mylexer.get_next_token() == ["EOF","",1,0]

#------------------------------------------------------------------------------------
     # CHECK Identifier handling
#------------------------------------------------------------------------------------
     
#------------------------------------------------------------------------------------
# Test case gnt 2 - checking single char length input stream
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_2():

     mylexer = Lexer( "a" )
     assert mylexer.get_next_token() == ["Identifier","a",1,0]
     assert mylexer.get_next_token() == ["EOF","",1,1]
     assert mylexer.get_next_token() == ["EOF","",1,1]
#------------------------------------------------------------------------------------
# Test case gnt 3 - checking two char length input stream
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_3():

    mylexer = Lexer( "ab" )
    assert mylexer.get_next_token() == ["Identifier","ab",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,2]
    assert mylexer.get_next_token() == ["EOF","",1,2]
#------------------------------------------------------------------------------------
# Test case gnt 4 - checking three char length input stream
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_4():

    mylexer = Lexer( "abc" )
    assert mylexer.get_next_token() == ["Identifier","abc",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,3]
    assert mylexer.get_next_token() == ["EOF","",1,3]
#------------------------------------------------------------------------------------
# Test case gnt 5 - checking identifier containing number at end
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_5():

    mylexer = Lexer( "abc1" )
    assert mylexer.get_next_token() == ["Identifier","abc1",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,4]
    assert mylexer.get_next_token() == ["EOF","",1,4]    
#------------------------------------------------------------------------------------
# Test case gnt 6 - checking identifier containing numbers at end
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_6():

    mylexer = Lexer( "abc12" )
    assert mylexer.get_next_token() == ["Identifier","abc12",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,5]
    assert mylexer.get_next_token() == ["EOF","",1,5]    
#------------------------------------------------------------------------------------
# Test case gnt 7 - checking identifier containing numbers at end
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_7():

    mylexer = Lexer( "abc123" )
    assert mylexer.get_next_token() == ["Identifier","abc123",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,6]
    assert mylexer.get_next_token() == ["EOF","",1,6]    
#------------------------------------------------------------------------------------
# Test case gnt 8 - checking identifier starting with underscore
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_8():

    mylexer = Lexer( "_" )
    assert mylexer.get_next_token() == ["Identifier","_",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,1]
    assert mylexer.get_next_token() == ["EOF","",1,1]    
#------------------------------------------------------------------------------------
# Test case gnt 9 - checking identifier starting with underscore
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_9():

    mylexer = Lexer( "_abc" )
    assert mylexer.get_next_token() == ["Identifier","_abc",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,4]
    assert mylexer.get_next_token() == ["EOF","",1,4]    
#------------------------------------------------------------------------------------
# Test case gnt 10 - checking identifier starting with underscore
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_10():

    mylexer = Lexer( "_123" )
    assert mylexer.get_next_token() == ["Identifier","_123",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,4]
    assert mylexer.get_next_token() == ["EOF","",1,4]    
#------------------------------------------------------------------------------------
# Test case gnt 11 - checking identifier starting with underscore
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Identifier_11():

    mylexer = Lexer( "_abc123_" )
    assert mylexer.get_next_token() == ["Identifier","_abc123_",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,8]
    assert mylexer.get_next_token() == ["EOF","",1,8]    

#------------------------------------------------------------------------------------
# CHECK Number Handling
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Test case gnt 1 - checking identifier starting with underscore
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Number_1():

    mylexer = Lexer( "1" )
    assert mylexer.get_next_token() == ["pp-number","1",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,1]
    assert mylexer.get_next_token() == ["EOF","",1,1]    
#------------------------------------------------------------------------------------
# Test case gnt 2 - checking identifier starting with underscore
# Description: Test get_next_token
#------------------------------------------------------------------------------------
def test_get_next_token_Number_2():

    mylexer = Lexer( "12" )
    assert mylexer.get_next_token() == ["pp-number","12",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,2]
    assert mylexer.get_next_token() == ["EOF","",1,2]

def test_get_next_token_Number_3():

    mylexer = Lexer( "12\n=345;" )
    assert mylexer.get_next_token() == ["pp-number","12",1,0]
    assert mylexer.get_next_token() == ["PUNCTUATION","=",2,0]
    assert mylexer.get_next_token() == ["pp-number","345",2,1]
    assert mylexer.get_next_token() == ["PUNCTUATION",";",2,4]
    assert mylexer.get_next_token() == ["EOF","",2,5]
    assert mylexer.get_next_token() == ["EOF","",2,5]

def test_get_next_token_Number_4():

    mylexer = Lexer("1.234")
    assert mylexer.get_next_token()==["pp-number","1.234",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,2]
    assert mylexer.get_next_token() == ["EOF","",1,2]

def test_get_next_token_Number_5():

    mylexer = Lexer("0.234")
    assert mylexer.get_next_token()==["pp-number","0.234",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,2]
    assert mylexer.get_next_token() == ["EOF","",1,2]

def test_get_next_token_Number_6():

    mylexer = Lexer(".234")
    assert mylexer.get_next_token()==["pp-number",".234",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,2]
    assert mylexer.get_next_token() == ["EOF","",1,2]
#------------------------------------------------------------------------------------
# CHECK Other Handling
#------------------------------------------------------------------------------------
def test_get_next_token_Comment_1():

    mylexer = Lexer( "/*12 */" )
    assert mylexer.get_next_token() == ["comment","/*12 */",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,6]
    assert mylexer.get_next_token() == ["EOF","",1,6]

def test_get_next_token_Comment_2():

    mylexer = Lexer( "/**/" )
    assert mylexer.get_next_token() == ["comment","/**/",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,3]
    assert mylexer.get_next_token() == ["EOF","",1,3]

def test_get_next_token_Comment_3():

    mylexer = Lexer( "/*\n */ " )
    assert mylexer.get_next_token() == ["comment","/*\n */",1,0]
    assert mylexer.get_next_token() == ["EOF","",2,3]
    assert mylexer.get_next_token() == ["EOF","",2,3]

def test_get_next_token_Comment_4():

    mylexer = Lexer( "//" )
    assert mylexer.get_next_token() == ["line-comment","//",1,0]
    assert mylexer.get_next_token() == ["EOF","",1,2]
    assert mylexer.get_next_token() == ["EOF","",1,2]

def test_get_next_token_Comment_5():

    mylexer = Lexer( "a//b" )
    assert mylexer.get_next_token() == ["Identifier", "a",1,0]
    assert mylexer.get_next_token() == ["line-comment","//b",1,1]
    assert mylexer.get_next_token() == ["EOF","",1,4]
    assert mylexer.get_next_token() == ["EOF","",1,4]

def test_get_next_token_Comment_6():

    mylexer = Lexer( "a//bcd\nefg" )
    assert mylexer.get_next_token() == ["Identifier", "a",1,0]
    assert mylexer.get_next_token() == ["line-comment","//bcd",1,1]
    assert mylexer.get_next_token() == ["Identifier", "efg",2,0]
    assert mylexer.get_next_token() == ["EOF","",2,3]
    assert mylexer.get_next_token() == ["EOF","",2,3]

def test_get_next_token_Comment_7():

    mylexer = Lexer( "// abc /* def*/ \nxyz" )
    assert mylexer.get_next_token() == ["line-comment","// abc /* def*/ ",1,0]
    assert mylexer.get_next_token() == ["Identifier", "xyz",2,0]
    assert mylexer.get_next_token() == ["EOF","",2,3]
    assert mylexer.get_next_token() == ["EOF","",2,3]

def test_get_next_token_Comment_8():

    mylexer = Lexer( "abc//def//xyz\ntuv" )
    assert mylexer.get_next_token() == ["Identifier", "abc",1,0]
    assert mylexer.get_next_token() == ["line-comment","//def//xyz",1,3]
    assert mylexer.get_next_token() == ["Identifier", "tuv",2,0]
    assert mylexer.get_next_token() == ["EOF","",2,3]
    assert mylexer.get_next_token() == ["EOF","",2,3]

#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 1 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_1():

    mylexer = Lexer( "a" )
    assert mylexer.get_next_token() == ["Identifier","a",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 2 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_2():

    mylexer = Lexer( "z" )
    assert mylexer.get_next_token() == ["Identifier","z",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 3 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_3():

    mylexer = Lexer( "A" )
    assert mylexer.get_next_token() == ["Identifier","A",1 ,0]        
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 4 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_4():

    mylexer = Lexer( "Z" )
    assert mylexer.get_next_token() == ["Identifier","Z",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 5 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_5():

    mylexer = Lexer( "_" )
    assert mylexer.get_next_token() == ["Identifier","_",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 5 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_6():

    mylexer = Lexer( "0" )
    assert mylexer.get_next_token() == ["pp-number","0",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 7 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_7():

    mylexer = Lexer( "9" )
    assert mylexer.get_next_token() == ["pp-number","9",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 8 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_8():

    mylexer = Lexer( "." )
    assert mylexer.get_next_token() == ["PUNCTUATION",".",1 ,0]
    assert mylexer.get_next_token() == ["EOF","",1,1]
    assert mylexer.get_next_token() == ["EOF","",1,1]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 9 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_9():

    mylexer = Lexer( "#" )
    assert mylexer.get_next_token() == ["PUNCTUATION","#",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 10 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_11():
    
    mylexer = Lexer( " " )
    assert mylexer.get_next_token() == ["WHITESPACE"," ",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 10 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_11():

    mylexer = Lexer( '\\' )
    assert mylexer.get_next_token() == ["PUNCTUATION",'\\',1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 12 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_12():

    mylexer = Lexer( "/" )
    assert mylexer.get_next_token() == ["PUNCTUATION","/",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 13 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_13():

    mylexer = Lexer( "!" )
    assert mylexer.get_next_token() == ["PUNCTUATION","!",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 14 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_14():

    mylexer = Lexer( ":" )
    assert mylexer.get_next_token() == ["PUNCTUATION",":",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 15 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_15():

    mylexer = Lexer( "-" )
    assert mylexer.get_next_token() == ["PUNCTUATION","-",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 16 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_16():

    mylexer = Lexer( "," )
    assert mylexer.get_next_token() == ["PUNCTUATION",",",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 10 - checking correct token type
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_17():

    mylexer = Lexer( "=" )
    assert mylexer.get_next_token() == ["PUNCTUATION","=",1 ,0]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 18 - checking multi calls
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_18():

    mylexer = Lexer( "a=10;" )
    assert mylexer.get_next_token() == ["Identifier","a",1 ,0]
    assert mylexer.get_next_token() == ["PUNCTUATION","=",1 ,1]
    assert mylexer.get_next_token() == ["pp-number","10",1 ,2]
    assert mylexer.get_next_token() == ["PUNCTUATION",";",1 ,4]
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 19 - checking multi line stuff
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_19():

    mylexer = Lexer( "a=\n10\n;" )
    assert mylexer.get_next_token() == ["Identifier","a",1 ,0]
    assert mylexer.get_next_token() == ["PUNCTUATION","=",1 ,1]
    assert mylexer.get_next_token() == ["pp-number","10",2 ,0]
    assert mylexer.get_next_token() == ["PUNCTUATION",";",3 ,0]
    
#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 20 - checking multi calls and EOF
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_20():

    mylexer = Lexer( "=" )
    assert mylexer.get_next_token() == ["PUNCTUATION","=",1 ,0]
    assert mylexer.get_next_token() == ["EOF","",1 ,1]

#------------------------------------------------------------------------------------
# Test case Phase 3 gtt 21 - practise using a loop around the call to get next token
# Description: Test get_token_type
#------------------------------------------------------------------------------------
def test_get_token_type_21():

    mylexer = Lexer( "a=\n10\n;" )

    mytoken = mylexer.get_next_token()

    while mytoken[0] != "EOF":
        print ("token:", mytoken )
        mytoken = mylexer.get_next_token()

     
    
