from datetime import datetime
import numpy as np
import pandas as pd
def control(m): #Está função realiza a validação das informações que estão sendo inseridas no membro.
    condicao = True
    try:
        m[1] = int(m[1])
        m[2] = str(m[2].upper())
        m[0] = str(m[0].upper())
        #Validando o nome do membro
        if len(m[0]) =='' or len(m[0]) <= 2:
            print('O nome precisa ter mais de 2 letras!')
            condicao = False
        #Validando o sexo
        elif not(m[2] == 'M' or m[2] == 'F'):
            print('Digite somente M ou F para o sexo!')
            condicao =False
        #Validando a idade
        elif m [1] <= 0 or m[1] > 120:
            print('Idade inválida')
            condicao = False
        #Validando o cpf, verificando se o tamanho da string é igual a 11:    
        elif len(str(m[3])) != 11:
            print('O CPF precisa ter 11 digitos')
            condicao = False
        #Validando o telefone, verificando se o total de digitos é maior do que 10   
        elif len(str(m[4])) <= 10:
            print('Numero de telefone inválido')
            condicao = False
        #Validando o CEP   
        elif len(str(m[5])) not in [8,9]:
            print('CEP inválido!')
            print('Tamanho do CEP: {} tamanho que deveria ser: {}'.format(len(str(m[5])),len('00000000')))
            condicao = False
        else:
            m[3] = int(m[3])
            m[4] = int(m[4])
            m[5] = int(m[5])
    except ValueError:
        print('Você digitou um ou mais campos incorretamente!')
        condicao = False
    #Caso seja o retorno seja True, a operação é feita!   
    return condicao

#Esta função verifica se o argumento existe dentro do arquivo
def consultPos(atributo,arq):
    m = open(arq)#Abrindo o arquivo
    l = m.readline()#Pegando a primeira linha
    cont=0
    p=0
    if(arq == 'DO.txt' and type(atributo) in [str]):#Verificando o nome do arquivo 
        print('Oi')
        p = 1
    elif(type(atributo) in [int]):#Verificando se o tipo do argumento é um inteiro
        p = 3
    elif(type(atributo) in [str]):#Verificando se o tipo do argumento é uma String
        p = 0
    membro = []
    while l != '':
        pos = l.split(';')#Separando as linhas para verificar cada posição
        if str(atributo) != pos[p]:#Verificando se a coluna dentro do arquivo contem o atributo
            cont+=1#A variavel cont irá retornar a posição do membro dentro do arquivo
        else:
            membro = pos#Recebe a linha dentro do arquivo e Retorna para a função em que foi solicitada a busca
            break
        l = m.readline()
    m.close()
    return cont,membro

#Função principal para realizar as copias das listas
def salvarArquivo(arq):
    cLinhas = []
    dataAtual = datetime.now()#Recebendo a data atual do computador
    dataFormatada = str(str(dataAtual.day)+'/'+str(dataAtual.month)+'/'+str(dataAtual.year))#Formatando a data para o formato padrão
    novaListaC = [] 
    vL = open(arq).readlines()[:] #Pegando todas as linhas do arquivo e armazenando na variavel vL
    cont = 0 
    copiaArquivo = 'C'+arq #Variavel responsavel para dar o nome do arquivo que irá guardar as informações
    vLC = open(copiaArquivo,'a')#Criando o arquivo para guardar as informações.
    vLC.close()#Fechando o mesmo
    vLC = open(copiaArquivo,'r').readlines()[:]#Abrindo novamente o arquivo para leitura
    
    if(vLC == []):#Caso o arquivo esteja vazio irá inserir a lista atual
        for i in vL:
            novaListaC.append(dataFormatada+';'+i)
        
    elif(vLC != []):#Caso o arquivo não esteja vazio irá pegar  somente as linhas em que a data atual não se encontra
        for i in vLC:
            linhas = i
            i = i.split(';')
            if dataFormatada != i[0]:
                cont+=1
                novaListaC.append(linhas)
        
        for i in vL:#Pegando a posição em que a data atual se encontrava e inserindo as novas linhas 
            novaListaC.insert(cont,dataFormatada+';'+i)
    
    arquivo = open(copiaArquivo,'w')#Abrindo o arquivo para escrita
    for i in novaListaC:
        arquivo.write(i)#Inserindo a nova cópia dentro do arquivo
    arquivo.close()

