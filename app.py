from flask import Flask
import json

app = Flask(__name__)
print("loading json")
app.config['D'] = json.load(open('dictionary.json', 'r'))
app.config['W'] = {app.config['D']['list'][i] : i for i in range(len(app.config['D']['list']))}
print("loaded")
"""
app.config['D'] = {
        'words': {
            word_dict['list'][i] : word_dict['words'][i] for i in range(len(word_dict['list']))},
        'rhymes': {word_dict['list'][int(k)]: set(word_dict['list'][idx] for idx in v) for k, v in word_dict['rhymes'].items()}
}
"""
print("made it here")

@app.route('/syllables/<word>', methods=['GET'])
def get_num_syllables(word=None):
    return str(app.config['D']['words'][app.config['W'][word]][0]['c'] if word is not None and word in app.config['W'] else 0)

@app.route('/phonemes/<word>', methods=['GET'])
def get_phonemes(word=None):
    return ' '.join(app.config['D']['words'][app.config['W'][word]][0]['p']) if word is not None and word in app.config['W'] else ''

@app.route('/stresses/<word>', methods=['GET'])
def get_stresses(word=None):
    return '' if word is None or word not in app.config['W'] else ''.join(str(int(x)) for x in app.config['D']['words'][app.config['W'][word]][0]['s'])

@app.route('/rhymes/with/<word_1>/<word_2>/', methods=['GET'])
def rhymes_with(word_1=None, word_2=None):
    return str(word_1 is not None and word_2 is not None and word_1 in app.config['W'] and word_2 in list(app.config['D']['list'][x] for x in app.config['D']['rhymes'][str(app.config['W'][word_1])]))

@app.route('/rhymes/<word>', methods=['GET'])
def get_rhymes(word=None):
    return '' if word is None or word not in app.config['W'] else '\n'.join(sorted((app.config['D']['list'][x] for x in app.config['D']['rhymes'][str(app.config['W'][word])]), key=lambda x:app.config['D']['words'][app.config['W'][x]][0]['c']))

if __name__ == '__main__':
	app.run()
