# zjk
chatglm+paddlespeech实现实时对话功能（可在服务器部署）

此项目首先搭建chatglm项目api服务器与paddlespecch项目的流式ASR服务器，流式 TTS服务器，随后通过与这些服务器进行交互实现实时语音对话功能，并可在服务器端部署来实现多人对话。

安装

建议在linux系统下部署，python3.7版本以上
建议使用anaconda将chatglm与paddlespeech在不同conda环境部署（chatglm使用pytorch，paddlespeech使用的是paddle）

paddlespeech服务器部署

相关依赖

    gcc >= 4.8.5
    paddlepaddle >= 2.4.1
    python >= 3.7
    linux(推荐)
gcc安装： 
sudo apt update

sudo apt install build-essential

paddlepaddle安装： pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple （默认安装cpu版）


源码编译

git clone https://github.com/PaddlePaddle/PaddleSpeech.git

cd PaddleSpeech

pip install pytest-runner

pip install .

启动服务器：

启动流式 ASR 服务

paddlespeech_server start --config_file ./demos/streaming_asr_server/conf/application.yaml

启动流式 TTS 服务

paddlespeech_server start --config_file ./demos/streaming_tts_server/conf/tts_online_application.yaml

chatglm的api服务器部署

详情请见https://github.com/THUDM/ChatGLM-6B

由于网上教程很多，我就不赘述了

成功运行chatglm项目内api.py文件即可

在确保chatglm服务器与paddlespeech的ASR，TTS服务器都在正常监听后运行hecheng。py文件即可进行实时对话



详情请见https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/README_cn.md



