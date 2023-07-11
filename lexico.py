#THAYNÁ MARINS GOMES ALVES
import ply.lex as lex


# Exemplo de código para teste dos analisadores
#função para abrir arquivo txt
#arquivo codigo esta com o exemplo do pdf simpascal
with open('exemplo.txt', encoding='utf-8') as file:
    data = file.read()


#ANALISADOR LEXICO
# Definindo os tokens
tokens = (
    # Palavras-chave
    'VAR', 'CONST','TYPE', 'BEGIN',  'END', 'IF', 'THEN', 'ELSE', 'WHILE',  'OF', 'ARRAY', 'RECORD', 'FUNCTION', 'WRITE', 'READ', 'INTEGER', 'REAL', 
    # Identificadores e literais
    'ID', 'NUMERO', 'VSTRING',
    # Operadores e pontuação
    'DOT','PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'COLON', 'SEMICOLON', 'COMMA', 'LPAREN', 'RPAREN','LBRACKETS', 'RBRACKETS',
    'GREATER', 'LESS', 'EQUAL', 'EXNOT'
)

# Expressões regulares para cada token
t_DOT = r'\.'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r':='
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKETS = r'\['
t_RBRACKETS = r'\]'
t_GREATER = r'>'
t_LESS = r'<'
t_EQUAL = r'='
t_EXNOT = r'!'


# lista/dicionário que mapeia palavras-chave a tipos de token
keywords = {
    'var': 'VAR',
    'const': 'CONST',
    'type': 'TYPE',
    'begin': 'BEGIN',
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',   
    'of': 'OF',
    'array': 'ARRAY',
    'record': 'RECORD',
    'function': 'FUNCTION',
    'write': 'WRITE',
    'read': 'READ',
    'integer':'INTEGER',
    'real': 'REAL',
}


# Expressões regulares para identificadores e palavras-chave
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = keywords.get(t.value, 'ID') #SE t.value está em keyword, o tipo do token é atualizado, se não o tipo do token é mantido como 'ID'.
    return t

# Expressões regulares para números
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_VSTRING(t):
    r'\"[a-zA-Z0-9\s]*\"'  
    t.value = t.value[1:-1] #remove as aspas antes de retornar
    return t

# Expressão regular para ignorar espaços em branco e comentários
t_ignore = ' \t'

def t_COMMENT(t):
    r'\{.*?\}'
    pass

# Função para lidar com erros de análise léxica
def t_error(t):
    print(f"Caractere inválido '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Cria o lexer
lexer = lex.lex()

# Insere o código fonte no lexer
lexer.input(data)
# Itera sobre os tokens e imprime cada um (LEXICO)
print('\n_____________ANALISADOR LEXICO____________\n\n')
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break  # Fim dos tokens
#     print(f'(Type, Value, Line) = ({tok.type}, {tok.value}, {tok.lineno})')

print("print do lexico comentado")

lexer.lineno = 1; # VOLTANDO O VALOR DA LINHA PARA 1 PARA O ANALISADOR SINTATICO
