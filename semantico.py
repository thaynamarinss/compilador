
from sintatico import *

print("__________________________ANALISADOR SEMANTICO__________________________________________\n")
escopo = 'global'

def extract_record_fields(node, symbol_table,classe, escopo, cont_ordem):
    # Verificar se o nó é do tipo "record"
    if node[4][1] == 'record':
        campos_node = node[4][2]
        extract_fields_campos(campos_node, symbol_table, classe, escopo, cont_ordem)

def extract_fields_campos(node, symbol_table, classe, escopo, cont_ordem):
    
    if node[0] == 'CAMPOS':
        id_name = node[1]#[1]
        tipo_name = node[3][1]
        key = id_name+'/'+escopo
        if key in symbol_table:
                print(f"Erro: '{id_name}' já foi definido.")
        else:
            # Adicionar os campos à tabela de símbolos
            symbol_table[key] = {'nome': id_name, 'class': classe, 'tipo': tipo_name, 'escopo': escopo, 'qtd': '-', 'ordem_na_func': cont_ordem}

        if node[4][1] is not None:
            extract_fields_campos(node[4][2], symbol_table, classe, escopo, cont_ordem + 1 if cont_ordem != '-' else cont_ordem)

#A PARTIR DO NODE VARIAVEL VERIFICA SE TEM MAIS LISTAS
def extract_variable_fields(node, symbol_table, escopo, tipo_name): #node = variavel
    lista_id = node[3]
    if  lista_id[1] is not None: #LISTA_ID
        id_name = lista_id[2]
        # Adicionar os campos à tabela de símbolos
        key = id_name+'/'+escopo
        if key in symbol_table:
            print(f"Erro: Variável '{id_name}' já foi definida.")
        else:
            symbol_table[key] = {'nome': id_name, 'class': 'variavel', 'tipo': tipo_name, 'escopo': escopo, 'qtd': '-', 'ordem_na_func': '-'}
        
        extract_variable_fields(lista_id, symbol_table, escopo, tipo_name)



def analyze_semantics(node, symbol_table, escopo):
    if isinstance(node, tuple):

                node_type = node[0]
                if node_type == 'PROGRAMA':
                    analyze_program(node[1], node[2], symbol_table,escopo)
                elif node_type == 'PRINCIPAL':
                    analyze_principal(node, symbol_table,escopo)
                elif node_type == 'DECLARACOES':
                    analyze_declarations(node[1], node[2], node[3], node[4], symbol_table,escopo)
                elif node_type == 'DEF_CONST':
                    analyze_def_const(node[1], node[2], symbol_table,escopo)
                elif node_type == 'DEF_TIPOS':
                    analyze_def_tipos(node[1], node[2], symbol_table,escopo)
                elif node_type == 'DEF_VAR':
                    analyze_def_var(node, symbol_table, escopo)
                elif node_type == 'DEF_FUNC':
                    analyze_def_func(node[1], node[2], symbol_table, escopo)
                elif node_type == 'CONSTANTE':
                    tipo = analyze_const_valor(node[4],symbol_table,escopo)
                    analyze_constante(node[2], tipo , symbol_table, escopo)
                elif node_type == 'TIPO':
                    analyze_tipo(node, symbol_table, escopo)
                elif node_type == 'VARIAVEL':
                    analyze_variavel(node, symbol_table, escopo)
                elif node_type == 'FUNCAO':
                    analyze_funcao(node, symbol_table, escopo)



# Funções separadas para cada bloco 'if'
def analyze_program(declarations, principal, symbol_table, escopo):
    analyze_semantics(declarations, symbol_table, escopo)
    analyze_semantics(principal, symbol_table, escopo)

def count_children(node):
    count = 0
    if isinstance(node, tuple):
        for child in node[1:]:
            count += 1
    return count


def analyze_principal(node, symbol_table, escopo):
    # Percorrer o comando e a lista de comandos
    command = node[2]
    # print("esse é tamanho do commando", count_children(command))
    list_com = node[3]
    analyze_comando(command, symbol_table, escopo)
    analyze_list_com(list_com, symbol_table, escopo)
    
