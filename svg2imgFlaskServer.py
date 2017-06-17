# -*- coding:utf-8 -*-
import time
from uuid import uuid1

from flask import Flask, request, jsonify
import cairosvg
import os
from frame.logHelper import LogHelper

app = Flask(__name__, static_folder='web/static')
try:
    app.config.from_object("frame.config")
except:
    print('load config error')
logger = LogHelper().logger


@app.route('/svg2png', methods=['POST'])
def svg_2_png():
    """
    svg_list:[{'name':"svg1","svg_str":"..."},{}]
    :return: jsonArr
    """
    request_json = request.get_json(force=True, silent=True)
    svg_list = request_json.get('svg_list', [])
    result = {"status": "error", "data": ""}
    if svg_list:
        today = time.strftime("%Y-%m-%d")
        basic_path = os.getcwd()
        png_temp_path = os.path.join(basic_path,
                                     'web/static/temp/temp-' + today + '/')
        if not os.path.exists(png_temp_path):
            os.makedirs(png_temp_path)
        for svg_dict in svg_list:
            try:
                uuid = str(uuid1())
                data_bytes = svg_dict.get('svg_str').encode(encoding='utf-8')
                cairosvg.svg2png(bytestring=data_bytes,
                                 write_to=png_temp_path + uuid + ".png")
                svg_dict["url"] = request.host_url + 'static/temp/temp-' + today + '/' + uuid + ".png"
            except:
                logger.exception('current data' + str(svg_dict) + ' .svg2png exception :')
                svg_dict["url"] = ""
        result["data"] = svg_list
        result["status"] = "ok"
    else:
        result['data'] = '参数异常'
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5679, debug=True)
