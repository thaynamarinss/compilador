import ply.yacc as yacc
from anytree import Node, RenderTree # servindo somente para imprimir a arvore do sintatico de forma organizada
from lexico import *


#ANALISADOR SINTATICO:


# Lista de tokens definida anteriormente
#from lexer import tokens

# Regras da gramática
def p_PROGRAMA(p):
    '''PROGRAMA : DECLARACOES PRINCIPAL'''
    p[0] = ('PROGRAMA',p[1],p[2])

def p_PRINCIPAL(p):
    '''PRINCIPAL : BEGIN COMANDO LISTA_COM END'''
    p[0] = ('PRINCIPAL',p[1],p[2], p[3], p[4])

def p_DECLARACOES(p):
    '''DECLARACOES : DEF_CONST DEF_TIPOS DEF_VAR DEF_FUNC'''
    p[0] = ('DECLARACOES', p[1],p[2],p[3],p[4])
    

#fazer condicional quando tem mais de uma opcao
def p_DEF_CONST(p):
    '''DEF_CONST : CONSTANTE DEF_CONST
                 | empty'''
    if len(p) == 3:
        p[0] = ('DEF_CONST', p[1],p[2]) 
    elif len(p) == 2: # para o caso da regra ir para empty
        p[0] = ('DEF_CONST', p[1])
    else:
        pass  

def p_DEF_TIPOS(p):
    '''DEF_TIPOS : TIPO DEF_TIPOS
                 | empty'''
    if len(p) == 3:
        p[0] = ('DEF_TIPOS',p[1],p[2])
    elif len(p) == 2:
        p[0] = ('DEF_TIPOS',p[1])
    else:
        pass

def p_DEF_VAR(p):
    '''DEF_VAR : VARIAVEL DEF_VAR
               | empty'''
    if len(p) == 3:
        p[0] = ('DEF_VAR',p[1],p[2])
    elif len(p) == 2:
        p[0] = ('DEF_VAR',p[1])
    else:
        pass

def p_DEF_FUNC(p):
    '''DEF_FUNC : FUNCAO DEF_FUNC
                | empty'''
    if len(p) == 3:
        p[0] = ('DEF_FUNC',p[1],p[2])
    elif len(p) == 2:
        p[0] = ('DEF_FUNC',p[1])
    else:
        pass


def p_CONSTANTE(p):
    '''CONSTANTE : CONST ID EQUAL CONST_VALOR SEMICOLON'''
    p[0] = ('CONSTANTE', p[1],p[2],p[3],p[4],p[5])

def p_CONST_VALOR(p):
    '''CONST_VALOR : VSTRING
                   | EXP_MAT'''
    p[0] = ('CONST_VALOR',p[1])

def p_TIPO(p):
    '''TIPO : TYPE ID EQUAL TIPO_DADO SEMICOLON'''
    p[0] = ('TIPO', p[1], p[2], p[3], p[4], p[5])

def p_VARIAVEL(p):
    '''VARIAVEL : VAR ID LISTA_ID COLON TIPO_DADO SEMICOLON'''
    p[0] = ('VARIAVEL', p[1], p[2], p[3], p[4], p[5], p[6])

