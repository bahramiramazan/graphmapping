
import random
import yaml
from os.path import join
import csv
import ast
import random
import argparse
#####
import copy
import datetime
import time
import numpy as np
import random
#############
import os
from openai import OpenAI

# Load environment variables from .env
from dotenv import load_dotenv
from env_utils import doublecheck_env




# Load environment variables from .env
load_dotenv()

# Check and print results
doublecheck_env("example.env")


######################################## 
######################################## 
def get_args():
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-t", "--task", help=" print_train,print_test")
    argParser.add_argument("-s", "--solution", help=" solutino")
    argParser.add_argument("-e", "--existing",default=None,type=str, help=" existing question")
    argParser.add_argument("-c", "--cross",default='True',type=str, help=" cross")
    argParser.add_argument("-v", "--version",default='origninal',type=str, help=" origninal")

    args = argParser.parse_args()
    print("args=%s" % args)

    return args



def shuflle_row(l1,l2):
    c = list(zip(l1, l2))
    random.shuffle(c)

    l1, l2 = zip(*c)
    return  l1, l2 


def shuflle_many_columns(L,nodes):
    
    L.append(nodes)
    c = list(zip(*L))
    random.shuffle(c)
    #zip(*[[1,2], [3,4], [5,6]])
    L_=[l for l in  zip(*c)]
    
    return L_[:-1],L_[-1]


def shuflle_many_columns_(L):
    

    c = list(zip(*L))
    random.shuffle(c)
    #zip(*[[1,2], [3,4], [5,6]])
    L_=[l for l in  zip(*c)]
    
    return L_[:]

###
def shuflle_two(l1,l2):
    c = list(zip(l1, l2))
    random.shuffle(c)

    l1, l2 = zip(*c)
    return  l1, l2
###

def crossing_columns(L,N):
    index=[k for k in range(len(L))]
    random.shuffle(index)
    
    N_new=[N[i] for i in index] 
    L_New=[]
    for l in L:
        l_=[l[i] for i in index]
        L_New.append(l_)
    return L_New, N_new
# def crossing_rows_and_v2(L,N):
#     index=[k for k in range(len(L))]
#     random.shuffle(index)
    
#     N_new=[N[i] for i in index] 
#     L_New=[]

#     L_New_=[]
#     for i in index:
#         l=L[i]
#         l_=[l[i] for i in index]
#         L_New_.append(l_)
        
#     return L_New_, N_new


def crossing_rows_and_v2(L,N,cross='no'):
    index_row=[k for k in range(len(L))]
    random.shuffle(index_row)
    
    index_col=[k for k in range(len(L))]
    random.shuffle(index_col)
    
    row_order=[copy.deepcopy(N[i])  for i in index_row] 
    column_order=[copy.deepcopy(N[i]) for i in index_col]
    if cross=='False':
        column_order=row_order
        index_col=index_row
        #print('cross',cross)
        #exit()

    adj_dic={}
    for i,l in  enumerate(L):
        a=N[i]
        for j,li in enumerate(l):
            b=N[j]
            adj_dic[(a,b)]=li
            
    L_New=[]
    #print('adj_dic',adj_dic)
    adj_dic_new={}
    for a in row_order:
        l=[]
        for b in column_order:
            v=adj_dic[(a,b)]
            l.append(v)
        L_New.append(l)
    ####################
    for i,l in  enumerate(L_New):
        a=row_order[i]
        for j,li in enumerate(l):
            b=column_order[j]
            adj_dic_new[(a,b)]=li
            
    for k in adj_dic_new.keys():
        old=adj_dic[k]
        new=adj_dic_new[k]
        if old!=new:
            print('wrong')
            exit()

    # print('row_order',row_order)
    # print('column_order',column_order)
    # print('cross',cross)
    # exit()
        
    return L_New,row_order,column_order
            
            
    
            
    
            
            

def load_config(file_name="config.yaml", concatenate=False):
    try:
        with open(file_name) as yaml_file:
            doc = yaml.safe_load(yaml_file)
        if concatenate:
            doc = {**doc[1], **doc[2], **doc[3], **doc[4]}
        return doc
    except:
        raise Exception("Can't load config file")




#####

#def find_mask(masked,ordered):
def find_mask(variables,masked,variable_values_list):
    
    masked_ids={}
    masked_=masked.copy()
    for v in variables:
        for mi,m in enumerate(masked):
            if v==m:
                masked_ids[v]=variable_values_list[mi]

    
    return masked_ids