def analyze_bloco_funcao(node, symbol_table, escopo):
    #defvar
    
    if node[1][1] is not None:
        analyze_def_var(node[1], symbol_table, escopo)

    # Percorrer o comando e a lista de comandos
    command = node[3]  
    # print("esse é tamanho do commando", count_children(command))
    list_com = node[4]
    
    analyze_comando(command, symbol_table, escopo)
    analyze_list_com(list_com, symbol_table, escopo)

def analyze_comando(node, symbol_table, escopo): 
    #node = comando
    if node[1] == 'while':
        exp_logica = node[2]
        bloco = node[3]
        analyze_exp_logica(exp_logica, symbol_table, escopo)
        #como bloco = principal:
        if bloco[1] == 'begin':
            analyze_principal(bloco,symbol_table,escopo)
        else:
            analyze_comando(bloco,symbol_table,escopo)
        #devo fazer analise de exp logica?
        #analyze_exp_logica(exp_logica, symbol_table, escopo)
        #analyze_bloco(bloco, symbol_table, escopo) #nao precisa se começar com begin = principal

    elif node[1] == 'if':
        exp_logica = node[2]
        bloco_then = node[4]
        no_sin_else = node[5]

        analyze_exp_logica(exp_logica, symbol_table, escopo)

        #analisa bloco do if
        if bloco_then[1] == 'begin':
            analyze_principal(bloco_then,symbol_table,escopo)
        else:
            analyze_comando(bloco_then,symbol_table,escopo)

        #analisa bloco do else
        if no_sin_else[1] is not None:            
            #else_node = no_sin_else[2]
            if bloco_then[1] == 'begin':
                analyze_principal(no_sin_else[2],symbol_table,escopo)
            else:
                analyze_comando(no_sin_else[2],symbol_table,escopo)

    elif node[1] == 'write':
        #verificando declaração de Id antes do uso
        if node[2][1] == 'EXP_MAT_AUX':
            analyze_exp_mat(node[1],symbol_table,escopo)      

        #const_valor = node[1]l_table or keyglobal not in symbol_table:
        #tipo = analyze_const_valor(const_valor, symbol_table, escopo) #retorna tipos

    elif node[1] == 'read':
        id_nome = node[2]
        key = id_nome+'/'+escopo
        keyglobal = id_nome+'/'+'global'
        if key not in symbol_table and keyglobal not in symbol_table:
            print(f"Erro: Identificador '{id_nome}' não foi declarado no '{escopo} e nem no escopo global.")  
        elif keyglobal in symbol_table and key not in symbol_table:
            analyze_nome(node[1],keyglobal, symbol_table, escopo)
        else:
            analyze_nome(node[1],key, symbol_table, escopo)

    
    elif len(node) == 5 and node[3] == ':=':  #node[1]!= 'COMANDO' and node[1] != 'read' and node[1] != 'write' and node[1] != 'if' and node[1] != 'while' : #se [COMANDO]  ->   [ID] [NOME] (:=) [EXP_MAT]
        id_nome = str(node[1])
        #print('id nome ahhh', id_nome)
        key = id_nome+'/'+escopo
        keyglobal = id_nome+'/'+'global'
        tipos = ['integer', 'real', 'string', 'array'] #so para controle
        #print(key)
        #- Declaração de Id antes do uso
        if key not in symbol_table and keyglobal not in symbol_table:
            print(f"Erro: Identificador '{id_nome}' não foi declarado no escopo '{escopo}' e nem no escopo global.")
        elif keyglobal in symbol_table and key not in symbol_table:
            #- Só permite atribuição com tipos iguais
            id_tipo = symbol_table[keyglobal]['tipo']
            if node[2][1] is not None:
                analyze_nome(node[2],keyglobal,symbol_table,escopo)       

            exp_mat = node[4]
            exp_mat_tipo = analyze_exp_mat(exp_mat, symbol_table, escopo)            
            #print('exp_mat_tipo é', exp_mat_tipo)
            #if any(elem != id_tipo for elem in exp_mat_tipo):
            if (isinstance(exp_mat_tipo, list) and any(elem != id_tipo for elem in exp_mat_tipo)) or (isinstance(exp_mat_tipo, str) and exp_mat_tipo != id_tipo):
                #se forem diferentes ele vai verificar o "subtipo" para ter certeza que são diferentes visto que pode ter uma atribuição de vetor := vetor ou interiro := a[1] (que acaba sendo um inteiro "escondido")
                if exp_mat_tipo not in tipos:   
                    tipo_certo = check_symbol_table(symbol_table, exp_mat_tipo)
                    if tipo_certo:                
                        if 'array' in tipo_certo: #analise especificamente para o caso de array/vetor considera que o acesso vai ser com indice ex: a[i]
                            exp_mat_tipo = tipo_certo                       
                            partes = exp_mat_tipo.split("]")
                            exp_mat_tipo = partes[1].strip() #pega so o tipo do array (integer,etc)
                else:
                    print(f"Erro: Atribuição inválida. O tipo de '{id_nome}' é '{id_tipo}', mas a expressão tem tipo '{exp_mat_tipo}'.")
 
                print(f"Erro: Atribuição inválida. O tipo de '{id_nome}' é '{id_tipo}', mas a expressão tem tipo '{exp_mat_tipo}'.")
        else:          
            #- Só permite atribuição com tipos iguais
            id_tipo = symbol_table[key]['tipo']
           # se tem nome vou na regra nome para pegar o tipo
            if node[2][1] is not None:
                analyze_nome(node[2],key,symbol_table,escopo)
            exp_mat = node[4]           
            exp_mat_tipo = analyze_exp_mat(exp_mat, symbol_table, escopo)  
          
           

            if (isinstance(exp_mat_tipo, list) and any(elem != id_tipo for elem in exp_mat_tipo)) or (isinstance(exp_mat_tipo, str) and exp_mat_tipo != id_tipo):
                #se forem diferentes ele vai verificar o "subtipo" para ter certeza que são diferentes visto que pode ter uma atribuição de vetor := vetor ou interiro := a[1] (que acaba sendo um inteiro "escondido")
                if exp_mat_tipo not in tipos:   
                    tipo_certo = check_symbol_table(symbol_table, exp_mat_tipo)
                    if tipo_certo:                
                        if 'array' in tipo_certo: #analisa especificamente para o caso de array/vetor considera que o acesso vai ser com indice ex: a[i]
                            exp_mat_tipo = tipo_certo                       
                            partes = exp_mat_tipo.split("]")
                            exp_mat_tipo = partes[1].strip() #pega so o tipo do array (integer,etc)
                else:
                    print(f"Erro: Atribuição inválida. O tipo de '{id_nome}' é '{id_tipo}', mas a expressão tem tipo '{exp_mat_tipo}'.")
 

