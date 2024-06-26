from flask import Flask, request, flash, make_response
from flask_cors import CORS, cross_origin
import openaikey
import llm
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__) # Initialize the web app
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'gptsm'

PARAGRAPH_SHORTEST = 10
LINE_LENGTH = 89


@app.route('/', methods=['POST', 'OPTIONS'])
@cross_origin()
def connect():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST": # The actual request following the preflight
        return convert_paragraphs(request)

def _build_cors_preflight_response():
    # https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
    response = make_response()
    response.access_control_allow_origin = '*'
    response.access_control_allow_headers = '*'
    response.access_control_allow_headers = '*'
    return response

def convert_paragraphs(request):
    plain_paragraphs = json.loads(request.form.get("payload"))

    styled_paragraphs = []

    l = len(plain_paragraphs)
    for i, p in enumerate(plain_paragraphs):
        logger.info(f"Processing paragraph {i+1}/{l}...")
        p = p.strip()
        
        if len(p) == 0:
            styled_paragraphs.append('')
            continue

        vl0 = ''
        logger.info(p)
        err_cnt = 0
        while(True):
            try:
                for d in llm.get_shortened_paragraph(p, openaikey.key):
                    vl0 += generate_vl0(d['0'], d['1'], d['2'], d['3'], d['4']) + ' '
                logger.info(vl0)
                styled_paragraphs.append(vl0)
                break
            except Exception as e:
                flash(f'An authentication error occurred: openai.error.AuthenticationError: Incorrect API key provided', 'error')
                logger.error(f'Failed to process paragraph {i} :( Retry count={err_cnt}')
                styled_paragraphs.append(p)
                err_cnt += 1
                if(err_cnt >= 3):
                    break        

    data = {'payload': json.dumps(styled_paragraphs)}
    response = make_response(data)
    # response.access_control_allow_origin = '*'
    return response

def is_equal(w1, w2):
    punc = ['.', ',', ':', '?', '!', ';', '"', '(', ')']
    tmp1 = w1
    tmp2 = w2
    if w1[-1] in punc:
        tmp1 = w1[:-1]
    if w2[-1] in punc:
        tmp2 = w2[:-1]
    return (tmp1.lower() == tmp2.lower())


def generate_vl0(l0, l1, l2, l3, l4): # underline
    l0_lst = l0.split()
    l1_lst = l1.split()
    l2_lst = l2.split()
    l3_lst = l3.split()
    l4_lst = l4.split()
    p1 = 0 # pointer
    p2 = 0 # pointer
    p3 = 0 # pointer
    p4 = 0 # pointer
    rst = ''
    for w in l0_lst:
        if p1 < len(l1_lst) and not is_equal(w, l1_lst[p1]):
            rst += ('<span class="gptsm-l0"> ' + w + ' </span> ')
        elif p1 < len(l1_lst) and is_equal(w, l1_lst[p1]):
            p1 += 1
            matched = False
            if p4 < len(l4_lst) and is_equal(w, l4_lst[p4]):
                p4 += 1
                rst += (' ' + w + ' ')
                matched = True
            if p3 < len(l3_lst) and is_equal(w, l3_lst[p3]):
                p3 += 1
                if not matched:
                    rst += ('<span class="gptsm-l3"> ' + w + ' </span> ')
                    matched = True
            if p2 < len(l2_lst) and is_equal(w, l2_lst[p2]):
                p2 += 1
                if not matched:
                    rst += ('<span class="gptsm-l2"> ' + w + ' </span> ')
                    matched = True
            if not matched:
                rst += ('<span class="gptsm-l1"> ' + w + ' </span> ')
        else:
            rst += ('<span class="gptsm-l0"> ' + w + ' </span> ')
    return rst

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True) 