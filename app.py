from flask import Flask
import json

app = Flask(__name__)
word_dict = json.load(open('dictionary.json', 'r'))
app.config['D'] = {
        'words': {
            word_dict['list'][i] : word_dict['words'][i] for i in range(len(word_dict['list']))},
        'rhymes': {word_dict['list'][int(k)]: set(word_dict['list'][idx] for idx in v) for k, v in word_dict['rhymes'].items()}
}

@app.route('/syllables/<word>', methods=['GET'])
def get_num_syllables(word=None):
    return str(app.config['D']['words'][word][0]['c'] if word is not None and word in app.config['D']['words'] else 0)

@app.route('/phonemes/<word>', methods=['GET'])
def get_phonemes(word=None):
    return ' '.join(app.config['D']['words'][word][0]['p']) if word is not None and word in app.config['D']['words'] else ''

@app.route('/stresses/<word>', methods=['GET'])
def get_stresses(word=None):
    return '' if word is None or word not in app.config['D']['words'] else ''.join(str(int(x)) for x in app.config['D']['words'][word][0]['s'])

@app.route('/rhymes/with/<word_1>/<word_2>/', methods=['GET'])
def rhymes_with(word_1=None, word_2=None):
    return str(word_1 is not None and word_2 is not None and word_1 in app.config['D']['rhymes'] and word_2 in app.config['D']['rhymes'][word_2])

@app.route('/rhymes/<word>', methods=['GET'])
def get_rhymes(word=None):
    return '' if word is None or word not in app.config['D']['rhymes'] else '\n'.join(sorted(app.config['D']['rhymes'][word], key=lambda x:app.config['D']['words'][x][0]['c']))