def analyze_list_com(list_com, symbol_table, escopo):
    if list_com[1] is not None:
        analyze_comando(list_com[2], symbol_table, escopo)
        analyze_list_com(list_com[3], symbol_table, escopo)

def analyze_exp_logica(exp_logica, symbol_table, escopo):
    if len(exp_logica) == 4:
        exp_mat = exp_logica[1]  
        outra_exp_logica = exp_logica[3]       
        analyze_exp_mat(exp_mat, symbol_table, escopo)    
        analyze_exp_logica(outra_exp_logica, symbol_table, escopo)    

    elif len(exp_logica) == 2:
        exp_mat = exp_logica[1]
        analyze_exp_mat(exp_mat, symbol_table, escopo)

def analyze_lista_param(lista_param,symbol_table, escopo):
  
    if lista_param[1] is not None:
        if len(lista_param) == 2:
            analyze_parametro(lista_param[1], symbol_table, escopo)
            
            return 1
        elif len(lista_param) == 4:
            analyze_parametro(lista_param[1], symbol_table, escopo) 
            cont= analyze_lista_param(lista_param[3], symbol_table, escopo)       
             
            return 1 + cont
    else:
        return 0

# def count_param(param,symbol_table, escopo, cont):
def analyze_pega_tiposda_lista_param(lista_param, symbol_table, escopo):
    lista_tipos = []
    tipos = ['integer', 'real', 'string', 'array']

    if lista_param[1] is not None:
        if len(lista_param) == 2:
            tipo = analyze_parametro(lista_param[1], symbol_table, escopo)
            if tipo not in tipos:
                tipo_certo = check_symbol_table(symbol_table, tipo)
                if tipo_certo:                    
                    tipo = tipo_certo
                    if 'array' in tipo:                        
                        partes = tipo.split("]")
                        tipo = partes[1].strip()  # Remove espaços em branco antes e depois do texto
                       # print('tipo tando', tipo)            
                else:
                    pass

            lista_tipos.append(tipo)
            return lista_tipos
        elif len(lista_param) == 4:
            tipo = analyze_parametro(lista_param[1], symbol_table, escopo) 
            if tipo not in tipos:
                tipo_certo = check_symbol_table(symbol_table, tipo)
                if tipo_certo:                    
                    tipo = tipo_certo                 
                else:
                    pass            
            lista_tipos.extend(analyze_pega_tiposda_lista_param(lista_param[3], symbol_table, escopo))
            lista_tipos.append(tipo)
            return lista_tipos
    return lista_tipos


