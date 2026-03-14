




import json


# Load environment variables from .env
from dotenv import load_dotenv
from env_utils import doublecheck_env
import os
#from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Check and print results
doublecheck_env("example.env")


# def get_prompt(task,q=None):

#     task=task.replace('bbeh_','')

#     f = open("cot-prompts/"+str(task)+".txt")
#     prompt=f.read()
#     if q!=None:

#         Prompt=f""" Your are a thinker and philosopher who can answer reasoning Qeustions. Make note of the following samples When answering the Questions:

#         - Sample Solutions and thinking examples: 
#         {prompt}

#         - Return only the final answer choice, and thinking step as json

#         """

#         prompt=Prompt + f""" The Question To Answer is : 
#         {q}"""

#         return prompt
#     else:

#         Prompt=f""" Your are a thinker and philosopher who can answer reasoning Qeustions. Make note of the following samples When answering the Questions:

#         - Sample Solutions and thinking examples: 
#         {prompt}

#         - Return only the final answer choice, and thinking step as json

#         """

#         return Prompt


def get_prompt(task,q=None):    

    if q==None:

        Prompt=f""" Your are a thinker and philosopher who can answer reasoning Qeustions.
        Note the followings: 

        - Think step by step

        - Return only the final answer choice, and thinking step as json

        """
    else:
        Prompt=f""" Your are a thinker and philosopher who can answer reasoning Qeustions.
        Note the followings: 

        - Think step by step

        - Return only the final answer choice, and thinking step as json
        - Question :
        {q}

        """

    return Prompt
    



def eval_bbeh(selected_model,q,task,model_source='gwdg' ):
        from openai import OpenAI

        from pydantic import BaseModel
        import ast     
        class Answer(BaseModel):
            answer: str
            thinking: str


        model_source=selected_model['agent']
        print('model_source',model_source)


        if  selected_model['agent'] in ['hf','gwdg']:

            

            SYSTEM_PROMPT=get_prompt(task)
            model=selected_model['model']
            SYSTEM_PROMPT=get_prompt(task)
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


            #q='what is your name? '
            
            response = client.responses.parse(
                model=model,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": q,
                    },
                ],
                text_format=Answer,
            )

            answer_cot = response.output_parsed
            

            # print('answer_cot',answer_cot)
            # exit()
            return answer_cot

            # response = client.responses.parse(
            #     model=model,
            #     input=[
            #         {"role": "system", "content": SYSTEM_PROMPT},
            #         {
            #             "role": "user",
            #             "content": q,
            #         },
            #     ],
            #     text_format=Answer,
            # )

            # answer_cot = response.output_parsed
            

            # print('answer_cot',answer_cot)
            # exit()
            # return answer_cot


            ####################

            # print('****')
    
            # print('answer_cot',answer_cot)
            # print('#########################################################################')
        elif model_source=='DASHSCOPE':
            client = OpenAI(
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                # The following is the base_url for the Singapore region.
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",  
            )

            prompt=get_prompt(task,q)
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
                text_format=Answer,

            )

            response = response.output_parsed
            return response




        elif model_source=='gpt':

            client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
            prompt=get_prompt(task,q)
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
                text_format=Answer,

            )

            response = response.output_parsed
            return response

        elif model_source=='gemini':
            from google import genai
            from pydantic import BaseModel, Field
            from typing import List, Optional




            from google import genai
            import json
            
            client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
            prompt=get_prompt(task,q)
          
   
            response = client.models.generate_content(
                    model=selected_model['model'],#"gemini-3-flash-preview",
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": Answer.model_json_schema(),
                    },
                )

            temp = Answer.model_validate_json(response.text)
            return temp
         