#Função principal para restaurar a versão anterior do arquivo
def restaurarArquivo(arq):
    dataAtual = datetime.now()#Pegando a data atual
    copias = open(arq)#Abrindo o arquivo de copias para leitura
    linha = copias.readline()
    dicData = {}#Criando um dicionario para guardar a lista de datas
    dicDataEscolhida = {}
    listaDatas = []
    listaAInserir = []
    cont = 0
    while linha != '':#Percorrendo o arquivo 
        linha = linha.split(';')#Separando as linhas através do ";"
        listaDatas.append(linha[0])#Inserindo a coluna de datas na lista
        dicData[linha[0]] = linha[1:]#Inserindo   as datas na chave do dicionario e inserindo as linhas dos membros nos valores de cada chave
        linha = copias.readline()
    for i in dicData.keys():#Percorrendo as chaves do dicionario
        cont+=1#O contador mostrará as possiveis opções
        print('____________________________')
        print('"{}" para {}'.format(cont,i))
        print('____________________________')
        dicDataEscolhida[cont] = i#inserindo a variavel cont nas chaves do dicionario e as datas nos valores
    #Pede para que o usuario digite um número de 1 até a ultima posição da lista
    opData = input('\nDigite uma opção entre 1 e {} para restaurar de acordo com a data escolhida: '.format(cont))
    if int(opData) in dicDataEscolhida.keys():#Verificando se o valor digitado está contido nas chaves
        dataEscolhida = dicDataEscolhida[int(opData)]#Pegando a data escolhida através da chave
        copias.seek(0) #Posicionando o cursor para o incio do arquivo
        for i in copias:#Percorrendo o arquivo atual
            membrosASalvar = i #Armazenando as linhas do arquivo sem separar
            i = i.split(';') #Separando a linha através do ";"
            tamanhoData = len(i[0])+1#Armazenando o tamanho da data para que não seja inserida dentro do arquivo
            if (str(dataEscolhida) in i):#Verificando a data escolhida pelo usuario está presente na linha
                listaAInserir.append(membrosASalvar[tamanhoData:])#Inserindo a linha do arquivo na posição após o tamanho da data 

        arquivo = open(arq[1:],'w')#Abrindo o arquivo para escrita
        for i in listaAInserir:
            arquivo.write(i)#inserindo as informações dentro do arquivo
        arquivo.close()    
            
    else:#Caso a opção digitada pelo usuario não esteja dentro das chaves do dicionario, ignora as operações acima. 
        print('Opção Invalida')        
    copias.close()
#Função principal para pegar as linhas do arquivo sem separalas      
def pegarLista(arq):
    linhas = []
    f = open(arq)
    for i in f:
        linhas.append(i)
    f.close()
    return linhas
             
