from django.shortcuts import render
from django.http import HttpResponse, Http404
from transformers import pipeline,AutoTokenizer, AutoModelForSeq2SeqLM
import random
import torch
import pandas as pd

#Trigger Startup immediately.

# Create your views here.
def index(request):
    return render(request, 'index.html')

def start_up():
    #!pip install transformers
    #!pip install torch
    return None

def Query(question):
    return None


def qa(request):
    if request.method == 'POST':
        #answer = "Post Trigered!"
        #return render(request, 'index.html', {'answer': answer})
        #return render(request, 'index.html', {'answer': answer})
        context = str(request.POST.get('question'))
        question_number = int(request.POST.get('question_number'))
        #print(question)
        #answer=question
        df = pd.DataFrame(columns=['Questions', 'Answers'])
        df = Question_Answer(question_number, context, df)

        global Random_name
        #Generate random number for the genrated file.
        Random_name=random.randint(0,200)

        # Get the file path of the generated contract
        df.to_excel(f"{Random_name}.xlsx")
        filepath = f"{Random_name}.xlsx"
        try:
            with open(filepath, 'rb') as excel:
                response = HttpResponse(excel.read(), content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(Random_name)
                return response
        except FileNotFoundError:
            raise Http404("Excel file not found.")
    else:
        answer = "Query Empty!"
        return render(request, 'index.html', {'answer': answer})
    return render(request, 'index.html', {'answer': answer})

#Trigger Startup on launch of web application!
#start_up()

def Question_Answer(Number, context, df):
    generator = pipeline('text2text-generation', model='voidful/context-only-question-generator')
    device = [0 if torch.cuda.is_available() else 'cpu'][0]
    for i in range(Number):
        randi=random.uniform(0, 1.5)
        questions = generator(context,temperature=randi,do_sample=True)
        generated_question = questions[0]['generated_text']
        print(f"Question {i}:{generated_question}")
        generated_answer=Answer_generate(generated_question, context, model="consciousAI/question-answering-generative-t5-v1-base-s-q-c", device=device)
        print(f"Answer {i}:{generated_answer}")
        df = Save_Pandas(df, generated_question, generated_answer)
    return df

def Answer_generate(query, context, model, device):
    
    FT_MODEL = AutoModelForSeq2SeqLM.from_pretrained(model).to(device)
    FT_MODEL_TOKENIZER = AutoTokenizer.from_pretrained(model)
    input_text = "question: " + query + "</s> question_context: " + context
    
    input_tokenized = FT_MODEL_TOKENIZER.encode(input_text, return_tensors='pt', truncation=True, padding='max_length', max_length=1024).to(device)
    _tok_count_assessment = FT_MODEL_TOKENIZER.encode(input_text, return_tensors='pt', truncation=True).to(device)

    summary_ids = FT_MODEL.generate(input_tokenized, 
                                       max_length=30, 
                                       min_length=5, 
                                       num_beams=2,
                                       early_stopping=True,
                                   )
    output = [FT_MODEL_TOKENIZER.decode(id, clean_up_tokenization_spaces=True, skip_special_tokens=True) for id in summary_ids] 
    
    return str(output[0])

def Save_Pandas(df, generated_question, generated_answer):
    if len(df.index) > 0:
        # check if the previous row is not empty
        if not df.iloc[-1].isnull().values.any():
            # add a new row to the dataframe
            df.loc[len(df)] = [generated_question, generated_answer]
    else:
        # if the dataframe is empty, add a new row
        df = pd.DataFrame([[generated_question, generated_answer]], columns=['Questions', 'Answers'])
    return df


if __name__ =="__main__":
    start_up()
    Query("Under PSSCOC, is there anything about contractor defaults?")