def eval_bbeh_answers():

    file='files/questions_opensource_repeat.json'
    file='files/questions'+'bbeh'+'.json'
    file='files/questions'+'bbeh'+'_5_random.json'
    file='files/questions'+'bbeh'+'_gpt_random.json'
    file='files/questions'+'bbeh'+'_gpt_random2.json'
    file='files/questions'+'bbeh'+'_gpt_random3.json'

    with open(file) as f:
        answers = json.load(f)['data']

    confusion_matrix={}

    for e in answers:
        agent=e['agent']
        selected_model=e['selected_model']
        answer=e['answer']
        thinking=e['thinking']
        target=e['target']
        input_=e['input']
        start=e['start']
        duration=e['duration']
        task=e['task']

        if agent in confusion_matrix.keys():
            if selected_model in confusion_matrix[agent].keys():

                if task in confusion_matrix[agent][selected_model].keys():

                    if answer==target:
                        confusion_matrix[agent][selected_model][task]['c']+=1
                        confusion_matrix[agent][selected_model][task]['duration']+=duration
                    else:
                        confusion_matrix[agent][selected_model][task]['nc']+=1
                        confusion_matrix[agent][selected_model][task]['duration']+=duration


                else:
                    confusion_matrix[agent][selected_model][task]={'c':0,'nc':0,'duration':0}

            else:
                confusion_matrix[agent][selected_model]={}


        else:
            confusion_matrix[agent]={}
            confusion_matrix[agent][selected_model]={}
            confusion_matrix[agent][selected_model][task]={'c':0,'nc':0,'duration':0}
            if answer==target:
                confusion_matrix[agent][selected_model][task]['c']+=1
                confusion_matrix[agent][selected_model][task]['duration']+=duration
            else:
                confusion_matrix[agent][selected_model][task]['nc']+=1
                confusion_matrix[agent][selected_model][task]['duration']+=duration


    for agent in confusion_matrix.keys():
        for model in confusion_matrix[agent].keys():
            for task in confusion_matrix[agent][model]:
                c=confusion_matrix[agent][model][task]['c']
                nc=confusion_matrix[agent][model][task]['nc']
                duration=confusion_matrix[agent][model][task]['duration']

                acc=c/(c+nc) if (c+nc)!=0 else 'zeroexample'
                print('agent',agent)
                print('task',task)
                print('model',model)
                print('acc',acc)
                print('duration',duration/(c+nc+1))
                print('total',c+nc)

                print('******************')


     
                






def eval_answer(flag=False):
    #####
    import itertools
    if flag:
        file='files/questions_'+str(60)+'_crossed.json'
        #file='files/questions'+'repeated'+str(2)+'.json'
        #file='files/questions_opensource_repeat.json'
        #file='files/questions'+'_opensource_repeat_602'+'.json'

        with open(file) as f:
            questions_records = json.load(f)#['Qs']
    
    else:
        file='files/questions'+str(9)+'.json'
        #file='files/questions_opensource_repeat.json'
        
        with open(file) as f:
            questions_records = json.load(f)#['Qs']



    keys=questions_records.keys()
    direct_indirect_all=[]
    Crossed_not_crossed_all=[]
    no_of_edges_acc_all=[]
    no_of_nodes_acc_all=[]
    Speed_All=[]

    Data_all=[]

    for k in keys:
        #print('questions_records[k]',questions_records[k].keys())
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
            # print('##############################')
            # print('data_name',data_name)
            # print('selected_model',selected_model)
            # print('Show_train_set',Show_train_set)
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
                #print('Crossed_edges',Crossed_edges)
          
                source_adj=eval_d['source_adj']


                no_of_edges= list(itertools.chain.from_iterable(source_adj))
                no_of_edges=sum(no_of_edges)
                no_of_edges=str(no_of_edges)

                no_of_nodes=len(source_adj[0])
                no_of_nodes=str(no_of_nodes)

               
            
                correctness=int(map_solution==an_obtained)

                item={\

                'correctness':correctness,
                'duration':duration,
                'type_':type_,
                'Crossed_edges':Crossed_edges,
                'no_of_edges':no_of_edges,
                'no_of_nodes':no_of_nodes,
                'model':selected_model['model'],



                }

                Data_all.append(item)
    return Data_all
   
            

         

