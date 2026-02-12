



from utils import *
import json
from numpy import random
import datetime
from solutions import *


#####
with open('files/questions'+str(9)+'.json') as f:
    questions_records = json.load(f)#['Qs']



questions_records={}
questions={}


# L=['348#2025-10-26 10*08*26.179500','978#2025-10-26 10*10*32.210895','57#2025-10-25 08*36*20.929632','558#2025-10-25 09*07*45.897417']
# L=[]
# q_new={}

# for k in L:
#     q_new[k]=questions[k]



# file='questions.json'
# Qs={'Qs':q_new}
# with open(file, 'w') as fp:
#     json.dump(Qs, fp)

# exit()



# def print_data(id_No,l,data,solution,train=False):

#     for di,d in enumerate(data):

#         Right_button_targets=d['Right_button_targets']
#         Left_button_targets=d['Left_button_targets']
#         Crossed_edges=d['Crossed_edges']
#         source=d['source']
#         target=d['target']
#         Type_=d['Type_']
#         Crossed_edges=d['Crossed_edges']
#         #print('Crossed_edges',Crossed_edges)
#         if len(Crossed_edges)==0:
#             Crossed_edges='no'
#         source_adj=source['adj']

#         source_nodes=source['nodes_in_row']
#         target_adj=target['adj']
        
 
#         target_nodes=target['nodes_in_row']
#         target_nodes_row=list(target_nodes)
#         target_nodes_in_column=target['nodes_in_column']
#         nodes_to_map=[Right_button_targets[0],Left_button_targets[0]]
#         map_solution=Right_button_targets,Left_button_targets
#         map_solution={Right_button_targets[0]:Right_button_targets[1],Left_button_targets[0]:Left_button_targets[1]}
#         #print('*****')
#         #print(str(l)+'_sample_'+str(di))
#         if train:
#             name=str(l)+'_train_'+str(di)
#         else:
#             name=str(l)+'_test_'+str(di)

#         target_column_order=target_nodes_in_column

#         item={'name':name,'source_nodes':source_nodes,'source_adj':source_adj,'target_adj':target_adj,\
#              'row_nodes_order_source':source_nodes,\
#               'column_nodes_order_source':source_nodes,\
#              'row_nodes_order_target':target_nodes_row,\
#              'column_nodes_order_target':target_nodes_in_column,
#              'map_solution':map_solution,\
#              'nodes_to_map':nodes_to_map,'Crossed_edges':Crossed_edges,'Type_':Type_}
#         print_as_question(id_No,item,solution=solution)

def print_test_questions(L_train,L_test,id_No,task,corss,version):
    train_sample_no=12
    test_sample_no='60'

    prompt_data={'train':'','test':''}

    train=True if task=='print_train' else False
    config = load_config("Graph_Mapping/config.yaml", concatenate=True)
    print('config',config['predefined_training'])

    list_all_train_data=[]


 

    config = load_config("Graph_Mapping/config.yaml", concatenate=True)
    print('config',config['predefined_training'])

    L=[4,6,8,10,12]
    list_all_train_data=[]
    for l in L_train:
        if l !=train_sample_no:
            continue
        print('##################################')
        Overwrite_cross=False if l=='experiment' else True
 
       #
        config['predefined_training']=str(l)+'_trials.csv'
        file_name=join('Graph_Mapping','trials',"training", config['predefined_training'])

        data_train, _ = load_trials(file_name)

        if version=='original':

            data=prepare_data(data_train,corss,version,Overwrite_cross)
            d={'data':data,'l':l,'id':id_No,'corss':corss}
            questions[id_No]=d
            #print_data(id_No,l,data,solution)
            Questions,List_questions=print_as_question(id_No,l,data,True,train=True)

            prompt_data['train']=Questions
            #prompt_data['questions_as_list']=List_questions
        else:
            train=True
            solution=True
            data=prepare_data(data_train,corss,version,Overwrite_cross)
            d={'data':data,'l':l,'id':id_No,'corss':corss,'version':version}
            questions[id_No]=d
            Questions,List_questions= print_as_question_v2(data,l,train,solution)
            prompt_data['train']=Questions
            #prompt_data['questions_as_list']=List_questions
           



    ################################ TEST #######################################
    
    for l in L_test:
        experiment=True if l=='experiment' else False
        Overwrite_cross=False if l=='experiment' else True

 

        if experiment==False:

            config['predefined_test']='test_'+l+'.csv'

            file_name=join('Graph_Mapping/trials',"tests", config['predefined_test'])
        else:

            config['predefined_test']='experiment.csv'

            file_name=join('Graph_Mapping/trials',"experiment", config['predefined_test'])


        _, data_exp = load_trials(file_name)
        #if config["randomize_trials_order"]:
        #random.shuffle(data_exp)
        if version=='original':
            solution=False

            data=prepare_data(data_exp,corss,version,Overwrite_cross)
            d={'data':data,'l':l,'id':id_No,'corss':corss}
            questions[id_No]=d
            #print_data(id_No,l,data,solution)
            Questions,List_questions=print_as_question(id_No,l,data,solution,train=False)

            prompt_data['test']=Questions
            prompt_data['questions_as_list']=List_questions
        else:
            train=False
            solution=False
            data=prepare_data(data_exp,corss,version,Overwrite_cross)
            d={'data':data,'l':l,'id':id_No,'corss':corss,'version':version}
            questions[id_No]=d
            Questions,List_questions= print_as_question_v2(data,l,train,solution)
            prompt_data['test']=Questions
            prompt_data['questions_as_list']=List_questions


    return prompt_data