def p_LISTA_ID(p):
    '''LISTA_ID : COMMA ID LISTA_ID
                | empty'''
    if len(p) == 4:
        p[0] = ('LISTA_ID', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('LISTA_ID', p[1])
    else:
        pass
        

def p_CAMPOS(p):
    '''CAMPOS : ID COLON TIPO_DADO LISTA_CAMPOS'''
    p[0] = ('CAMPOS', p[1], p[2], p[3], p[4])

def p_LISTA_CAMPOS(p):
    '''LISTA_CAMPOS : SEMICOLON CAMPOS LISTA_CAMPOS
                    | empty'''
    if len(p) == 4:
        p[0] = ('LISTA_CAMPOS', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('LISTA_CAMPOS', p[1])
    else:
        pass
        

def p_TIPO_DADO(p):
    '''TIPO_DADO : INTEGER
                 | REAL
                 | ARRAY LBRACKETS NUMERO RBRACKETS OF TIPO_DADO
                 | RECORD CAMPOS END
                 | ID'''
    if len(p) == 7:
        p[0] = ('TIPO_DADO', p[1], p[2], p[3], p[4], p[5], p[6])
    elif len(p) == 4:
        p[0] = ('TIPO_DADO', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('TIPO_DADO', p[1])
    else:
        pass


def p_FUNCAO(p):
    '''FUNCAO : FUNCTION NOME_FUNCAO BLOCO_FUNCAO'''
    p[0] = ('FUNCAO', p[1], p[2], p[3])

def p_NOME_FUNCAO(p):
    '''NOME_FUNCAO : ID PARAM_FUNC COLON TIPO_DADO'''
    p[0] = ('NOME_FUNCAO', p[1], p[2], p[3], p[4])

def p_PARAM_FUNC(p):
    '''PARAM_FUNC : LPAREN CAMPOS RPAREN
                  | empty'''
    if len(p) == 4:
        p[0] = ('PARAM_FUNC', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('PARAM_FUNC', p[1])
    else:
        pass

def p_BLOCO_FUNCAO(p):
    '''BLOCO_FUNCAO : DEF_VAR BEGIN COMANDO LISTA_COM END'''
    p[0] = ('BLOCO_FUNCAO', p[1], p[2], p[3], p[4], p[5])

def p_LISTA_COM(p):
    '''LISTA_COM : SEMICOLON COMANDO LISTA_COM
                 | empty'''
    if len(p) == 4:
        p[0] = ('LISTA_COM', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('LISTA_COM', p[1])
    else:
        pass

def p_BLOCO(p):
    '''BLOCO : BEGIN COMANDO LISTA_COM END
             | COMANDO'''
    
    if len(p) == 5:
        p[0] = ('BLOCO', p[1], p[2], p[3], p[4])
    elif len(p) == 2:
        p[0] = ('BLOCO', p[1])
    else:
        pass

def p_COMANDO(p):
    '''COMANDO : ID NOME ASSIGN EXP_MAT
               | WHILE EXP_LOGICA BLOCO
               | IF EXP_LOGICA THEN BLOCO SIN_ELSE
               | WRITE CONST_VALOR
               | READ ID NOME'''
    if len(p) == 6:
        p[0] = ('COMANDO', p[1], p[2], p[3], p[4], p[5])
    elif len(p) == 5:
        p[0] = ('COMANDO', p[1], p[2], p[3], p[4])
    elif len(p) == 4:
        p[0] = ('COMANDO', p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = ('COMANDO', p[1], p[2])
    else:
        pass   

def p_SIN_ELSE(p):
    '''SIN_ELSE : ELSE BLOCO
            | empty'''
    
    if len(p) == 3:
        p[0] = ('SIN_ELSE', p[1], p[2])
    elif len(p) == 2:
        p[0] = ('SIN_ELSE', p[1])
    else:
        pass   

def p_LISTA_PARAM(p):
    '''LISTA_PARAM : PARAMETRO COMMA LISTA_PARAM
            | PARAMETRO
            | empty
    '''
    if len(p) == 4:
        p[0] = ('LISTA_PARAM', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('LISTA_PARAM', p[1])
    else:
        pass   

# Expressão lógica
def p_EXP_LOGICA(p):
    '''
    EXP_LOGICA : EXP_MAT OP_LOGICO EXP_LOGICA
                | EXP_MAT
               
    '''
    if len(p) == 4:
        p[0] = ('EXP_LOGICA', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('EXP_LOGICA', p[1])
    else:
        pass 

def p_EXP_MAT(p):
    '''EXP_MAT : PARAMETRO OP_MAT EXP_MAT
            | PARAMETRO
    '''
    if len(p) == 4:
        p[0] = ('EXP_MAT_AUX', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('EXP_MAT_AUX', p[1])
    else:
        pass 


def p_PARAMETRO(p):
    '''PARAMETRO : ID NOME
                 | NUMERO'''
    if len(p) == 3:
        p[0] = ('PARAMETRO', p[1], p[2])
    elif len(p) == 2:
        p[0] = ('PARAMETRO', p[1])
    else:
        pass 

def p_OP_LOGICO(p):
    '''OP_LOGICO : GREATER
                 | LESS
                 | EQUAL
                 | EXNOT'''

    p[0] = ('OP_LOGICO', p[1])

    

def p_OP_MAT(p):
    '''OP_MAT : PLUS
              | MINUS
              | TIMES
              | DIVIDE'''
    p[0] = ('OP_MAT', p[1])

def p_NOME(p):
    '''NOME : DOT ID NOME
            | LBRACKETS PARAMETRO RBRACKETS
            | LPAREN LISTA_PARAM RPAREN
            | empty'''    
    if len(p) == 4:
        p[0] = ('NOME', p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = ('NOME', p[1])
    else:
        pass 


    

def p_empty(p):
    'empty :'
    pass

# errorsintatico = []
# def p_error(p):
#     errorsintatico.append(p)
#     print(f"Erro de sintaxe na linha {p.lineno} - token inesperado: {p.type}")


print('\n_____________ANALISADOR SINTATICO____________\n')

print("Print da arvores sintatica em arquivo")
def p_error(p):
    print(f"Erro de sintaxe na linha {p.lineno} - token inesperado: {p.type}")
    exit(0)
    

#Cria o sintatico
parser = yacc.yacc()



result = parser.parse(data, lexer=lexer)
#print(result)
#o codigo abaixo esta servindo somente para fins de impressar de da arvore criada pelo parser
#função para percorrer a árvore e criar os nós correspondentes
def create_tree(node):
    #se node for uma tupla(==nó interno da árvore):
    if isinstance(node, tuple): 
        # O primeiro elemento da tupla é o nome do nó
        root = Node(node[0])
        # Os elementos seguintes são os filhos
        for child in node[1:]:
            child_node = create_tree(child)
            child_node.parent = root
        return root
    else:
        # Caso seja uma folha da árvore (valor simples)
        return Node(str(node))

result = parser.parse(data, lexer=lexer)
tree = create_tree(result)

# Imprime a árvore em formato de árvore
# for pre, _, node in RenderTree(tree):
#     print("{}{}".format(pre, node.name))
#imprime a arvore no arquivo txt (fica melhor de visualizar)
with open('arquivo_saida_arvore_sintatica.txt', 'w', encoding='utf-8') as arquivo:
    for pre, _, node in RenderTree(tree):
        linha = f"{pre}{node.name}\n"
        arquivo.write(linha)

#se o sintatico achar um erro ele nao entra na analise semantica