def check_symbol_table(symbol_table, value):
    for entry in symbol_table.values():
        if entry['nome'] == value and entry['class'] == 'tipo':
            return entry['tipo']
    return False

def analyze_nome(nome, key, symbol_table, escopo): #key é o id que pega antes do nome
    tipos = ['integer', 'real', 'string', 'array']
    tipo_id= symbol_table[key]['tipo']   #tipo da variavel que antecede o ponto ex: aluno de result 
    class_id = symbol_table[key]['class'] 
    qtd_id = symbol_table[key]['qtd']   

    if tipo_id not in tipos:
        tipo_certo = check_symbol_table(symbol_table, tipo_id)
        if tipo_certo:
            # Faça algo com o tipo_certo            
            tipo_id = tipo_certo
            #print("Tipo correto:", tipo_id)
        else:
            pass#print("Tipo não encontrado na tabela de símbolos")


    #- Só pode usar campo (.) em variáveis do tipo registro
    #- obs: verificação feita em outra função como id-- Só posso acessar campo de registro declarado
    if nome[1] is not None:
        if nome[1][0] == '.':
            if tipo_id != 'record': # in tipos: #nao é do tipo id nao tem chance de ser registro
                print(f"Erro: Você tentou acessar campos (em '{key}') de uma variavel que é não é do tipo record (registro) ")
            analyze_nome(nome[3], key,symbol_table,escopo)
        
        elif nome[1][0] == '[':
            if 'array' not in tipo_id:
                print(f"Erro: Você tentou usar indice em uma variavel que não é do tipo array   (em '{key}')")
            else:
                #pega indice maximo do array
                # Encontrar a posição dos colchetes
                abre_colchete = tipo_id.find('[')
                fecha_colchete = tipo_id.find(']')
                # Extrair a substring entre os colchetes
                #nalizar o tipo inteiro 
                indice_max = tipo_id[abre_colchete + 1:fecha_colchete]
                analyze_parametro(nome[2],symbol_table,escopo) #se for id vai analisar se foi declarada
                num_indice = nome[2][1]                
                if isinstance(num_indice, (int, float)):
                    if int(num_indice) <1 or int(num_indice) > int(indice_max):
                        print(f"Erro: o indice que voce tentou acessar não está dentro das possibilidades do indice do array   (em '{key}')")
                return 'vet_ind'
        if nome[1][0] == '(':
            #print("class id", class_id)
            if class_id != 'funcao':
                    print(f"Erro: não é possivel acessar parametros de uma variavel que não é uma função em '{key}')")
            else:
                tipo_parametros_passados = analyze_pega_tiposda_lista_param(nome[2], symbol_table, escopo)
                #print("\n\nlista teste _______________",tipo_parametros_passados)
                count_parameters = analyze_lista_param(nome[2], symbol_table, escopo)                
                #print("\n\ cont dos param teste _______________",count_parameters)
                #se retornar none é pq nao tem parametros
                if count_parameters == None:
                    count_parameters = 0
                if count_parameters != qtd_id:
                    print(f"Erro: quantidade de parâmetros na chamada da função deve ser igual a da declaração '{key}')")
                
                if (isinstance(tipo_parametros_passados, list) and any(elem != tipo_id for elem in tipo_parametros_passados)) or (isinstance(tipo_parametros_passados, str) and tipo_parametros_passados != tipo_id):
                    print(f"Erro: O tipo dos parametros passados nas funções deve ser igual aos argumentos da funcao '{key}' que é do tipo '{tipo_id}' voce está passando parametros do tipo: '{tipo_parametros_passados}'. )")
                
                #print("count_parameters: ", count_parameters)
           
        


