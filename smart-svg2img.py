# -*- coding:utf-8 -*-
import time
from uuid import uuid1

from flask import Flask, request, jsonify
import cairosvg
import os
from frame.logHelper import LogHelper

app = Flask(__name__)
app.config.from_object("frame.config")
logger = LogHelper().logger


@app.route('/svg2png', methods=['POST'])
def hello_world():
    request_json = request.get_json(force=True, silent=True)
    datas = request_json.get('data', [])
    result = {"status": "error", "data": ""}
    if datas:
        today = time.strftime("%Y-%m-%d")
        png_temp_path = os.path.join(app.config.get('SMARTEYE_TEMP_URL'),
                                     'temp/temp-' + today + '/')
        for data in datas:
            if "content" in data:
                try:
                    uuid = str(uuid1())
                    data_bytes = data.get('content').encode(encoding='utf-8')
                    cairosvg.svg2png(bytestring=data_bytes,
                                     write_to=png_temp_path + uuid + ".png")
                    data["url"] = png_temp_path + uuid + ".png"
                except:
                    logger.exception('current data' + str(data) + ' .svg2png exception :')
                    data["url"] = ""
        result["data"] = datas
        result["status"] = "ok"
    else:
        result['data'] = '参数异常'
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=5679, debug=True)