#Função principal para inseirir os membros na lista de Membros
def inserirMembro():    
    arquivo = open('Membro.txt','a')#Abrindo o arquivo para leitura, caso não exista, irá criar um novo.
    s='s'
    op ='s'
    membro = [0]*6#Criando a lista a ser preenchida com 6 posições
    while(s == 's'):
        #Interagindo com o usuário para inserir as informações do membro
        membro[0] = input('Digite o nome do membro:').strip()
        membro[1] = input('Digite a idade do membro:').strip()
        membro[2] = input('Digite o sexo do membro("M" para masculino e "F" para Feminino):').strip()
        membro[3] = input('Digite o CPF, obs(somente números):').strip()
        membro[4] = input('Digite o telefone para contato do membro, obs(somente números):').strip()
        membro[5] = input('Digite o CEP do membro, obs(somente números):').strip()
        condicao = control(membro)#Validando as informações que foram digitadas pelo usuario
        if condicao == False:#Caso o usuario digite algum campo incorretamente, pergunta se deseja repitir o processo 
            op = input('Deseja tentar novamente ? (s/n)')
            if(op == 's' or op == 'sim'):
                s = 's'
            else:
                break
        else:
            argumentos = consultPos(membro[3],arq='Membro.txt')#Verificando se o CPF do membro se encontra no arquivo
            if(argumentos[1] != []):#A tupla na posição 1 armazena a linha do arquivo em que o cpf foi encontrado, caso esteja preenchida não irá inserir o membro novamente
                print('Membro já cadastrado!')
            else:#Caso o membro ainda não esteja na lista, irá inserir no mesmo formato das outras linhas
                arquivo.write(str(membro[0])+';'+str(membro[1])+';'+str(membro[2])+';'+str(membro[3])+';'+str(membro[4])+';'+str(membro[5])+'\n')
            s = input(str('Deseja continuar inserindo? (s/n)'))#Pergunta se deseja inseirir outra pessoa no arquivo
        if(s == 'n'):
            break
    arquivo.close()
    print()
   
#Função principal para a atualização das informações do membro
def atualizarMembro(m,n,posM):
    while(True):
        menuAtualizarMembro(m)#Chamando a função que contém o menu com as opções que disponíveis para atualizar os atributos do membro
        try:#Interagindo com o usuario para inseirir as novas informações do membro
            pos = input('\nEscolha qual campo deseja alterar ou digite zero para sair:')
            if(pos == '1'):
                m[0] = input(str('Digite o novo nome do Membro: ')).strip()
            elif(pos == '2'):
                m[1] = input(str('Digite a nova idade do Membro: ')).strip()
            elif(pos == '3'):
                m[2] = input(str('Digite o sexo do Membro: ')).strip()
            elif(pos == '4'):
                m[3] = input(str('Digite o novo CPF do Membro: ')).strip()
            elif(pos == '5'):
                m[4] = input(str('Digite o novo Telefone do Membro: ')).strip()
            elif(pos == '6'):
                m[5] = input(str('Digite o novo CEP do Membro: ')).strip()
            elif(pos == '7'):
                condicao = control(m)#Validando as informações inseridas pelo usuário
                linhas = ''#Variável que irá armazenar as informações do arquivo
                if(condicao == True):#Caso esteja
                    novoMembro = str(m[0])+';'+str(m[1])+';'+str(m[2])+';'+str(m[3])+';'+str(m[4])+';'+str(m[5])
                    linhas = pegarLista(arq='Membro.txt')
                    lString=[]
                    for i in range(len(linhas)):#Percorrendo as linhas do arquivo 
                        if(posM == i):#Caso a posição da linha seja igual a posição do membro no arquivo lido anteriormente, irá inserir a linha na mesma posição
                            linhas.pop(i)
                            linhas.insert(i,novoMembro+'\n')        
                    arqNovo = open('Membro.txt','w')
                    for j in linhas: #Percorrendo a lista com as informações do membro atualizadas
                        arqNovo.write(str(j))#Inserindo os membros dentro do arquivo
                    print('Atualização concluida!')
                    arqNovo.close()
                else:#Pergunta ao usuário se deseja realizar as operações novamente
                    op = input('Deseja tentar atualizar anovamente ? (s/n)')
                    if(op == 's' or op == 'sim'):
                        s = 's'
                    else:
                        break
            elif(pos == '0'):#Caso o usuario digite 0 irá retornar ao menu principal
                break
            else:
                print('Digite uma opção válida!')
        except KeyboardInterrupt:
            print('O programa foi interrompido pelo usuário!')
            break
        except:
            print('Erro inesperado!')

    
#Função principal para excluir o membro dentro do arquivo
def apagar(atributo,arq):
    nlm = []
    arquivo = open(arq,'r')#Abrindo arquivo para leitura    
    linhas = arquivo.readline()#Pegando a linha do arquivo
    while linhas != '':#Percorrendo a lista
        if str(atributo) not in linhas.split(';'):#Verifica se o atributo não se encontra na linha
            nlm.append(linhas)#Pegando todas as linhas em que o atributo não se encontra.
        linhas = arquivo.readline()
    arquivo.close()
    arquivoCMD = open(arq,'w')#Abrindo arquivo para leitura 
    for i in nlm:#Percorrendo o arquivo
        arquivoCMD.write(str(i))#Inserindo as linhas detro do arquivo
    arquivoCMD.close()    
    print('O membro foi excluído com sucesso!')