####
def generate_questions(task,version,print_existing_id=None,corss='True'):
    print('test')
    id_No = random.randint(1000,size=(1))[0]
    print('id_No',id_No)


    while id_No in questions.keys():
        id_No = random.randint(1000)[0]


    date= datetime.datetime.now()
    date=str(date)
    print('str(x)',str(date))
    id_No=str(id_No)+'#'+str(date)
    id_No=id_No.replace(':','*')

    L=['20','30','44_items','60','easy_26','hard_36','experiment']
    L=[4,6,8,10,12]

    l_train=[12,]
    l_test=['experiment',]





    # file='questions.json'
    # Qs={'Qs':questions}
    # with open(file, 'w') as fp:
    #     json.dump(Qs, fp)



    #######################
    gemini_3_flash_preview={'agent':'gemini','model':"gemini-3-flash-preview"}
    gemini_3_pro_preview={'agent':'gemini','model':"gemini-3-pro-preview"}
    gemini_25_flash={'agent':'gemini','model':"gemini-2.5-flash"}
    
    gemini_25_pro={'agent':'gemini','model':"gemini-2.5-pro"}
    gemini_20_flash={'agent':'gemini','model':"gemini-2.0-flash"}
    ########
    gpt_41_mini={'agent':'gpt','model':"gpt-4.1-mini"}
    gpt_41={'agent':'gpt','model':"gpt-4.1"}


    gpt_5_mini={'agent':'gpt','model':"gpt-5-mini"}
    gpt_5_nano={'agent':'gpt','model':"gpt-5-nano"}
    gpt_52={'agent':'gpt','model':"gpt-5.2"}

    MODELS=[gpt_41_mini,gpt_41,gpt_5_mini,gpt_5_nano,gpt_52,\
    gemini_20_flash,gemini_25_pro,gemini_25_flash,gemini_3_pro_preview,gemini_3_flash_preview]
    

    corss_=corss


    

    

    for mi,m in enumerate(MODELS):
        data=print_test_questions(l_train,l_test,id_No,task,corss_,version)
        questions_as_list=data['questions_as_list']
        train=data['train']

        print('m',m['model'])
        print('mi',mi)
   

        selected_model=m
        Show_train_set=False
        cross_temp='crossed' if cross=='True' else 'not_crossed'
        id_No_=id_No+m['model']



        answers=ask_ai(selected_model,questions_as_list,train,version,Show_train_set)
        #exit()



        
        Record={'Qs':questions,'data':data,'answers':answers,'data_name':l_test[0],'selected_model':selected_model,'Show_train_set':Show_train_set}

        key=l_test[0]
        corss,version
        cross_temp='crossed' if cross else 'not_crossed'
        if key in questions_records.keys():
            questions_records[key][version][cross_temp][id_No_]=Record
        else:
            questions_records[key]={'original':{'crossed':{},'not_crossed':{}},'v2':{}}
            questions_records[key][version][cross_temp][id_No_]=Record

        file='files/questions'+str(key)+'.json'
        with open(file, 'w') as fp:
            json.dump(questions_records, fp)



