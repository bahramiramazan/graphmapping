
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
#############

    
key=''

GEMINI_KEY=''
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
import numpy as np



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
		X=['r1','r2','r3','r4','r5','r6','r7','r8','r9','r10']
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
			#exit()
		####

		######
		unknown_nodes=len(target_nodes_in_column)-1 if len(target_nodes_in_column) <=3 else len(target_nodes_in_column)-2 \
		               if len(target_nodes_in_column)<=4  else len(target_nodes_in_column)-3
		if len(target_nodes_in_column) <=2:
		    unknown_nodes=0 
		test_list = [i for i in range(len(target_nodes_in_column))]
		test_list=random.sample(test_list, unknown_nodes)
		X=['c1','c2','c3','c4','c5','c6','c7','c8','c9','c10']
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


		####

		sol_row=find_mask(row_variables,target_nodes_row_,target_nodes_row)

		sol_column=find_mask(column_variable,target_nodes_in_column_,target_nodes_in_column)


		item={'source_nodes':source_nodes_row,'source_adj':source_adj,'target_adj':target_adj,\
		     'source_nodes_order_in_row':source_nodes_row,'source_nodes_order_in_column':source_nodes_column,\
		     'target_nodes_order_in_row':target_nodes_row,'target_nodes_order_in_column':target_nodes_in_column,\
		     'masked_target_nodes_order_in_row':target_nodes_row_,
		     'masked_target_nodes_order_in_column':target_nodes_in_column_,\
		     'column_variable':column_variable,'row_variables':row_variables,'sol_row':sol_row,'sol_column':sol_column,'Type_':Type_}

		return item


def prepare_data(data,cross,version,Overwrite_cross):
    data_processes=[]
    alphabet=['a','b','c','d','e','f','g']
    alphabet2=['k','l','m','n','o','p','q']
    if version=='v2':
    	alphabet2=copy.deepcopy(alphabet)

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

        #print('type',Type_)
        #exit()


        temp=0
        for n in Nodes_A:
            nodes_A_dic[n]=temp
            temp=temp+1
        temp=0  
        for n in Nodes_B:
            nodes_B_dic[n]=temp
            temp=temp+1#

        
        Right_button_targets=d['Right_button_targets']
        Left_button_targets=d['Left_button_targets']
        #print('Right_button_targets',Right_button_targets)
        #print('Left_button_targets',Left_button_targets)
        
        m,n=Right_button_targets[0],Right_button_targets[1]
        Right_button_targets=[nodes_A_dic[m],nodes_B_dic[n]]
        
        
        m,n=Left_button_targets[0],Left_button_targets[1]
        Left_button_targets=[nodes_A_dic[m],nodes_B_dic[n]]
        
        #print('Right_button_targets',Right_button_targets)
        #print('Left_button_targets',Left_button_targets)
        Crossed_edges=d['Crossed_edges']
        #print('Crossed_edges',Crossed_edges)
        #exit()
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

        if version=='v2':
        	adj_target=adj_source

        Crossed_edges=cross
        adj_A=list(adj_A)
        adj_B=list(adj_B)

        target_nodes_in_column=copy.deepcopy(nodes_target) 


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
            #print('item',item)
            
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
        #print('type_',type_)
   
        #exit()

        #####
        

        temp_='\n'+temp_ +f'\n question no: {name}'
        

        # print('  Initially: ')
        # print('    source_adj',source_adj)
        # print('    nodes order in row, source adj = ',row_nodes_order_source)
        # print('    nodes order in column, source adj = ',column_nodes_order_source)
        # print('  renaming nodes and reordering:')
        # print('    target_adj',target_adj)
        # print('    nodes order in row, target adj = ',row_nodes_order_target)
        # print('    nodes order in column, target adj = ',column_nodes_order_target)
        # print('    Crossed_edges',Crossed_edges)
        # print(' Quesetion: map given source nodes to appropriate target nodes: ',nodes_to_map)
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
        #print(' ')
            #print('id_No',id_No)
            temp_=temp_ +f'\n Solution as dic: '

            temp_=temp_ +f'\n solution map: {map_solution}'

         
            # source_logic_all=return_logic(source_adj,column_nodes_order_source,row_nodes_order_source)
            # #print('source_logic_all',source_logic_all)
            # target_logic_all=return_logic(target_adj,column_nodes_order_target,row_nodes_order_target)
            # #print(source_logic)
            # print('step by step solution')
            # temp_=temp_ +f'\n step by step solution '
            # for n in map_solution.keys():
            
            #     node_source=n
            #     node_target=map_solution[n]

            #     source_logic=source_logic_all[node_source]
            #     source_incoming=source_logic['incoming']
            #     source_outgoing=source_logic['outgoing']
            #     ##
            #     target_logic=target_logic_all[node_target]
            #     target_incoming=target_logic['incoming']
            #     target_outgoing=target_logic['outgoing']
            #     continue
                
            #     print('* Has_connectoin_to('+str(node_source)+')=',source_outgoing)
            #     print('Has_connectoin_from('+str(node_source)+')=',source_incoming)
                
            #     print('in the target graph: ')
            #     print('* Has_connectoin_to('+str(node_target)+')=',target_outgoing)
            #     print('* Has_connectoin_from('+str(node_target)+')=',target_incoming)
            #     print('therefore:')
            #     print('    ',node_source,'->',node_target)

        Questions=Questions+temp_
        #List_questions[name]= copy.copy(temp_)
        List_questions[name]= {'q':copy.copy(temp_),'map_solution':map_solution,'eval_d':item}

    return Questions,List_questions
        