#Função principal para inseiri dizimos e ofertas
def inserirDO(nome,arq,tipo):#Os argumentos estão sendo passados pela função escolherOPDF   
    arquivo = open(arq,'a')
    s='s'
    op ='s'
    dataAtual = datetime.now()#Pegando a data atual
    dataFormatada = str(str(dataAtual.day)+'/'+str(dataAtual.month)+'/'+str(dataAtual.year))#Formatando a data
    vetorDO = [0]*5#Criando a lista com as posições que serão preenchidas pelo usuário
    while(s == 's'):
        vetorDO[0] = tipo
        vetorDO[1] = nome.upper()
        vetorDO[2] = input('Digite o valor: ').strip()
        vetorDO[2] = float(vetorDO[2])
        vetorDO[3] = dataFormatada
        vetorDO[4] = str(input('Digite a descrição:')).strip()
        if(vetorDO[2] <= 0 ):
            print('O valor precisa ser maior do que zero!')
            break
        elif vetorDO[4] == '':
            vetorDO[4] = 'Sem descrição'               
        arquivo.write(str(vetorDO[0])+';'+str(vetorDO[1])+';'+str(vetorDO[2])+';'+str(vetorDO[3])+';'+str(vetorDO[4])+'\n')
        break
    arquivo.close()
    print()

#Mostrando as alterações feitas e o menu para o usuário
def menuAtualizarMembro(posM):
    print('Modificações atuais:')
    print('Nome: {0}, Idade: {1}, Sexo: {2},'\
           'CPF: {3}, Tel: {4}, CEP: {5}'.\
    format(posM[0].upper(),posM[1],posM[2].upper(),\
           posM[3],posM[4],posM[5]))

    print(' _____________________\n'\
         '|` _____________________`\n'\
         '| |1 - Nome             |\n'\
         '| |2 - Idade            |\n'\
         '| |3 - Sexo: (M/F)      |\n'\
         '| |4 - CPF              |\n'\
         '| |5 - Telefone         |\n'\
         '| |6 - CEP              |\n'\
         '| |7 - Salvar Alterações|\n'\
         '| |0 - Cancelar         |\n'\
         ' `|_____________________|')
#Menu dos Dizimos e Ofertas da função escolherOPDF
def menuDizimosEOfertas():
    print(' _____________________________\n'\
          '|` ____________________________`\n'\
          '| |1 - Dizimar                 |\n'\
          '| |2 - Ofertar                 |\n'\
          '| |3 - Apagar Contribuição     |\n'\
          '| |4 - Salvar                  |\n'\
          '| |5 - Restaurar arquivo       |\n'\
          '| |6 - Análise detalhada       |\n'\
          '| |0 - Voltar ao menu anterior |\n'\
          ' `|____________________________|')
#Menu para fazer a análise dos Dizimos e Ofertas
def menuAnalise():
    print(' ___________________________________\n'\
          '|` __________________________________`\n'\
          '| |1 - Arrecadação Máxima por dia    |\n'\
          '| |2 - Renda Total                   |\n'\
          '| |3 - Numero de contribuições       |\n'\
          '| |4 - Membros que não contribuiram  |\n'\
          '| |5 - Visualizar Dados              |\n'\
          '| |0 - Voltar ao menu anterior       |\n'\
          ' `|_________________________________ |')
#Menu principal do programa       
def menuPrincipal():
    print(' ____________________________________\n'\
         '|` ___________________________________`\n'\
         '| |1 - Cadastrar membro               |\n'\
         '| |2 - Atualizar informações do membro|\n'\
         '| |3 - Apagar membro                  |\n'\
         '| |4 - Listar membros                 |\n'\
         '| |5 - Inserir Dizimo/Oferta          |\n'\
         '| |6 - Salvar o arquivo atual         |\n'\
         '| |7 - Restaurar arquivo              |\n'\
         '| |0 - Encerrar o programa            |\n'\
         ' `|___________________________________|')