def load_trials(file_name, randomize_graphs=False):
    file_path =file_name# join("trials", file_name)
    #print('file_name',file_name)
    #print('file_path',file_path)

    with open(file_path) as f:
        reader = csv.reader(f, delimiter=';')
        #print('reader')
        header = None
        data_train = []
        data_exp = []
        for row in reader:
            if not header:
                header = row
            else:
                #print('header',header)
                #print(row)
                data_row = {k: v for k, v in zip(header, row)}
                for k in ["NR", "FEED", "TRAIN", "Number_of_nodes", "Number_of_edges","Bidirectional"]:
                    data_row[k] = int(data_row[k])
                for k in ["Nodes_A", "Nodes_B"]:
                    data_row[k] = [int(elem) for elem in data_row[k].split(",")]
                for k in ["Edges_A", "Edges_B", "Left_button_targets", "Right_button_targets"]:
                    data_row[k] = ast.literal_eval(data_row[k])

                if randomize_graphs and random.choice([True, False]):
                    data_row["Nodes_A"], data_row["Nodes_B"] = data_row["Nodes_B"], data_row["Nodes_A"]
                    data_row["Edges_A"], data_row["Edges_B"] = data_row["Edges_B"], data_row["Edges_A"]
                    data_row["Left_button_targets"], data_row["Right_button_targets"] = data_row["Right_button_targets"], data_row["Left_button_targets"]


                if data_row["TRAIN"] == 1:
                    data_train.append(data_row)
                else:
                    data_exp.append(data_row)


    # block_nr = set([info["Block"] for info in data_exp])
    # data_exp = [[info for info in data_exp if info["Block"] == i] for i in block_nr]
    return data_train, data_exp


#####




def mask_nodes(d):

    source=d['source']
    target=d['target']
    Type_=d['Type_']
    Crossed_edges=d['Crossed_edges']
    #print('Crossed_edges',Crossed_edges)
    if len(str(Crossed_edges))==0 or Crossed_edges==False:
        Crossed_edges='no'
    source_adj=source['adj']
    ##
    source_nodes_row=source['nodes_in_row']
    source_nodes_column=source['nodes_in_column']
    target_adj=target['adj']



    target_nodes_row=target['nodes_in_row']
    target_nodes_row=list(target_nodes_row)
    target_nodes_in_column=target['nodes_in_column']



    test_list = [i for i in range(len(target_nodes_row))]
    unknown_nodes=len(target_nodes_row)-1 if len(target_nodes_row) ==3 else len(target_nodes_row)-2 \
                   if len(target_nodes_row)<=4  else len(target_nodes_row)-3
    if len(target_nodes_row) <=2:
        unknown_nodes=0

        


    test_list=random.sample(test_list, unknown_nodes)
    X=['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10','r11','r12','r13']
    Y=X

    X_=random.sample(X, len(target_nodes_row)-1)
    target_nodes_row=list(target_nodes_row)
    target_nodes_row_=target_nodes_row.copy()
    if len(target_nodes_row_)>=2:
        j_=0
        for i in test_list:

            target_nodes_row_[i]=X_[j_]
            j_=j_+1
    else:
    	print(len(target_nodes_row_))





    unknown_nodes=len(target_nodes_in_column)-1 if len(target_nodes_in_column) <=3 else len(target_nodes_in_column)-2 \
                   if len(target_nodes_in_column)<=4  else len(target_nodes_in_column)-3



    if len(target_nodes_in_column) <=2:
        unknown_nodes=0 
    test_list = [i for i in range(len(target_nodes_in_column))]
    test_list=random.sample(test_list, unknown_nodes)
    X=['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13']

    X=random.sample(X, len(target_nodes_in_column)-1)
    target_nodes_in_column=list(target_nodes_in_column)
    target_nodes_in_column_=target_nodes_in_column.copy()
    j=0
    if len(target_nodes_in_column_)>2:
        j=0
        for i in test_list:

            target_nodes_in_column_[i]=X[j]
            j=j+1
    #
    column_variable=X[:j]
    row_variables=X_[:j_]




    ######



    sol_row=find_mask(row_variables,target_nodes_row_,target_nodes_row)

    sol_column=find_mask(column_variable,target_nodes_in_column_,target_nodes_in_column)

    for ni,n in enumerate(target_nodes_row_):
        if n not in Y:
            target_nodes_row_[ni]='S'+str(ni)

    for ni,n in enumerate(target_nodes_in_column_):
        if n not in X:
            target_nodes_in_column_[ni]='T'+str(ni)



    item={'source_nodes':source_nodes_row,'source_adj':source_adj,'target_adj':target_adj,\
         'source_nodes_order_in_row':source_nodes_row,'source_nodes_order_in_column':source_nodes_column,\
         'target_nodes_order_in_row':target_nodes_row,'target_nodes_order_in_column':target_nodes_in_column,\
         'masked_target_nodes_order_in_row':target_nodes_row_,
         'masked_target_nodes_order_in_column':target_nodes_in_column_,\
         'column_variable':column_variable,'row_variables':row_variables,'sol_row':sol_row,'sol_column':sol_column,'Type_':Type_}

    return item