def eval_answer(flag=False):
    #####
    import itertools
    if flag:
        with open('questions_'+str(60)+'_crossed.json') as f:
            questions_records = json.load(f)#['Qs']
    
    else:
        with open('questions'+str(9)+'.json') as f:
            questions_records = json.load(f)#['Qs']

    # with open('questions'+'easy_26'+'.json') as f:
    #     questions_records = json.load(f)#['Qs']

    # with open('Neuer_Ordner/questions'+'gemini-3-flash-preview'+'.json') as f:
    #     questions_records = json.load(f)#['Qs']






    keys=questions_records.keys()
    direct_indirect_all=[]
    Crossed_not_crossed_all=[]
    no_of_edges_acc_all=[]
    no_of_nodes_acc_all=[]
    Speed_All=[]

    for k in keys:
        print('questions_records[k]',questions_records[k].keys())
        answers_set_all_crossed=questions_records[k]['original']['crossed']
        answers_set_all_not_crossed=questions_records[k]['original']['not_crossed']
    
        total_seconds=0
        tempd=answers_set_all_crossed

        for batchid in tempd:

            answers_set_batch=tempd[batchid]



            questions=answers_set_batch['Qs']
            data=answers_set_batch['data']
            answers=answers_set_batch['answers']
            data_name=answers_set_batch['data_name']
            selected_model=answers_set_batch['selected_model']
            Show_train_set=answers_set_batch['Show_train_set'] if 'Show_train_set' in answers_set_batch.keys() else True

  
            # if 'gpt' not in selected_model['model']:
            #     continue
            print('##############################')
            print('data_name',data_name)
            print('selected_model',selected_model)
            print('Show_train_set',Show_train_set)
            ##
            direct_indirect={}
            Crossed_not_crossed={}
            no_of_edges_acc={}
            no_of_nodes_acc={}

            c=0
            nc=0
            total_seconds=0
            for a in answers:
                
                map_solution=a['map_solution']
                an_obtained=a['an_obtained']
                duration=a['duration']
                eval_d=a['eval_d']
                name=eval_d['name']
                type_=eval_d['Type_']
                Crossed_edges=eval_d['Crossed_edges']
          
                source_adj=eval_d['source_adj']

                no_of_edges= list(itertools.chain.from_iterable(source_adj))
                no_of_edges=sum(no_of_edges)
                no_of_nodes=len(source_adj[0])
                no_of_edges=str(no_of_edges)
                no_of_nodes=str(no_of_nodes)
                # print('source_adj',source_adj)
                # print('no_of_edges',no_of_edges)


                

          
          
                total_seconds=total_seconds+duration
                if map_solution==an_obtained:
                    c=c+1
                    if type_ in direct_indirect.keys():
                        direct_indirect[type_]['c']=direct_indirect[type_]['c']+1
                        #print('direct_indirect[type_]',direct_indirect[type_])
                        direct_indirect[type_]['duration']+=duration
                    else:
                        direct_indirect[type_]={'c':0,'nc':0,'duration':duration}
                        direct_indirect[type_]['c']=direct_indirect[type_]['c']+1
                    ########
                    if Crossed_edges in Crossed_not_crossed.keys():
                        Crossed_not_crossed[Crossed_edges]['c']=Crossed_not_crossed[Crossed_edges]['c']+1
                        Crossed_not_crossed[Crossed_edges]['duration']+=duration
                    else:
                        Crossed_not_crossed[Crossed_edges]={'c':0,'nc':0,'duration':duration}
                        Crossed_not_crossed[Crossed_edges]['c']=Crossed_not_crossed[Crossed_edges]['c']+1
                    ##################
                    if no_of_edges in no_of_edges_acc.keys():
                        no_of_edges_acc[no_of_edges]['c']+=1
                        no_of_edges_acc[no_of_edges]['duration']+=duration
                    else:
                        no_of_edges_acc[no_of_edges]={'c':0,'nc':0,'duration':duration}
                        no_of_edges_acc[no_of_edges]['c']+=1
                        no_of_edges_acc[no_of_edges]['duration']=duration
                    ##
                    if no_of_nodes in no_of_nodes_acc.keys():
                        no_of_nodes_acc[no_of_nodes]['c']+=1
                        no_of_nodes_acc[no_of_nodes]['duration']+=duration
                    else:
                        no_of_nodes_acc[no_of_nodes]={'c':0,'nc':0,'duration':duration}
                        no_of_nodes_acc[no_of_nodes]['c']+=1
                else:
                    nc=nc+1
                    if type_ in direct_indirect.keys():
                        direct_indirect[type_]['nc']=direct_indirect[type_]['nc']+1
                        direct_indirect[type_]['duration']=+duration
                    else:
                        direct_indirect[type_]={'c':0,'nc':0,'duration':duration}
                        direct_indirect[type_]['nc']=direct_indirect[type_]['nc']+1
                    ########
                    if Crossed_edges in Crossed_not_crossed.keys():
                        Crossed_not_crossed[Crossed_edges]['nc']=Crossed_not_crossed[Crossed_edges]['nc']+1
                        Crossed_not_crossed[Crossed_edges]['duration']+=duration
                    else:
                        Crossed_not_crossed[Crossed_edges]={'c':0,'nc':0,'duration':duration}
                        Crossed_not_crossed[Crossed_edges]['nc']=Crossed_not_crossed[Crossed_edges]['nc']+1
                    ##################
                    ##################
                    if no_of_edges in no_of_edges_acc.keys():
                        no_of_edges_acc[no_of_edges]['nc']+=1
                        no_of_edges_acc[no_of_edges]['duration']=duration
                    else:
                        no_of_edges_acc[no_of_edges]={'c':0,'nc':0,'duration':duration}
                        no_of_edges_acc[no_of_edges]['nc']+=1
                    ##
                    if no_of_nodes in no_of_nodes_acc.keys():
                        no_of_nodes_acc[no_of_nodes]['nc']+=1
                        no_of_nodes_acc[no_of_nodes]['duration']+=duration
                    else:
                        no_of_nodes_acc[no_of_nodes]={'c':0,'nc':0,'duration':duration}
                        no_of_nodes_acc[no_of_nodes]['nc']+=1
            print('c',c)
            print('nc',nc)
            print('total_minutes',total_seconds/60)

            ###
            for k in no_of_edges_acc.keys():
                c=no_of_edges_acc[k]['c']
                nc=no_of_edges_acc[k]['nc']
                acc=c/(c+nc)
                no_of_edges_acc[k]['ac']=acc

            for k in no_of_nodes_acc.keys():
                c=no_of_nodes_acc[k]['c']
                nc=no_of_nodes_acc[k]['nc']
                acc=c/(c+nc)
                no_of_nodes_acc[k]['ac']=acc


            print('+++')
            print('direct_indirect',direct_indirect)
            print('Crossed_not_crossed',Crossed_not_crossed)
            print('no_of_edges_acc',no_of_edges_acc)
            print('no_of_nodes_acc',no_of_nodes_acc)
            ###
            selected_model=selected_model['model']
            for k in direct_indirect.keys():
                data=direct_indirect[k]
                duration=data['duration']/(data['c']+data['nc'])
                acc=data['c']/(data['c']+data['nc'])
                if acc==0:
                    acc=.1
                if k=='mixed':
                    continue
                direct_indirect_all.append([selected_model,k,acc,duration])
            ##
            for k in Crossed_not_crossed.keys():
                data=Crossed_not_crossed[k]
                acc=data['c']/(data['c']+data['nc'])
                duration=data['duration']/(data['c']+data['nc'])
                if acc==0:
                    acc=.1
                if k=='no':
                    k='False'
                Crossed_not_crossed_all.append([selected_model,k,acc,duration])
            ##
            for k in no_of_edges_acc.keys():
                data=no_of_edges_acc[k]
                acc=data['c']/(data['c']+data['nc'])
                duration=data['duration']/(data['c']+data['nc'])
                if acc==0:
                    acc=.1
                no_of_edges_acc_all.append([selected_model,k,acc,duration])
            ##
            ##
            for k in no_of_nodes_acc.keys():
                data=no_of_nodes_acc[k]
                duration=data['duration']/(data['c']+data['nc'])
                acc=data['c']/(data['c']+data['nc'])
                if acc==0:
                    acc=.1
                no_of_nodes_acc_all.append([selected_model,k,acc,duration])


    return direct_indirect_all,Crossed_not_crossed_all,no_of_edges_acc_all,no_of_nodes_acc_all



         






if __name__ == "__main__":
    # python main.py  --task train/eval/preprocess/collect --version
    args=get_args()
    task=args.task

    existing=args.existing
    cross=args.cross
    version=args.version

    if task=='ask':
        generate_questions(task,version,print_existing_id=existing,corss=cross)
    elif task=='eval':
        eval_answer()



###