#Função principal para fazer a análise dos dizimos e ofertas    
def analiseDetalhada():
    while(True):
        menuAnalise()
        try:
            op = input('Digite uma opção:')#Interagindo com o usuário para escolher uma opção
            if op == '1':#Criando um vetor para armazenar as informações do arquivo de Dizimos e Ofertas
                dados = np.loadtxt('DO.txt',delimiter =';',\
                    dtype= {'names': ('especie','nomes','valor','data','descricao'),\
                    'formats': ('U1','U25','f','U10','U25')})
                cont = 0
                listaDatas = []
                listaOpc = []
                listaDatasDisponiveis = set(dados['data'])#Utilizando a função set para remover as datas que se repetem no arquivo
                for i in listaDatasDisponiveis:#Percorrendo a lista de datas Disponíveis
                    listaDatas.append(i)#Armazenando as datas da lista
                    cont +=1
                    listaOpc.append(cont)
                    print('_'*25)
                    print('Digite {} para escolher a data {}'.format(cont,i))
                    print('_'*25)
                opc = input('Digite um numero para escolher a data: ').strip()#Interagindo com o usuário para escolher uma opção das datas disponíveis
                if int(opc) in listaOpc:#Verifica se a opção está dentro da lista de opções
                    datas = listaDatas[int(opc)-1]#Subtraindo 1 para pegar a data exata na lista de datas
                    p = pd.DataFrame(dados)#Criando DataFrame com as informações do vetor
                    dFilter = p[dados['data'] == str(datas)]#Pegando somente as linhas do DataFrame em que a data se encontra
                    print('A contribuição máximo nessa data foi de:',np.sum(dFilter['valor']))#Exibindo o valor máximo de contribuições na data escolhida
                else:
                    raise ValueError
                
            elif op == '2':#Criando um vetor para armazenar as informações do arquivo de Dizimos e Ofertas
                dados = np.loadtxt('DO.txt',delimiter =';',\
                    dtype= {'names': ('especie','nomes','valor','data','descricao'),\
                    'formats': ('U1','U25','f','U10','U25')})
                print(np.sum(dados['valor']))#Exibindo o somatório total das contribuições

            elif op == '3':#Criando um vetor para armazenar as informações do arquivo de Dizimos e Ofertas
                dados = np.loadtxt('DO.txt',delimiter =';',\
                    dtype= {'names': ('especie','nomes','valor','data','descricao'),\
                    'formats': ('U1','U25','f','U10','U25')})
                #Criando um vetor para armazenar as informações do arquivo dos Membros
                dados1 = np.loadtxt('Membro.txt',delimiter =';',\
                    dtype= {'names': ('nomes','idade','sexo','cpf','telefone','cep'),\
                        'formats': ('U25','i4','U1','U11','U10','U7')})
                contTotal = 0
                listaNomes = dados['nomes']#Pegando a coluna de nomes no arquivo de Dizimos e ofertas
                nomes = set(dados1['nomes'])#Pegando a coluna de nomes no arquivo dos Membros
                for p in nomes:#Percorrendo os nomes dentro da lista
                    nome = p#Guardando os nomes na variavel
                    p = p.split(' ')#Separando os nomes através dos espaços 
                    cont = 0
                    for w in listaNomes:#Percorrendo a lista de nomes do arquivo de dizimos e ofertas
                        if w.startswith(p[0]):#Verificando se o primeiro nome do membro está presente nos nomes de cada membro
                            cont+=1#somando 1 cada vez que o nome é encontrado
                    contTotal += cont#Armazena o número total de contribuições de cada membro
                    if(cont==0):#Caso o membro nunca tenha contribuido, seu nome será exibido
                        print('O membro {} não contribuiu'.format(p,cont))
                    else:#Exibindo a quantidade de pessoas que contribuiram e o total das contribuições
                        print (p[0] + ' contribuiu ' + str(cont) + ' vez(es)')
                print ('O numero total das contribuições é de: ' + str(contTotal))
                

            elif op == '4':#Criando um vetor para armazenar as informações do arquivo de Dizimos e Ofertas
                dados = np.loadtxt('DO.txt',delimiter =';',\
            dtype= {'names': ('especie','nomes','valor','data','descricao'),\
                    'formats': ('U1','U25','f','U10','U25')})
                listaDeNomes = []
                contribuidores = dados['nomes']#Pegando a coluna de nomes do arquivo de Dizimos e Ofertas
                arq = open('Membro.txt') 
                for i in arq:
                    i = i.split(';')
                    listaDeNomes.append(i[0])
                arq.close()#Subtraindo as informações 
                #Verifica a quantidade de membros que ainda não dizimaram
                naoContribuidores = len(set(contribuidores)) - len(set(listaDeNomes))
                print('O número de pessoas que não contribuiram é:',abs(naoContribuidores))

            elif op == '5':#Criando vetor com as informações dos dizimos e ofertas
                dados = np.loadtxt('DO.txt',delimiter =';',\
            dtype= {'names': ('especie','nomes','valor','data','descricao'),\
                    'formats': ('U1','U25','f','U10','U25')})
                p = pd.DataFrame(dados)#Criando DataFrame com as informações dos dizimos e ofertas
                print(p)

            elif op == '0':
                break
        except ValueError:
            print('Opção inválida!')
        except FileNotFoundError:
            print('Arquivo de Dizimos e Ofertas está vazio ou ainda não foi gerado')
        except KeyboardInterrupt:
            print('O programa foi interrompido pelo usuário!')
        except:
            print('Erro inesperado')