def print_as_question_v2(data,l,train,solution):

    Questions=''
    List_questions={}

    Questions=Questions +'\n ***********************'


    for di,d in enumerate(data):


		# item={'source_nodes':source_nodes_row,'source_adj':source_adj,'target_adj':target_adj,\
		#      'source_nodes_order_in_row':source_nodes_row,'source_nodes_order_in_column':source_nodes_column,\
		#      'target_nodes_order_in_row':target_nodes_row,'target_nodes_order_in_column':target_nodes_in_column,\
		#      'masked_target_nodes_order_in_row':target_nodes_row_,
		#      'masked_target_nodes_order_in_column':target_nodes_in_column_,\
		#      'column_variable':column_variable,'row_variables':row_variables,'sol_row':sol_row,'sol_column':sol_column}
        
       

        # Alternative solutions 


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
        if train==True:
            name=str(l)+'_train_'+str(di)
        else:
            name=str(l)+'_test_'+str(di)
        if len(source_nodes_order_in_row)<=2:
        	continue
        # print(name)
        # print('initially:')
        # print('    nodes_order_in_row = ',source_nodes_order_in_row)
        # print('    nodes_order_in_column = ',source_nodes_order_in_column)
        # print('    source_adj:',source_adj)
        # print('after swapping rows, columns ')

        # print('    target_adj:',target_adj)
    

        # print('     maksed_target_row_order',masked_target_nodes_order_in_row)
        # print('     maksed_target_column_order',masked_target_nodes_order_in_column)
        # print('Question:')
        # print(' map the mask variables in column and row  to source nodes:')
        # print(' mask variabbles in row',row_variables)
        # print(' mask variabbles in column',column_variable)
        ##
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
        List_questions[name]= {'q':copy.copy(temp_),'sol_row':sol_row,'sol_column':sol_column,'eval_d':d}

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
        return prompt_for_v2_questions
        

def ask_ai(selected_model,Qs,train,version,Show_train_set,one_by_one=True):


    if selected_model['agent']=='gpt':

        from openai import OpenAI
        client = OpenAI(api_key=key)
    else:
        from google import genai
        import json
        client = genai.Client(api_key=GEMINI_KEY)




    if one_by_one==False:
        pass


    else:
        def get_answer(selected_model,questions,train_questions,version,client):

            if Show_train_set:
                prompt = get_prompt(questions,train_questions,version)
            else:
                prompt = get_prompt_(questions,train_questions,version)

            print('prompt',prompt)


        
            if selected_model['agent']=='gpt':

                from openai import OpenAI
                from pydantic import BaseModel
                import ast
           
                class Mapping_Original(BaseModel):
                    source: str
                    target: str


                class Mapping_v2_row(BaseModel):
                    row_variable: str
                    coresponding_node: str

                class Mapping_v2_column(BaseModel):
                    column_variable: str
                    coresponding_node: str

                class Answer_original(BaseModel):
                    questions_id: str
                    list_of_variable_mappings:list[Mapping_Original] #list[str]#[dict]


                class Answer_v2(BaseModel):
                    questions_id: str
                    sol_row: list[Mapping_v2_row]#[dict]
                    sol_column: list[Mapping_v2_column]#[dict]

                answer_class=Answer_original if version=='original' else Answer_v2

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

            else:
                from google import genai
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


                ###
                answer_class=Answer_original if version=='original' else Answer_v2
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
                print('type_',type_)

                #print('q',q)
                #print('################')
                #continue


                start_time = datetime.datetime.now()
                
                an=get_answer(selected_model,q,train,version,client)

                list_of_variable_mappings=an.list_of_variable_mappings
                an_obtained={}
                for t in list_of_variable_mappings:
                    source=t.source 
                    target=t.target
                    an_obtained[source]=target
                end_time = datetime.datetime.now()
                duration=end_time-start_time
                duration= duration.total_seconds()
                item={'eval_d':eval_d,'map_solution':map_solution,'an_obtained':an_obtained,'q':q,'duration':duration}

                Answers_all.append(item)
                time.sleep(6)
                
               
            else:
                q=q_['q']
                eval_d=q_['eval_d']
                sol_row_=q_['sol_row']
                sol_column_=q_['sol_column']
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


                item={'eval_d':eval_d,'sol_row_':sol_row_,'sol_column_':sol_column_,\
                'an_row_obtained':an_row_obtained,'an_col_obtained':an_col_obtained,'q':q,'duration':duration}

                Answers_all.append(item)
    return Answers_all

            

                


         