def analyze_exp_mat(exp_mat, symbol_table, escopo):    
   
    if len(exp_mat) == 4: #param + op + outra exp
        parametro = exp_mat[1]
        tipo_param1 = analyze_parametro(parametro, symbol_table, escopo)        
        return [tipo_param1,analyze_exp_mat(exp_mat[3], symbol_table, escopo)]      

    elif len(exp_mat) == 2: #so vai ter parametro
        parametro = exp_mat[1]
        #retorna o tipo 
        return analyze_parametro(parametro, symbol_table, escopo)

def analyze_parametro(parametro, symbol_table, escopo):
#analisa se parametro esta na tabela de simbolos e retorna o tipo
   # tipos = ['integer', 'real', 'string', 'array']



    if len(parametro) == 3:
        #print(parametro[1]+'/'+escopo) 
        id_nome = parametro[1]
        key = id_nome+'/'+escopo
        keyglobal = id_nome+'/'+'global'
        if key not in symbol_table and keyglobal not in symbol_table:
            print(f"Erro: Identificador '{id_nome}' no escopo '{escopo}'não foi declarado.")

        elif keyglobal in symbol_table and key not in symbol_table:
            analyze_nome(parametro[2],keyglobal,symbol_table,escopo)            
            id_tipo = symbol_table[keyglobal]['tipo']     

            # if id_tipo not in tipos:
            #     tipo_certo = check_symbol_table(symbol_table, id_tipo)
            #     if tipo_certo:
            #         # Faça algo com o tipo_certo            
            #         id_tipo = tipo_certo
            #         #print("Tipo correto:", tipo_id)
            #     else:
            #         pass#print("Tipo não encontrado na tabela de símbolos")


            return id_tipo
        else:            
            #print("parametro[2]", parametro[2])
            analyze_nome(parametro[2],key,symbol_table,escopo)
            id_tipo = symbol_table[key]['tipo'] 
            # if id_tipo not in tipos:
            #     tipo_certo = check_symbol_table(symbol_table, id_tipo)
            #     if tipo_certo:
            #         # Faça algo com o tipo_certo            
            #         id_tipo = tipo_certo
            #         #print("Tipo correto:", tipo_id)
            #     else:
            #         pass#print("Tipo não encontrado na tabela de símbolos")                     
            return id_tipo
        

    elif len(parametro) == 2: 
        #print('oi parametro 0',parametro[1])
        if isinstance(parametro[1], int):            
            return 'integer'
        elif isinstance(parametro[1], float):
            return 'real'
       
        

def analyze_const_valor(const_valor, symbol_table, escopo):  
    if const_valor[1][0] == 'EXP_MAT_AUX':
        tipo = analyze_exp_mat(const_valor[1],symbol_table,escopo)
        return tipo
    else:
        return 'string'
     


# def analyze_bloco(bloco, symbol_table, escopo):



    
def analyze_declarations(def_const, def_tipos, def_var, def_func, symbol_table, escopo):
    analyze_semantics(def_const, symbol_table, escopo)
    analyze_semantics(def_tipos, symbol_table, escopo)
    analyze_semantics(def_var, symbol_table, escopo)
    analyze_semantics(def_func, symbol_table, escopo)

def analyze_def_const(constant, def_const, symbol_table, escopo):
    analyze_semantics(constant, symbol_table, escopo)
    if def_const[1] is not None:
        analyze_semantics(def_const, symbol_table, escopo)

def analyze_def_tipos(tipo, def_tipos, symbol_table, escopo):
    analyze_semantics(tipo, symbol_table, escopo)
    if def_tipos[1] is not None:
        analyze_semantics(def_tipos, symbol_table, escopo)

def analyze_def_var(node, symbol_table, escopo):
    # Percorrer cada variável definida
    variable = node[1]
    def_var = node[2]
    analyze_semantics(variable, symbol_table, escopo)
    if def_var[1] is not None:
        analyze_semantics(def_var, symbol_table, escopo)