#Função principal dos Dizimos e Ofertas
def escolherOPDF():
    while(True):
        menuDizimosEOfertas()
        try:#Interagindo com o usuario para escolher uma opção
            op = input('\nEscolha uma opção:')
            if(op == '1'):
                #Pergunta o nome do membro e retira os espaços
                nome = input('Digite o nome do membro que irá dizimar: ').strip()
                condicao = consultPos(nome.upper(),arq='Membro.txt')#Verifica se o membro está dentro da lista
                if(condicao[1] != []):#Caso a lista não esteja vazia irá levar as informações que foram encontradas e a categoria em que o valor pertence
                    inserirDO(nome,arq='DO.txt',tipo='D')
                else:
                    print('\nNão foi possível localizar o membro.\nVerifique se ele já está cadastrado através da opção 4!.')
                    break
                
            elif(op == '2'):
                nome = input('Digite o nome do membro que irá ofertar: ').strip()
                condicao = consultPos(nome.upper(), arq='Membro.txt')
                if(condicao[1] != []):#Caso a lista não esteja vazia irá levar as informações que foram encontradas e a categoria em que o valor pertence
                    inserirDO(nome,arq='DO.txt',tipo='O')
                else:
                    print('\nO membro não foi localizado.\nVerifique se o membro está inserido na lista de membros.')
                    break
                
            elif(op == '3'):#Irá excluir o membro da lista através do nome digitado pelo usuário
                nome = input('Digite o nome da membro que realizou o dizimo:')
                nome = nome.upper()
                nome = nome.strip()
                nome = str(nome)
                linhas = consultPos(nome,arq='DO.txt')
                if(linhas[1] != []):#Caso o arquivo não esteja vazio irá excluir o membro da lista 
                    apagar(nome,arq='DO.txt')
                else:
                    print('\nO membro não foi localizado.\nVerifique se o membro está inserido na lista de membros.')
                    
            elif(op == '4'): #Salva o arquivo
                salvarArquivo(arq='DO.txt')
                print('Arquivo salvo!')
                
            elif(op == '5'):#Restaura a versão anterior do arquivo
                restaurarArquivo(arq='CDO.txt')
                
            elif(op == '6'):#Realiza a análise detalhada dos dizimos e ofertas
                argumentos = pegarLista(arq='DO.txt')
                if(len(argumentos) >= 2):
                    analiseDetalhada()
                else:#O valor foi considerado pois não era possível realizar a comparação com apenas um membro contribuidor
                    print('É necessário 2 contribuições para realizar esta função.')    
            elif(op == '0'):
                break
            else:
                raise ValueError
        except ValueError:
            print('Opção invalida!')
        except KeyboardInterrupt:
            print('O programa foi interrompido pelo usuário!')
        except FileNotFoundError:
            print('\nA lista  ainda não foi gerada!')
        except:
            print('Erro inesperado!')

            