def get_type(E):
    t={'incoming':0,'outgoing':0}
    Nodes_income_out={}

    for e1 in E:
        n1,n2=e1[0],e1[1]
        if n1 not in Nodes_income_out.keys():
            Nodes_income_out[n1]={'incoming':0,'outgoing':0}

        if n2 not in Nodes_income_out.keys():
            Nodes_income_out[n2]={'incoming':0,'outgoing':0}

        Nodes_income_out[n1]['outgoing']+=1
        Nodes_income_out[n2]['incoming']+=1


    type_=[]
    pattern={}
    for k in Nodes_income_out.keys():
        incoming=Nodes_income_out[k]['incoming']
        outgoing=Nodes_income_out[k]['outgoing']
        if str(incoming)+'-'+str(outgoing) in pattern.keys():
            continue
        pattern[str(incoming)+'-'+str(outgoing)]=0
        for k2 in Nodes_income_out.keys():
            incoming_=Nodes_income_out[k2]['incoming']
            outgoing_=Nodes_income_out[k2]['outgoing']

            if incoming==incoming_ and outgoing==outgoing_:
                pattern[str(incoming)+'-'+str(outgoing)]+=1

    pattern=[p+'*'+str(pattern[p])+'#' for p in pattern.keys()]
    pattern=''.join(pattern)

    return pattern



def v2_graphmapping():
    number_of_nodes=random.randint(5, 8)
    Nodes_A=[i for i in range(number_of_nodes)]

    
    Edges=[]
    edges_dic={'-1#-1#':True}
    for node in Nodes_A:
        max_edge=2 if len(Nodes_A)>4 else 2
        number_of_edges=2#random.randint(1, max_edge)
        no = number_of_edges
        a = 0
        b = len(Nodes_A)
        ed=[-1,-1]
        key=[str(t)+'#' for t in ed]
        key = ''.join(key)
        while key in list(edges_dic.keys()) or node  in ed :
            ed = random.sample(Nodes_A, no)
            key=[str(t)+'#' for t in ed]
            key = ''.join(key)
        print('key',key)
        edges_dic[key]=True
        for n in ed:
            if n==node:
                continue
            temp=(node,n)
            Edges.append(temp)

    # if n len(Nodes_A)>5:
    #     inDi_Nodes = random.sample(Nodes_A, 2)
    ##
    e=random.sample(Edges, 1)[0]
    Edges.remove(e)
    n2=n1=0
    n3=0
    while n1==n2 and  (n2,n1)  in Edges and (n2,n1)!=e and (n3,n1)!=e:
        n2 = random.sample(Nodes_A, 1)[0]
        n1 = random.sample(Nodes_A, 1)[0]
        n3 = random.sample(Nodes_A, 1)[0]

    temp=(n2,n1)
    
    print('Edges',Edges)
    print(temp in Edges)
    Edges.append(temp)
    temp=(n3,n1)
    Edges.append(temp)
    ###########################
    
    # n2=n1=0
    # while n1==n2 and  (n1,n2)  in Edges and (n1,n2)!=e:
    #     n2 = random.sample(Nodes_A, 1)[0]
    #     n1 = random.sample(Nodes_A, 1)[0]

    # temp=(n1,n2)
    
    # print('Edges',Edges)
    # print(temp in Edges)
    # Edges.append(temp)


    # row=[0  for n in Nodes_A ]

    # adj_A=[row for n in Nodes_A]
    # adj_A=np.array(adj_A)
    # nodes_A_dic={}
    # temp=0
    # for n in Nodes_A:
    #     nodes_A_dic[n]=temp
    #     temp=temp+1

    # for e in Edges:
    #     i,j=e[0],e[1]
    #     i,j=nodes_A_dic[i],nodes_A_dic[j]

    #     adj_A[i,j]=1

    # adj_source=adj_A.tolist()

    # print('adj_source',adj_source)
    # exit()
    ######################











    Edges_A=Edges

    Nodes_B=copy.deepcopy(Nodes_A)
    Edges_B=copy.deepcopy(Edges_A)
    print('Nodes_B',Nodes_B)
    print('Edges_B',Edges_B)
    # check
    type_=get_type(Edges_A)







    return Nodes_A,Nodes_B,Edges_A,Edges_B,type_


       