def analyze_def_func(function, def_func, symbol_table, escopo):
    analyze_semantics(function, symbol_table, escopo)
    if def_func[1] is not None:
        analyze_semantics(def_func, symbol_table, escopo)

def analyze_constante(constant_name, constant_value, symbol_table, escopo):
    key = constant_name + '/' + escopo    

    if key in symbol_table:
        print(f"Erro: Constante '{constant_name}' já foi definida.")
    else:
        symbol_table[key] = {'nome': constant_name, 'class': 'const', 'tipo': constant_value, 'escopo': escopo, 'qtd': '-', 'ordem_na_func': '-'}

def analyze_tipo(node, symbol_table, escopo):
    # Extrair informações relevantes do tipo e atualizar a tabela de símbolos
    type_name = node[2]
    type_value = node[4][1]   
    if type_value == 'array':
        type_value = 'array' + str(node[4][2][0]) + str(node[4][3]) +  str(node[4][4][0]) + str(node[4][6][1])
        
    # Verificar se o tipo já foi definido

    key = type_name + '/' + escopo
    if key in symbol_table:
        print(f"Erro: '{type_name}' já foi definido.")
    else:
        symbol_table[key] = {'nome': type_name, 'class': 'tipo', 'tipo': type_value, 'escopo': escopo, 'qtd': '-', 'ordem_na_func': '-'}
    extract_record_fields(node, symbol_table, str('campos'), type_name, str('-'))

def analyze_variavel(node, symbol_table, escopo):
    # Extrair informações relevantes da variável e atualizar a tabela de símbolos
    variable_name = node[2]
    variable_type = node[5][1]
    # Verificar se a variável já foi definida
    
    key = variable_name + '/' + escopo
    if key in symbol_table:
        print(f"Erro: Variável '{variable_name}' já foi definida no '{escopo}.")
    else:
        symbol_table[key] = {'nome': variable_name, 'class': 'variavel', 'tipo': variable_type, 'escopo': escopo, 'qtd': '-', 'ordem_na_func': '-'}
    extract_variable_fields(node, symbol_table, escopo, variable_type)

def count_parameters(node): #node campos
    if node[0] == 'CAMPOS':
        return 1 + count_parameters(node[4])
    elif node[0] == 'LISTA_CAMPOS':
        if node[1] is not None:
            return count_parameters(node[2]) + count_parameters(node[3])
        else:
            return 0
    else:
        return 0


def analyze_funcao(node, symbol_table, escopo):
    function_name = node[2][1]                      
    function_type = node[2][4][1]
    function_parameters = node[2][2]
    function_bloco_func = node[3]   
    # print(function_bloco_func) 
    # print(function_bloco_func[1]) 
    # Verifica se a função já foi definida    
    key = function_name + '/' + escopo
    key_result = 'result'+'/'+ function_name
    qtdparam = 0
    if function_parameters[1] is not None:
        campos = function_parameters[2]
        qtdparam = count_parameters(campos) #pega campos
        # print("nome func:", function_name)
        # print("qtde param = ", qtdparam)
    if key in symbol_table:
        print(f"Erro: Função '{function_name}' já foi definida.")
    else:
        symbol_table[key] = {'nome': function_name, 'class': 'funcao', 'tipo': function_type, 'escopo': escopo, 'qtd': qtdparam, 'ordem_na_func': '-'}
        symbol_table[key_result] = {'nome': 'result', 'class': 'variavel', 'tipo': function_type, 'escopo': function_name, 'qtd': '-', 'ordem_na_func': '-'}

    if function_parameters[1] is not None:
        # print('teste campo')
        # print(function_parameters[2])
        extract_fields_campos(function_parameters[2], symbol_table, 'parametro', function_name, 1)
    
    analyze_bloco_funcao(function_bloco_func,symbol_table,function_name)
 
symbol_table = {}

# Execute a análise semântica
analyze_semantics(result, symbol_table, escopo)



def print_symbol_table(symbol_table):
    print("\n\nTabela de Símbolos:")
    print("-------------------")
    for symbol, attributes in symbol_table.items():
        print(f"Key: {symbol}")
        for attribute, value in attributes.items():
            print(f"{attribute}: {value}")
        print("-------------------")




#print_symbol_table(symbol_table)

