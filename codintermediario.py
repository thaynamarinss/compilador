import sintatico
import semantico
#importando a arvore sintatica do comp.py
arvore = sintatico.result
#print(arvore)  # Acesso à variável result do comp.py

print("\n"+"_"*50 +"Gerador de código intermediario"+"_"*50)
#contadores para controlar os nomes por exemplo temp(contador)
temp_counter = 0
label_counter = 0
intermediate_code = []

def generate_intermediate_code(node):
    global temp_counter
    global label_counter
    if isinstance(node, tuple):       

        if node[0] == 'PROGRAMA':
            generate_intermediate_code(node[1])  # Processa as DECLARACOES
            generate_intermediate_code(node[2])  # Processa o PRINCIPAL

        elif node[0] == 'PRINCIPAL':            
            generate_intermediate_code(node[2])  # Processa o COMANDO
            generate_intermediate_code(node[3])  # Processa a LISTA_COM
        
        elif node[0] == 'COMANDO':

            if node[1] == 'while':                
                labelWhile = f"label{label_counter}"
                label_counter += 1
                labelEndWhile = f"label{label_counter}"
                label_counter += 1
                exp_logica = node[2]
                bloco = node[3]
                #label inicio while
                intermediate_code.append(f"LBL {labelWhile} - -")
                tempR = generate_intermediate_code(exp_logica)               
                
                #SALTA SE O TEMP FOR 0 (FALSE)
                intermediate_code.append(f"JEZ {labelEndWhile} {tempR}")
        
                generate_intermediate_code(bloco)
                intermediate_code.append(f"JMP {labelWhile} - -")
                intermediate_code.append(f"LBL {labelEndWhile} - -")
            
            elif node[1]  == 'if':
                labelIFFalse = f"label{label_counter}"
                label_counter += 1
                tempR = generate_intermediate_code(node[2]) #exp_logica
                #SALTA SE O TEMP FOR 0 (FALSE)
                intermediate_code.append(f"JEZ {labelIFFalse} {tempR}")
                labelendIF =f"label{label_counter}"
                label_counter += 1
                
                generate_intermediate_code(node[4]) #bloco
                intermediate_code.append(f"JMP {labelendIF} - -")#pular para o final do if
                intermediate_code.append(f"LBL {labelIFFalse} - -") #label do else
                generate_intermediate_code(node[5]) #else

                intermediate_code.append(f"LBL {labelendIF}") #label final if

           
            elif node[1] == 'write':
                temp = generate_intermediate_code(node[2]) #const_valor
                intermediate_code.append(f"WRITE {temp} -")

            elif node[1] == 'read':
                id = node[2]
                nome = node[3]                
                generate_intermediate_code(nome)             
                if nome[1] is not None:
                    if nome[1] == '.':
                        pontoP = nome[2]
                        intermediate_code.append(f"READ {id}.{pontoP}")
                else:
                    intermediate_code.append(f"READ {id}")


            elif len(node) == 5 and node[3] == ':=':
                id = node[1]
                exp_mat = node[4]
                temp = generate_intermediate_code(exp_mat)
                intermediate_code.append(f"ATR {id} {temp}")
               
        elif node[0] == 'EXP_LOGICA':            

            if len(node) == 4:     
                tempA = generate_intermediate_code(node[1]) #exp_mat   
                tempB = generate_intermediate_code(node[3])#exp_logica #problema passa a lista ao inves de temp
                op = node[2]
                temp = f"temp{temp_counter}"
                temp_counter += 1

                if op[1] == '>':  
                    #GRT (GREATER) armazena 1 se for maior 
                    intermediate_code.append(f"GRT {temp} {tempA} {tempB} ") #pode usar o les e inverter para verificar de B > A
                    
                elif op[1] == '<':
                    #less armazena 1 se for menor e 0 se for maior              
                    intermediate_code.append(f"LESS {temp} {tempA} {tempB} ") 
                
                elif op[1] == '=':
                    #EQL armazena 1 se forem iguais e 0 se não
                    intermediate_code.append(f"EQL {temp} {tempA} {tempB}")
                
                elif op[1] == '!':
                    #dif armazena 1 se forem diferentes
                    intermediate_code.append(f"DIF {temp} {tempA} {tempB}")
                
                return temp # retorna temp com result 0 para falso ou 1 para verdadeiro

            else:
                temp = generate_intermediate_code(node[1])#exp_mat
                return temp
            


        elif node[0] == 'EXP_MAT_AUX':        
            temp = ''
            if len(node) == 4:
                tempA = generate_intermediate_code(node[1]) #parametro
                tempB = generate_intermediate_code(node[3])  #expmat     
                op = node[2]

                if op[1] == '+':
                    temp = f"temp{temp_counter}"
                    temp_counter += 1
                    intermediate_code.append(f"ADD {temp} {tempA} {tempB}")
                    
                
                elif op[1] == '-':                                                                       
                    temp = f"temp{temp_counter}"
                    temp_counter += 1
                    intermediate_code.append(f"SUB {temp} {tempA} {tempB}")        

                elif op[1] == '*':
                    temp = f"temp{temp_counter}"
                    temp_counter += 1
                    intermediate_code.append(f"mul {temp} {tempA} {tempB}")
            
                else:# aqui no caso de ser / divisao
                    temp = f"temp{temp_counter}"
                    temp_counter += 1
                    intermediate_code.append(f"DIV {temp} {tempA} {tempB}")
    
            else:
                temp = generate_intermediate_code(node[1]) # caso seja so o parametro
        
            return temp               

            
        elif node[0] == 'PARAMETRO':
            param = node[1]
            if isinstance(param, int) or isinstance(param, float):
                return param
            else:                                  
                temp = f"temp{temp_counter}"
                temp_counter += 1
                if node[2][1] == '(':                                   
                    generate_intermediate_code(node[2]) #nome
                    intermediate_code.append(f"CALL {param} - -")
                    intermediate_code.append(f"ATR {temp} {param} -") 
                else:
                    intermediate_code.append(f"ATR {temp} {param} -")                
                    generate_intermediate_code(node[2]) #nome
                return temp

        elif node[0] == 'BLOCO':
            if len(node) == 2:
                generate_intermediate_code(node[1]) #comando
            else:
                generate_intermediate_code(node[2]) #comando
                generate_intermediate_code(node[3]) #lista_com

        elif node[0] == 'LISTA_COM':
            if node[1] is not None:
                generate_intermediate_code(node[2]) #comando
                generate_intermediate_code(node[3]) #lista_com
        
        elif node[0] == "SIN_ELSE":
           
           if node[1] is not None:                
                generate_intermediate_code(node[2]) #BLOCO
        
        elif node[0] == 'CONST_VALOR':
           
            if node[1][0] == 'EXP_MAT_AUX':                
                temp = generate_intermediate_code(node[1]) #EXP_MAT_AUX                 
            else:
                temp = f'"{node[1]}"' 
            return temp
            
        elif node[0] == 'DECLARACOES':
            def_const = node[1]
            def_func = node[4]
            generate_intermediate_code(def_const)
            generate_intermediate_code(def_func)
        #DEF_CONST ESTA COMENTADO POIS SERIA TRATADO NO CODIGO FINAL (indicando o espaço que deve ser reservado)
        # elif node[0] == 'DEF_CONST':
        #     if node[1] is not None:
        #         generate_intermediate_code(node[1]) #CONSTANTE
        #         generate_intermediate_code(node[2]) #DEF_CONST
        elif node[0] == 'CONSTANTE':
            id = node[2]
            temp = generate_intermediate_code(node[4]) # CONST_VALOR
            print(f'temp const é igual a {temp}')
            intermediate_code.append(f"ATR {id} {temp} -")

        elif node[0] == 'DEF_FUNC':
            if node[1] is not None:
                generate_intermediate_code(node[1]) #FUNCAO
                generate_intermediate_code(node[2]) #def_func

        elif node[0] == 'FUNCAO':
            generate_intermediate_code(node[2]) #nome_funcao
            generate_intermediate_code(node[3]) #bloco_func
            intermediate_code.append(f"RET result - -")
        
        elif node[0] == 'NOME_FUNCAO':
            nomeFunc = node[1]
            intermediate_code.append(f'LBL {nomeFunc} - -')
            generate_intermediate_code(node[2]) #param_func
        
        elif node[0] == 'PARAM_FUNC':
            if node[1] is not None:
                generate_intermediate_code(node[2]) #campos
       
        elif node[0] == 'CAMPOS':
            id_param = node[1]
            intermediate_code.append(f"POP {id_param} - -")
            generate_intermediate_code(node[4]) #lista_campos 
        
        elif node[0] == 'LISTA_CAMPOS':
            if node[1] is not None:
                generate_intermediate_code(node[2]) #campos
                generate_intermediate_code(node[3]) #lista_campos

        elif node[0] == 'BLOCO_FUNCAO':
            generate_intermediate_code(node[3]) #comando
            generate_intermediate_code(node[4]) #lista_com

        elif node[0] == 'LISTA_PARAM':
            if node[1] is not None:
                tp = generate_intermediate_code(node[1]) #parametro
                intermediate_code.append(f"PUSH {tp} - -")
                if len(node) == 4:                    
                    generate_intermediate_code(node[3]) #LISTA_PARAM
        
        elif node[0] == 'NOME':
            if node[1] is not None:
                if node[1][0] == '.':
                    generate_intermediate_code(node[3]) #nome
                elif node[1][0] == '(':#chamada de função ()
                    generate_intermediate_code(node[2]) #lista_param
                else: 
                    generate_intermediate_code(node[2]) #param     

    return intermediate_code

# Chama a função para gerar o código intermediário
intermediate_code = generate_intermediate_code(arvore)

# Imprime o código intermediário gerado
for line in intermediate_code:
    print(line)

