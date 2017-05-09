'''
Simple web service wrapping a Word2Vec as implemented in Gensim
Example call: curl http://127.0.0.1:5000/wor2vec/n_similarity/ws1=Sushi&ws1=Shop&ws2=Japanese&ws2=Restaurant
@TODO: Add more methods
@TODO: Add command line parameter: path to the trained model
@TODO: Add command line parameters: host and port
'''

from flask import Flask, request, jsonify
from flask.ext.restful import Resource, Api, reqparse
from gensim.models.word2vec import Word2Vec as w
from gensim import utils, matutils
from numpy import exp, dot, zeros, outer, random, dtype, get_include, float32 as REAL,\
     uint32, seterr, array, uint8, vstack, argsort, fromstring, sqrt, newaxis, ndarray, empty, sum as np_sum
import pickle
import argparse
import base64
import sys
import json

parser = reqparse.RequestParser()


def filter_words(words):
    if words is None:
        return
    return [word for word in words if word in model.vocab]


class Add(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('arg1', type=str, required=True, help="arg1 cannot be blank!", action='append')
        parser.add_argument('arg2', type=str, required=True, help="arg2 cannot be blank!", action='append')
        args = parser.parse_args()
        print(str(int(args['arg1'])+int(args['arg2'])))
        return model.add(str(int(args['arg1'])+int(args['arg2'])))


class N_Similarity(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ws1', type=str, required=True, help="Word set 1 cannot be blank!", action='append')
        parser.add_argument('ws2', type=str, required=True, help="Word set 2 cannot be blank!", action='append')
        args = parser.parse_args()
        return model.n_similarity(filter_words(args['ws1']),filter_words(args['ws2']))


class Similarity(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('w1', type=str, required=True, help="Word 1 cannot be blank!")
        parser.add_argument('w2', type=str, required=True, help="Word 2 cannot be blank!")
        args = parser.parse_args()
        return model.similarity(args['w1'], args['w2'])


class MostSimilar(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('positive', type=str, required=False, help="Positive words.", action='append')
        parser.add_argument('negative', type=str, required=False, help="Negative words.", action='append')
        parser.add_argument('topn', type=int, required=False, help="Number of results.")
        args = parser.parse_args()
        pos = filter_words(args.get('positive', []))
        neg = filter_words(args.get('negative', []))
        t = args.get('topn', 10)
        pos = [] if pos == None else pos
        neg = [] if neg == None else neg
        t = 10 if t == None else t
        print("positive: " + str(pos) + " negative: " + str(neg) + " topn: " + str(t))
        try:
            res = model.most_similar_cosmul(positive=pos,negative=neg,topn=t)
            return res
        except Exception:
            print(Exception)
            print(res)


class Model(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('word', type=str, required=True, help="word to query.")
        args = parser.parse_args()
        try:
            res = model[args['word']]
            res = base64.b64encode(res)
            return res
        except Exception:
            print(Exception)
            print(res)

class ModelWordSet(Resource):
    def get(self):
        try:
            res = base64.b64encode(pickle.dumps(set(model.index2word)))
            return res
        except Exception:
            print(Exception)
            print(res)

app = Flask(__name__)
api = Api(app)

@app.errorhandler(404)
def pageNotFound(error):
    return "page not found"

@app.errorhandler(500)
def raiseError(error):
    return error

if __name__ == '__main__':
    global model

    #----------- Parsing Arguments ---------------
    p = argparse.ArgumentParser()
    p.add_argument("--model", help="Path to the trained model", default="/Users/kz/Projects/word2vec-api-master/models/GoogleNews.bin")
    p.add_argument("--binary", help="Specifies the loaded model is binary", default=False)
    p.add_argument("--host", help="Host name (default: http://127.0.0.1)", default='http://127.0.0.1')
    p.add_argument("--port", help="Port (default: 5000)", default=5000)
    p.add_argument("--path", help="Path (default: /math)", default='/math')
    args = p.parse_args()
    #
    # model_path = args.model
    #
    # if not args.model:
    #     print("Usage: word2vec-apy.py --model path/to/the/model [--host host --port 1234]")
    # model = w.load_word2vec_format(args.model, binary=args.binary)
    # api.add_resource(N_Similarity, args.path+'/n_similarity')
    # api.add_resource(Similarity, args.path+'/similarity')
    # api.add_resource(MostSimilar, args.path+'/most_similar')
    # api.add_resource(Model, args.path+'/model')
    api.add_resource(Add, args.path+'/add')
    # api.add_resource(ModelWordSet, '/word2vec/model_word_set')
    app.run(host=args.host, port=args.port)
