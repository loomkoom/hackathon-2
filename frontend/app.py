from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import random
import re
from module import Model

app = Flask(__name__)


def predict(indexOfRow):
    return random.randint(0, 2)

def exportToExcel(name,labeled_data):
    df = pd.DataFrame(labeled_data)
    df.to_excel(name, index=False, columns=['text', 'model_unanimous'])
    
def validate_filename(filename):
    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    if not pattern.match(filename):
        raise Exception("Invalid filename, only alphanumeric characters.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    #print(file.filename)
    
    
    model = Model(pd.read_excel(file))
    dropedData = model.prepare_data() 
    model.train_randomforest()
    ## IMPLEMENT WITH TEAM

    ## add columns to df
    
    size = model.get_size()
    
    
    
    for i in range(size):
        predict = model.predict(i)
        #print("For row ",i," the prediction is ",predict)
        #print(dropedData.at[i,'text'])
        if dropedData.at[i, 'majority_vote'] == "NoMajority":
            model.df.at[i, 'label_1'] = False
            model.df.at[i, 'label_2'] = False
            model.df.at[i, 'label_3'] = False
        if predict == 0:
            model.df.at[i, 'label_1'] = True
            model.df.at[i, 'label_2'] = False
            model.df.at[i, 'label_3'] = False
        elif predict == 1:
            model.df.at[i, 'label_1'] = False
            model.df.at[i, 'label_2'] = True
            model.df.at[i, 'label_3'] = False
        elif predict == 2:
            model.df.at[i, 'label_1'] = False
            model.df.at[i, 'label_2'] = False
            model.df.at[i, 'label_3'] = True
            
        
            
    ## END IMPLEMENT WITH TEAM

    labels = []
    for i in range(size):
        try:
            row_index = i
            label_1 = model.df.at[i, 'label_1']
            label_2 = model.df.at[i, 'label_2']
            label_3 = model.df.at[i, 'label_3']
            proc_text = dropedData.at[i, 'proc_text']
            majority_vote = dropedData.at[i, 'majority_vote']
            
            # Aggiungi i valori alla lista dei labels
            labels.append({
                'row_index': row_index,
                'label_1': label_1,
                'label_2': label_2,
                'label_3': label_3,
                'text': proc_text,
                'majority_vote': majority_vote
            })
        except Exception as e:
            # Se si verifica un errore, aggiungi una voce 'error' alla lista dei labels
            labels.append({
                'error': str(e)
            })
    
    
    return render_template('label.html', data=zip(model.df.iloc[:, 0], labels))


@app.route('/export', methods=['POST'])
def export():
    try:
        labeled_data = []
        filename = request.form['filename']
        validate_filename(filename)
        
        for key, value in request.form.items():
            if "_" in key:
                row_index = int(key.split('_')[0])
                
                if '_label' in key:
                    while len(labeled_data) <= row_index:
                        labeled_data.append({'model_unanimous': '', 'text': ''})
                    labeled_data[row_index]['model_unanimous'] = value
                
                elif '_text' in key:
                    while len(labeled_data) <= row_index:
                        labeled_data.append({'label': '', 'text': ''})
                    labeled_data[row_index]['text'] = value
                    
        
        exportToExcel(filename+".xlsx",labeled_data)
        #return a json with {success: true} or {success: false}
        return {'success': True, 'filename': filename+".xlsx"}
    except Exception as e:
        return {'success': False, 'error': str(e)}


if __name__ == '__main__':
    app.run(debug=True)