def main():
    while(True):
        menuPrincipal()
        try:
            op = input('\nEscolha uma opção:').strip()
            if(op == '1'):
                #Realiza a inserção do membro no arquivo atual
                inserirMembro() 
                
            elif(op == '2'):
                nome = input(str('Digite o nome completo do membro que deseja atualizar os dados: ')).strip()
                argumentos = consultPos(nome.upper(),arq='Membro.txt')
                if(argumentos[1] != []):#Verificando a existencia do membro no arquivo,caso exista irá chamar a função para atualizar o membro                              
                    atualizarMembro(argumentos[1],nome,argumentos[0])
                else:
                    print('Membro não localizado')
                           
            elif(op == '3'):
                opc = input('Deseja excluir pelo nome ou pelo cpf?\nDigite "1" para nome e "2" para cpf:').strip()

                if(opc == ''):#Caso o usuário não digite nada, chama a exceção ValueError
                	raise ValueError
                elif(opc == '1'):
                    atributoDoMembro = input(str('Digite o nome completo do membro que deseja apagar: ')).strip()
                    atributoDoMembro = atributoDoMembro.upper()
                    argumentos = consultPos(atributoDoMembro,arq='Membro.txt')
                    if(argumentos[1] != []):#Verificando a existencia do membro no arquivo,caso exista irá chamar a função para apagar o membro 
                        apagar(atributoDoMembro,arq='Membro.txt')
                    else:
                        print('Membro não localizado.')
                elif(opc == '2'):
                    atributoDoMembro = input(str('Digite o CPF do membro, obs: somente números!')).strip()
                    atributoDoMembro = atributoDoMembro.strip()
                    atributoDoMembro = int(atributoDoMembro)
                    argumentos = consultPos(atributoDoMembro,arq='Membro.txt')
                    if(argumentos[1] != []):#Verificando a existencia do membro no arquivo,caso exista irá chamar a função para apagar o membro 
                        apagar(atributoDoMembro,arq='Membro.txt')
                    else:
                        print('Membro não localizado.')
                
                    
            elif(op == '4'):
                #Pega as linhas do arquivo
                linhas = pegarLista(arq='Membro.txt')
                #Caso retorne a lista vazia, irá exibir a mensagem para o usuário
                if(linhas == []):
                    print('Arquivo vazio!')
                else:#Lista os membros no arquivo
                    for i in linhas:
                        i = i.split(';')
                        print('______'*7)
                        print('Nome: {}; Idade: {}; Sexo: {}'.format(i[0],i[1],i[2]))
                        print('______'*7)
            elif(op == '5'):
                escolherOPDF()
                
            elif(op == '6'):#Salva as informações do membro
                salvarArquivo(arq='Membro.txt')
                print('O arquivo foi salvo!')
                
            elif(op == '7'):#Restaura uma versão anterior da lista
                restaurarArquivo(arq='CMembro.txt')   
            elif(op == '0'):#Encerra o programa
                print('Programa encerrado!')
                break
            else:
                raise ValueError
            
        except ValueError:
               print('Opção invalida!')
        except KeyboardInterrupt:
            print('O programa foi interrompido pelo usuário!')
            break
        except FileNotFoundError:
            print('\nA lista  ainda não foi gerada!')
        except ModuleNotFoundError:
        	print('Será necessario instalat os modulos numpy, pandas e datetime para executar o codigo.')
        except:
            print('Erro inesperado!')
  
if __name__ == '__main__':
    main()