def prepare_data(data,cross,version,Overwrite_cross):
    data_processes=[]
    if version=='v2':
        alphabet=['a','b','c','d','e','f','g','h','k','l','m','n','p','q','o','w','i', 'j', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z']
        alphabet2=copy.deepcopy(alphabet)
        alphabet2=[
                        "α", "β", "γ", "δ", "ε", "ζ", "η", "θ",
                        "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π",
                        "ρ", "σ", "ς", "τ", "υ", "φ", "χ", "ψ", "ω"
                    ]
    else:
        alphabet=['a','b','c','d','e','f','g','h',]
        alphabet2=['k','l','m','n','p','q','o','w']

    	

    random.shuffle(alphabet)
    print('cross',cross)

    for d in data:
        #print('+++++++')
        #print('d',d)
        nodes_A_dic={}
        nodes_B_dic={}
        Nodes_A=d['Nodes_A']
        Edges_A=d['Edges_A']
        
        Nodes_B=d['Nodes_B']

        Edges_B=d['Edges_B']
        Type_=d['Type']

        if version=='v2':
            # print('Nodes_A',Nodes_A)
            # print('Edges_A',Edges_A)
            # print('Nodes_B',Nodes_B)
            # print('Edges_B',Edges_B)
            # continue
            #exit()
            Nodes_A,Nodes_B,Edges_A,Edges_B,Type_=v2_graphmapping()




        temp=0
        for n in Nodes_A:
            nodes_A_dic[n]=temp
            temp=temp+1
        temp=0  
        for n in Nodes_B:
            nodes_B_dic[n]=temp
            temp=temp+1#


        if version!='v2':

            print(nodes_B_dic,nodes_B_dic)
            Right_button_targets=d['Right_button_targets']
            Left_button_targets=d['Left_button_targets']
            #print('Right_button_targets',Right_button_targets)
            #print('Left_button_targets',Left_button_targets)
            
            m,n=Right_button_targets[0],Right_button_targets[1]
            Right_button_targets=[nodes_A_dic[m],nodes_B_dic[n]]
            
            
            m,n=Left_button_targets[0],Left_button_targets[1]
            Left_button_targets=[nodes_A_dic[m],nodes_B_dic[n]]
        else:
            Left_button_targets=[0,0]
            Right_button_targets=[0,0]
        
        #print('Right_button_targets',Right_button_targets)
        #print('Left_button_targets',Left_button_targets)
        Crossed_edges=d['Crossed_edges']

        if version=='v2':
            Crossed_edges='True'
       
        if Overwrite_cross==False:
             
            if len(Crossed_edges)==0 or Crossed_edges=='no':
                cross='False' 
                Crossed_edges='False' 
            else:
                Crossed_edges='True' 
                cross='True' 



        if  Overwrite_cross==True: 
     
            Crossed_edges=cross



        # print('cross',cross)
        # print('Overwrite_cross',Overwrite_cross)
        # exit()


        

  

        nodes_source=[alphabet[i] for i,n in enumerate(Nodes_A)]
        nodes_target=[alphabet2[i] for i,n in enumerate(Nodes_B)]
        if version=='v2':
        	nodes_target=copy.deepcopy(nodes_source)
        
        n1,n2=Left_button_targets[0],Left_button_targets[1]
        Left_button_targets=[nodes_source[n1],nodes_target[n2]]
        ####
        n1,n2=Right_button_targets[0],Right_button_targets[1]
        Right_button_targets=[nodes_source[n1],nodes_target[n2]]
        row=[0  for n in nodes_source ]

        adj_A=[row for n in nodes_source]
        adj_A=np.array(adj_A)

        for e in Edges_A:
            i,j=e[0],e[1]
            i,j=nodes_A_dic[i],nodes_A_dic[j]

            adj_A[i,j]=1

        adj_source=adj_A.tolist()
        ##
        adj_B=[row for n in nodes_source]
        adj_B=np.array(adj_B)


 

        for e in Edges_B:
            i,j=e[0],e[1]
            i,j=nodes_B_dic[i],nodes_B_dic[j]
            adj_B[i,j]=1

        adj_target=adj_B.tolist()
        # print('adj_B',adj_B)
        # print('adj_A',adj_A)

        if version=='v2':
        	adj_target=adj_source

        Crossed_edges=cross
        adj_A=list(adj_A)
        adj_B=list(adj_B)

        target_nodes_in_column=copy.deepcopy(nodes_target) 


        print('Crossed_edges:',Crossed_edges)


        adj_target,nodes_target,target_nodes_in_column=crossing_rows_and_v2(adj_target,nodes_target,cross=cross)

        item=     {'Type_':Type_,'Right_button_targets':Right_button_targets,'Left_button_targets':Left_button_targets,\
		'Crossed_edges':Crossed_edges,'source':{'adj':adj_source,'nodes_in_row':nodes_source,\
		'nodes_in_column':nodes_source},'target':{'adj':adj_target,'nodes_in_row':nodes_target,\
		'nodes_in_column':target_nodes_in_column}
		}




        if version!='v2':
        	data_processes.append(item)
        else:
            item=mask_nodes(item)
            # print('item',item)
            # exit()
            
            #continue
            data_processes.append(item)







    #exit()
    return data_processes
    


##


def shuflle_given__in_columns(adj,nodes_in_column):
    #print('nodes_in_column',nodes_in_column)
    nodes_in_column=nodes_in_column.copy()
    adj=adj.copy()
    
    adj=np.array(adj)
    for i in range(2):
        n,m=random.sample([i for i in range(len(nodes_in_column))], 2)
        adj[:, [n, m]] = adj[:, [m, n]]
        temp=nodes_in_column[n]
        nodes_in_column[n]=nodes_in_column[m]
        nodes_in_column[m]=temp
    #print('nodes_in_column',nodes_in_column)
    return adj.tolist(),nodes_in_column




###
def return_logic(adj,c_order,r_order):

    
    column_dic={}
    row_di={}
    logic={}
    adj_np=np.array(adj)
    for i in range(len(r_order)):
        node=r_order[i]
        row_di[node]=i
        
    for i in range(len(c_order)):
        node=c_order[i]
        column_dic[node]=i

    for i in range(len(adj)):
        node=r_order[i]
        node_column=column_dic[node]
        node_row=row_di[node]
        incoming_edge=[]
        outgoing_edge=[]
        for j in range(len(adj)):
            node_to=r_order[j]
            #node_column=column_dic[node]
            #node_row=row_di[node]
            if adj_np[node_row,j]==1:
                outgoing_edge.append(node_to)
        for j in range(len(adj)):
            node_from=c_order[j]
            #node_column=column_dic[node]
            #node_row=row_di[node]
            if adj_np[j,node_column]==1:
                incoming_edge.append(node_to)
     
        logic[node]={'outgoing':outgoing_edge,'incoming':incoming_edge}
    return logic
                
            
def organize_item(d,id_No,l,train,di):

    Right_button_targets=d['Right_button_targets']
    Left_button_targets=d['Left_button_targets']
    Crossed_edges=d['Crossed_edges']
    source=d['source']
    target=d['target']
    Type_=d['Type_']

    print('Type_',Type_)
    #exit()
    Crossed_edges=d['Crossed_edges']
    #print('Crossed_edges',Crossed_edges)
    if Crossed_edges=='False':
        Crossed_edges='no'
    source_adj=source['adj']

    source_nodes=source['nodes_in_row']
    target_adj=target['adj']
    

    target_nodes=target['nodes_in_row']
    target_nodes_row=list(target_nodes)
    target_nodes_in_column=target['nodes_in_column']
    nodes_to_map=[Right_button_targets[0],Left_button_targets[0]]
    map_solution=Right_button_targets,Left_button_targets
    map_solution={Right_button_targets[0]:Right_button_targets[1],Left_button_targets[0]:Left_button_targets[1]}
    #print('*****')
    #print(str(l)+'_sample_'+str(di))
    if train:
        name=str(l)+'_train_'+str(di)
    else:
        name=str(l)+'_test_'+str(di)

    target_column_order=target_nodes_in_column

    item={'name':name,'source_nodes':source_nodes,'source_adj':source_adj,'target_adj':target_adj,\
         'row_nodes_order_source':source_nodes,\
          'column_nodes_order_source':source_nodes,\
         'row_nodes_order_target':target_nodes_row,\
         'column_nodes_order_target':target_nodes_in_column,
         'map_solution':map_solution,\
         'nodes_to_map':nodes_to_map,'Crossed_edges':Crossed_edges,'Type_':Type_}
    return item

def print_as_question(id_No,l,data,solution,train=False):

    Questions=''

    List_questions={}

    for di,d in enumerate(data):

        item=organize_item(d,id_No,l,train,di)
        temp_=''

        temp_='\n'+temp_ +f'\n ***********************'

        source_adj=item['source_adj']
        target_adj=item['target_adj']
        row_nodes_order_source=item['row_nodes_order_source']
        row_nodes_order_target=item['row_nodes_order_target']
        column_nodes_order_source=item['column_nodes_order_source']
        column_nodes_order_target=item['column_nodes_order_target']
        
        map_solution=item['map_solution']
        nodes_to_map=item['nodes_to_map']
        Crossed_edges=item['Crossed_edges']
        name=item['name']
        type_=item['Type_']


        temp_='\n'+temp_ +f'\n question no: {name}'
        ##
        temp_=temp_ +f'\n Initially: '
        temp_=temp_ +f'\n   source_adj: {source_adj}'
        temp_=temp_ +f'\n    nodes order in row, source adj = : {row_nodes_order_source}'
        temp_=temp_ +f'\n     nodes order in column, source adj =  {column_nodes_order_source}'
        temp_=temp_ +f'\n after renaming nodes,'
        temp_=temp_ +f'\n   target_adj=  {target_adj}'
        temp_=temp_ +f'\n     nodes order in row, target adj = : {row_nodes_order_target}'
        temp_=temp_ +f'\n     nodes order in column, target adj =  {column_nodes_order_target}'
        temp_=temp_ +f'\n   Crossed_edges=  {Crossed_edges}'
        temp_=temp_ +f'\n Quesetion: map given source nodes to appropriate target nodes: {nodes_to_map}'
        ##
        if solution:

            temp_=temp_ +f'\n Solution as dic: '

            temp_=temp_ +f'\n solution map: {map_solution}'

        Questions=Questions+temp_
        #List_questions[name]= copy.copy(temp_)
        List_questions[name]= {'q':copy.copy(temp_),'map_solution':map_solution,'eval_d':item}

    return Questions,List_questions
        

def print_as_question_v2(data,l,train,solution):

    Questions=''
    List_questions={}

    Questions=Questions +'\n ***********************'


    for di,d in enumerate(data):



        source_adj=d['source_adj']
        target_adj=d['target_adj']
        source_nodes_order_in_row=d['source_nodes_order_in_row']
        target_nodes_order_in_row=d['target_nodes_order_in_row']
        source_nodes_order_in_column=d['source_nodes_order_in_column']
        target_nodes_order_in_column=d['target_nodes_order_in_column']
        masked_target_nodes_order_in_row=d['masked_target_nodes_order_in_row']
        masked_target_nodes_order_in_column=d['masked_target_nodes_order_in_column']
        sol_row=d['sol_row']
        sol_column=d['sol_column']
        column_variable=d['column_variable']
        row_variables=d['row_variables']
        Type_=d['Type_']

 
        if train==True:
            name=str(l)+'_train_'+str(di)
        else:
            name=str(l)+'_test_'+str(di)
        if len(source_nodes_order_in_row)<=2:
        	continue

        temp_=''
        temp_=temp_ +f'\n ***********************'
        temp_=temp_ +f'\n {name}:'
        temp_=temp_ +f'\n Initially: '
        temp_=temp_ +f'\n     nodes_order_in_row = : {source_nodes_order_in_row}'
        temp_=temp_ +f'\n     nodes_order_in_column = : {source_nodes_order_in_column}'
        temp_=temp_ +f'\n    source_adj = : {source_adj}'
        temp_=temp_ +f'\n after swapping rows, columns'
        temp_=temp_ +f'\n    target_adj = : {target_adj}'
        temp_=temp_ +f'\n     maksed_target_row_order = : {masked_target_nodes_order_in_row}'
        temp_=temp_ +f'\n     maksed_target_column_order = : {masked_target_nodes_order_in_column}'
        temp_=temp_ +f'\n Question:'
        temp_=temp_ +f'\n map the mask variables in column and row  to source nodes:'
        temp_=temp_ +f'\n     mask variabbles in row : {row_variables}'
        temp_=temp_ +f'\n     mask variabbles in column : {column_variable}'
        #print('temp_',temp_)
        if solution:
            temp_=temp_+f'\n solution is as below: '
            temp_=temp_+f'\n sol_row: {sol_row}'
            temp_=temp_+f'\n sol_column: {sol_column}'


      
        Questions=Questions+temp_
        List_questions[name]= {'q':copy.copy(temp_),'sol_row':sol_row,'sol_column':sol_column,'eval_d':d,'Type_':Type_}

        #print('Questions',Questions)
        #print('sol_column',sol_column)
        #exit()

    return Questions,List_questions



def get_prompt(q,train,version):
    if version=='original':
        prompt_for_original_questions = f"""
        Given two isomorphic graphs, namely source and target, your task is to map some of thr target nodes to the coressponding source nodes. Note the following
        Rules:
        - First graph is called source. 
        - Second graph is called target. 
        - For each graph, they are specified using adjacency matrix
        - The order of nodes in the row and column of adj matrix is given for each graph.
        - The target graph is obtained from the source graph by renaming the nodes, and probably shuffling the orders in row and column of adjacency matrix.
        - To help you, with provide some sample training questions, and then you answer the test question.
        - Samples to learn from are below:
                {train}

        - Question to answer is below: 

        {q}


        - make the mappings variables to nodes as dictionary of key and vlaues, with key being variable, and value the node it coresponds to!

        
        """
        return prompt_for_original_questions

    else:
        prompt_for_v2_questions = f"""
        Given two isomorphic graphs, namely source and target, your task is to map some of thr target nodes to the coressponding source nodes. Note the following
        Rules:
        - First graph is called source. 
        - Second graph is called target. 
        - For each graph, they are specified using adjacency matrix
        - The order of nodes in the row and column of adj matrix is given for each graph.
        - The target graph is obtained from the source graph by renaming the nodes, and probably shuffling the orders in row and column of adjacency matrix.
        - To help you, with provide some sample training questions, and then you answer the test question.
        - Samples to learn from are below:
                {train}

        - Question to answer is below: 
        {q}
        - make the mappings variables to nodes as dictionary of key and vlaues, with key being variable, and value the node it coresponds to!


        """
        return prompt_for_v2_questions
        

def get_prompt_hf():
    p = f"""
        Given two isomorphic graphs, namely source and target, your task is to map some of thr target nodes to the coressponding source nodes. Note the following
        Rules:
        - First graph is called source. 
        - Second graph is called target. 
        - For each graph, they are specified using adjacency matrix
        - The order of nodes in the row and column of adj matrix is given for each graph.
        - The target graph is obtained from the source graph by renaming the nodes, and probably shuffling the orders in row and column of adjacency matrix.
    
        - make the mappings variables to nodes as dictionary of key and vlaues, with key being variable, and value the node it coresponds to!

        
        """
    return p

def get_prompt_(q,train,version):
    if version=='original':
        prompt_for_original_questions = f"""
        Given two isomorphic graphs, namely source and target, your task is to map some of thr target nodes to the coressponding source nodes. Note the following
        Rules:
        - First graph is called source. 
        - Second graph is called target. 
        - For each graph, they are specified using adjacency matrix
        - The order of nodes in the row and column of adj matrix is given for each graph.
        - The target graph is obtained from the source graph by renaming the nodes, and probably shuffling the orders in row and column of adjacency matrix.
    

        - Question to answer is below: 

        {q}


        - make the mappings variables to nodes as dictionary of key and vlaues, with key being variable, and value the node it coresponds to!

        
        """
        return prompt_for_original_questions

    else:
        prompt_for_v2_questions = f"""
        Given two isomorphic graphs, namely source and target, your task is to map some of thr target nodes to the coressponding source nodes. Note the following
        Rules:
        - First graph is called source. 
        - Second graph is called target. 
        - For each graph, they are specified using adjacency matrix
        - The order of nodes in the row and column of adj matrix is given for each graph.
        - The target graph is obtained from the source graph by renaming the nodes, and probably shuffling the orders in row and column of adjacency matrix.
 

        - Question to answer is below: 
        {q}
        - make the mappings variables to nodes as dictionary of key and vlaues, with key being variable, and value the node it coresponds to!


        """

        print('prompt_for_v2_questions',q)

        return prompt_for_v2_questions



from pydantic import BaseModel, Field
from typing import List, Optional
class Mapping_Original(BaseModel):
    source: str = Field(description="Name of the source node.")
    target: str = Field(description="Name of the target node.")



class Answer_original(BaseModel):
    questions_id:str= Field(description="question No")
    list_of_variable_mappings:List[Mapping_Original]
###

class Mapping_v2_row(BaseModel):
    row_variable: str = Field(description="row variable")
    coresponding_node: str = Field(description="coresponding node")

class Mapping_v2_column(BaseModel):
    column_variable: str = Field(description="column variable")
    coresponding_node: str = Field(description="coresponding variable")


class Answer_v2(BaseModel):
    questions_id:str= Field(description="question NO")
    sol_row:List[Mapping_v2_row]
    sol_column:List[Mapping_v2_column]     

def ask_ai(selected_model,Qs,train,version,Show_train_set,one_by_one=True):


    if selected_model['agent']=='gpt':

        
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    else:
        from google import genai
        import json
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])




    if one_by_one==False:
        pass


    else:
        def get_answer(selected_model,questions,train_questions,version,client):
            answer_class=Answer_original if version=='original' else Answer_v2

            if Show_train_set:
                prompt = get_prompt(questions,train_questions,version)
            else:
                prompt = get_prompt_(questions,train_questions,version)

            #print('prompt',prompt)


        
            if selected_model['agent']=='gpt':




                response = client.responses.parse(
                    model=selected_model['model'],#"gpt-4.1-mini",
                    #model="gpt-5-nano",
                    input=[
                        {
                            "role": "user",
                            "content": [
                                       {
                                    "type": "input_text",
                                    "text": prompt,
                                },
                            ]
                        }
                    ]
                    ,
                    text_format=answer_class,

                )

                response = response.output_parsed
                return response

            elif selected_model['agent']=='gemini':
                from google import genai
               


                ###
                # print('answer_class.model_json_schema()',answer_class.model_json_schema())
                # exit()

                response = client.models.generate_content(
                    model=selected_model['model'],#"gemini-3-flash-preview",
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": answer_class.model_json_schema(),
                    },
                )

                temp = answer_class.model_validate_json(response.text)
                return temp

            elif  selected_model['agent'] in ['hf','gwdg']:

                


                model=selected_model['model']

                if selected_model['agent'] =='hf':
          
        
                    client = OpenAI(
                        base_url="https://router.huggingface.co/v1",
                        api_key=os.environ["HF_TOKEN"],
                    )
                else:
                    gwdg_api_key='21816d10af937e0b236b3da7b1bfe05b'
                    API_endpoint= "https://chat-ai.academiccloud.de/v1"

                    # API configuration
                    api_key =gwdg_api_key # Replace with your API key
                    base_url = "https://chat-ai.academiccloud.de/v1"
                    model = "llama-3.1-sauerkrautlm-70b-instruct"#"qwen3-30b-a3b-thinking-2507" # llama-3.1-sauerkrautlm-70b-instruct
                      
                    # Start OpenAI client
                    client = OpenAI(
                        api_key = api_key,
                        base_url = base_url,

                    )

                prompt=get_prompt_hf()
                


                response = client.responses.parse(
                    model=model,
                    input=[
                        {"role": "system", "content": prompt},
                        {
                            "role": "user",
                            "content": q,
                        },
                    ],
                    text_format=answer_class,
                )

                answer_cot = response.output_parsed
                

                #print('answer_cot',answer_cot)
                # exit()
                return answer_cot


            elif selected_model['agent'] =='DASHSCOPE':
                #print('test',)
                # client = OpenAI(
                #     api_key=os.getenv("DASHSCOPE_API_KEY"),
                #     # The following is the base_url for the Singapore region.
                #     base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",  
                # )
          

                client = OpenAI(
                    # If environment variable is not set, replace with: api_key="sk-xxx"
                    api_key=os.getenv("DASHSCOPE_API_KEY"),
                    base_url="https://dashscope-intl.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1",
                )

                # response = client.responses.create(
                #     model="qwen3.5-plus",
                #     input="What can you do?"
                # )

                # # Get model response
                # print(response.output_text)
                # exit()



                model=selected_model['model']

                prompt=get_prompt_hf()
                response = client.responses.parse(
                    model=model,
                    input=[
                        {"role": "system", "content": prompt},
                        {
                            "role": "user",
                            "content": q,
                        },
                    ],
                    text_format=answer_class,
                )

                #print('response',response)
                response = response.output_parsed
                return response
                 
              

        Data_all={}
        Answers_all=[]
       
        for qi,q in enumerate(Qs):
            print('qi',qi)
            q_=Qs[q]

            if version=='original':
                
            
                q=q_['q']
                eval_d=q_['eval_d']
                map_solution=q_['map_solution']

                name=eval_d['name']
                type_=eval_d['Type_']
                #print('type_',type_)

                #print('q',q)
                #print('################')
                #continue


                start_time = datetime.datetime.now()
                an=None
                try_n=0
                while an==None and try_n<4:
                    #an=get_answer(selected_model,q,train,version,client)
                    try:
                      an=get_answer(selected_model,q,train,version,client)
                      #print('an',an)
                    except:
                      print("An exception occurred")
             
                    try_n+=1

                if an!=None:
                    list_of_variable_mappings=an.list_of_variable_mappings
                    an_obtained={}
                    for t in list_of_variable_mappings:
                        source=t.source 
                        target=t.target
                        an_obtained[source]=target
                    end_time = datetime.datetime.now()
                    duration=end_time-start_time
                    duration= duration.total_seconds()
                    item={'eval_d':eval_d,'map_solution':map_solution,'an_obtained':an_obtained,'q':q,'duration':duration,'start_time':str(start_time)}
                else:
                    print('an',an)
                    print('failed')
                    item={'eval_d':eval_d,'map_solution':map_solution,'an_obtained':'None','q':q,'duration':'None','start_time':'None'}

                Answers_all.append(item)
                time.sleep(6)
            else:
                q=q_['q']
             
                eval_d=q_['eval_d']
                sol_row_=q_['sol_row']
                sol_column_=q_['sol_column']
                Type_=q_['Type_']
                start_time = datetime.datetime.now()
                an=get_answer(selected_model,q,train,version,client)
                #print('an',an)
                end_time = datetime.datetime.now()
                duration=end_time-start_time
                duration= duration.total_seconds()

                time.sleep(6)

       
                
                an_row_obtained={}
                an_col_obtained={}
      
                sol_column=an.sol_column
                sol_row=an.sol_row
                print('######')
                for k in q_.keys():
                    #print('k',k)
                    d=q_[k]
                    #print('d',d)


                for c in sol_column:
                    #print('c',c)
                    column_variable=c.column_variable
                    coresponding_node=c.coresponding_node
                    an_col_obtained[column_variable]=coresponding_node
                for c in sol_row:
                    #print('c',c)
                    row_variable=c.row_variable
                    coresponding_node=c.coresponding_node
                    an_row_obtained[row_variable]=coresponding_node



                print('sol_row_',sol_row_)
                print('an_row_obtained',an_row_obtained)
                print('***')
                print('sol_column_',sol_column_)
                print('an_col_obtained',an_col_obtained)
                print('type_',Type_)




                item={'eval_d':eval_d,'sol_row_':sol_row_,'sol_column_':sol_column_,\
                'an_row_obtained':an_row_obtained,'an_col_obtained':an_col_obtained,'q':q,'duration':duration}

                Answers_all.append(item)
                
               
    return Answers_all

            

                


         