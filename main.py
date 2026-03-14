



from utils import *
import json
from numpy import random
import datetime

from Eval import *
import datetime
import time
import os

#####
file=file='files/questions'+'_opensource_repeat_60'+'.json'
with open(file) as f:
    questions_records = json.load(f)#['Qs']



#questions_records={}
questions={}

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
        if version=='v2':
            Overwrite_cross=True
 
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

        print('Overwrite_cross',Overwrite_cross)

 

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





deepseek_v3_2_Exp={'agent':'hf','model':"deepseek-ai/DeepSeek-V3.2-Exp:novita"}


deepseek_v3_2={'agent':'hf','model':"deepseek-ai/DeepSeek-V3.2:novita"}

Qwen3_Coder={'agent':'hf','model':"Qwen/Qwen3-Coder-Next:novita"}


Qwen3={'agent':'hf','model':"Qwen/Qwen3-235B-A22B-Instruct-2507:novita"}

Qwen3_235B={'agent':'gwdg','model':"qwen3-32b"}
Qwen3_30b={'agent':'gwdg','model':"qwen3-30b-a3b-thinking-2507"}


qwen3_coder={'agent':'gwdg','model':"qwen3-coder-30b-a3b-instruct"}


mistral={'agent':'gwdg','model':"mistral-large-instruct"}

deepseek_r1={'agent':'gwdg','model':"deepseek-r1"}

deepseek_r1_distill={'agent':'gwdg','model':"deepseek-r1-distill-llama-70b"}


Qwen2_5={'agent':'hf','model':"Qwen/Qwen2.5-7B-Instruct:together"}
Qwen_2={'agent':'hf','model':"Qwen/Qwen2-72B-Instruct:featherless-ai"}


Llama_4={'agent':'hf','model':"meta-llama/Llama-4-Scout-17B-16E-Instruct:groq"}

Llama_3_3={'agent':'hf','model':"meta-llama/Llama-3.3-70B-Instruct:groq"}
# Qwen=Llama_3_3

OpenSource_MODELS=[Llama_4,deepseek_v3_2_Exp,deepseek_v3_2,\
Qwen3,Qwen3_235B,Qwen3_30b,qwen3_coder,mistral,deepseek_r1,deepseek_r1_distill,Qwen2_5,\


]

OpenSource_MODELS=[deepseek_v3_2_Exp,deepseek_v3_2,]

BBEH_Test_Models=[Llama_4,gpt_52,gemini_3_flash_preview,gpt_41_mini,gpt_5_mini,gpt_5_nano,gpt_52,\
gemini_3_pro_preview,gemini_25_flash,gemini_20_flash,\
deepseek_v3_2_Exp,deepseek_v3_2,Qwen3_235B,Qwen2_5]


BBEH_Test_Models=[Qwen2_5,Qwen3_235B,Qwen2_5,Llama_3_3]

BBEH_Test_Models=[deepseek_r1,deepseek_r1_distill,deepseek_v3_2_Exp,deepseek_v3_2,]

BBEH_Test_Models=[deepseek_v3_2_Exp,deepseek_v3_2]


MODELS_Pro=[deepseek_v3_2,gemini_3_flash_preview,gemini_25_pro,gpt_41_mini,gpt_41,gpt_5_mini,gpt_5_nano,gpt_52,\
gemini_20_flash,gemini_25_pro,gemini_25_flash,gemini_3_pro_preview,gemini_3_flash_preview]



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
    l_test=['60',]


    #######################
    corss_=corss
  
    MODELS=OpenSource_MODELS

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
    

        
        Record={'Qs':questions,'data':data,'answers':answers,'data_name':l_test[0],'selected_model':selected_model,'Show_train_set':Show_train_set}

        key=l_test[0]
        corss,version
        cross_temp='crossed' if cross else 'not_crossed'
        if key in questions_records.keys():
            questions_records[key][version][cross_temp][id_No_]=Record
        else:
            questions_records[key]={'original':{'crossed':{},'not_crossed':{}},'v2':{}}
            questions_records[key][version][cross_temp][id_No_]=Record

        file='files/questions'+'_opensource_repeat_602'+'.json'
        with open(file, 'w') as fp:
            json.dump(questions_records, fp)



def read_bbeh(task,model_source='gwdg'):


    # import os
    # from openai import OpenAI

    # client = OpenAI(
    #     base_url="https://router.huggingface.co/v1",
    #     api_key=os.environ["HF_TOKEN"],
    # )

    # completion = client.chat.completions.create(
    #     model="deepseek-ai/DeepSeek-V3.2:novita",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": "What is the capital of France?"
    #         }
    #     ],
    # )

    # print(completion.choices[0].message)
    # exit()
    
    MODELS=BBEH_Test_Models


    Records_Data=[]

    for mi,selected_model in enumerate(MODELS): 
        path = "bbeh-main/benchmark_tasks"
        task_folders = os.listdir(path)
        #print("Directory contents:", task_folders)
        print('selected_model',selected_model)
        for ti, task in enumerate(task_folders):
            print('task',task)


            #continue
            if task=='.DS_Store':
                continue
            task_file_path=path+'/'+str(task)+'/task.json'
            with open(task_file_path) as f:
                task_data = json.load(f)#['Qs']
            print('task_data',task_data.keys())

            examples=task_data['examples']
            canary=task_data['canary']
            #print('canary',canary)
            #print('****')
            random.shuffle(examples)

            examples=examples[:10]
       
            for e in examples:
                # print('task_folders',ti)
                # print('examples',len(examples))
                # print('e.keys',e.keys())
                # print('e',e)
                print('----')
                input_=e['input']
                target=e['target']

                q=input_
          
                start_time = datetime.datetime.now()
                #try:
                answer=eval_bbeh(selected_model,q,task,model_source='gemini' )
                print('answer',answer.answer)

                print('target',target)
                end_time = datetime.datetime.now()
                duration=end_time-start_time
                duration= duration.total_seconds()

                Record={'agent':selected_model['agent'],\
                'selected_model':selected_model['model'],'answer':answer.answer,'thinking':answer.thinking,\
                'target':target,'input':input_,'task':task,'start':str(start_time),'duration':duration}
                Records_Data.append(Record)
                # except:

                #     print('exception occured')
                #     continue
                file='files/questions'+'bbeh'+'_gpt_random3.json'
                Data={'data':Records_Data}
                with open(file, 'w') as fp:
                    json.dump(Data, fp)
                

                #break
        
            file='files/questions'+'bbeh'+'_gpt_random3.json'
            Data={'data':Records_Data}
            with open(file, 'w') as fp:
                json.dump(Data, fp)
        #break
                
 



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
    elif task=='bbeh':
        read_bbeh(task)



        