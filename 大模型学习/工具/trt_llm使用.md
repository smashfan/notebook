

1. 准备阶段：如何查看已经安装了docker>19.3，

2. 由于现在还没有现成的TensorRT-LLM docker镜像，需要自己编译docker镜像，可参考该[文档](https://github.com/NVIDIA/TensorRT-LLM/blob/release/0.5.0/docs/source/installation.md)，也可以直接用下面的命令直接编译（已有编译好的镜像可以跳过该步骤）。

   ```
   # 拉取TensorRT-LLM仓库
   git clone https://github.com/NVIDIA/TensorRT-LLM.git
   cd TensorRT-LLM
   git submodule update --init --recursive
   git lfs install
   git lfs pull
   
   # 编译docker
   cd TensorRT-LLM/docker
   make release_build
   
   # 然后返回到项目路径
   cd ../..
   ```

   

3. 进入项目目录，然后创建并启动容器，同时将本地`qwen`代码路径映射到`/app/tensorrt_llm/examples/qwen`路径，然后打开8000和7860端口的映射，方便调试api和web界面。

   ```
   docker run --gpus all \
     --name trt_llm \
     -d \
     --ipc=host \
     --ulimit memlock=-1 \
     --restart=always \
     --ulimit stack=67108864 \
     -p 8000:8000 \
     -p 7860:7860 \
     -v ${PWD}/qwen:/app/tensorrt_llm/examples/qwen \
     tensorrt_llm/release sleep 8640000
   ```


```
docker tag fjq:v1 registry.cn-hangzhou.aliyuncs.com/smashfan/smashtest:v1
docker push registry.cn-hangzhou.aliyuncs.com/smashfan/smashtest:[镜像版本号]
```

1. 下载模型`QWen-7B-Chat`模型（可以参考总述部分），然后将文件夹重命名为`qwen_7b_chat`，最后放到`qwen/`路径下即可。

2. 进入docker容器里面的qwen路径，安装提供的Python依赖

   ```
   docker exec -it trt_llm /bin/bash
   cd /app/tensorrt_llm/examples/qwen/
       pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

   

3. 将Huggingface格式的数据转成FT(FastTransformer)需要的数据格式（非必选，不convert直接build也是可以的，两种方式都兼容，直接build更省空间，但是不支持smooth quant; 运行该代码默认是需要加载cuda版huggingface模型再转换，所以低于24G显存的显卡建议跳过这步。）

   ```
   python3 hf_qwen_convert.py
   ```

   

4. 修改编译参数（可选）

   - 默认编译参数，包括batch_size, max_input_len, max_new_tokens, seq_length都存放在`default_config.py`中
   - 对于24G显存用户，直接编译即可，默认是fp16数据类型，max_batch_size=2
   - 对于低显存用户，可以降低max_batch_size=1，或者继续降低max_input_len, max_new_tokens

5. 开始编译。

   - 对于24G显存用户，可以直接编译fp16。

   ```
   python3 build.py
   ```

   

   - 对于16G显存用户，可以试试int8 (weight only)。

   ```
   python3 build.py --use_weight_only --weight_only_precision=int8
   ```

   

   - 对于12G显存用户，可以试试int4 (weight only)

   ```
   python3 build.py --use_weight_only --weight_only_precision=int4
   ```

   

6. 试运行（可选）编译完后，再试跑一下，输出`Output: "您好，我是来自达摩院的大规模语言模型，我叫通义千问。<|im_end|>"`这说明成功。

   ```
   python3 run.py
   ```

   

7. 验证模型精度（可选）。可以试试跑一下`summarize.py`，对比一下huggingface和trt-llm的rouge得分。对于`网络不好`的用户，可以从网盘下载数据集，然后按照使用说明操作即可。

   - 百度网盘：链接: https://pan.baidu.com/s/1UQ01fBBELesQLMF4gP0vcg?pwd=b62q 提取码: b62q
   - 谷歌云盘：https://drive.google.com/drive/folders/1YrSv1NNhqihPhCh6JYcz7aAR5DAuO5gU?usp=sharing
   - 跑hugggingface版

   ```
   python3 summarize.py --backend=hf
   
   
   ```

   

   - 跑trt-llm版

   ```
   python3 summarize.py --backend=trt_llm
   ```

   

   - 注：如果用了网盘的数据集，解压后加载就需要多两个环境变量了，运行示范如下：

   ```
   HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 summarize.py --backend=hf
   或者
   HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python3 summarize.py --backend=trt_llm
   ```

   

   - 一般来说，如果trt-llm的rouge分数和huggingface差不多，略低一些（1以内）或者略高一些（2以内），则说明精度基本对齐。

8. 测量模型吞吐速度和生成速度（可选）。需要下载`ShareGPT_V3_unfiltered_cleaned_split.json`这个文件。

   - 可以通过wget/浏览器直接下载，[下载链接](https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered/resolve/main/ShareGPT_V3_unfiltered_cleaned_split.json)
   - 也可通过百度网盘下载，链接: https://pan.baidu.com/s/12rot0Lc0hc9oCb7GxBS6Ng?pwd=jps5 提取码: jps5
   - 下载后同样放到`examples/qwen/`路径下即可
   - 测量前，如果需要改max_input_length/max_new_tokens，可以直接改`default_config.py`即可。一般不推荐修改，如果修改了这个，则需要重新编译一次trt-llm，保证两者输入数据集长度统一。
   - 测量huggingface模型

   ```
   python3 benchmark.py --backend=hf --dataset=ShareGPT_V3_unfiltered_cleaned_split.json --hf_max_batch_size=1
   
   A6000-hf单卡测试速度：Throughput: 0.20 requests/s, 101.28 tokens/s
   ```

   

   - 测量trt-llm模型 (注意：`--trt_max_batch_size`不应该超过build时候定义的最大batch_size，否则会出现内存错误。)

   ```
   python3 benchmark.py --backend=trt_llm --dataset=ShareGPT_V3_unfiltered_cleaned_split.json --trt_max_batch_size=1
   
   A6000-trt_llm单卡测试速度：Throughput: 0.28 requests/s, 136.11 tokens/s
   ```

   

9. 尝试终端对话（可选）。运行下面的命令，然后输入你的问题，直接回车即可。

   ```
   python3 cli_chat.py
   ```

   

10. 部署api，并调用api进行对话（可选）。

    - 部署api

    ```
    python3 api.py
    ```

    

    - 另开一个终端，进入`qwen/client`目录，里面有4个文件，分别代表不同的调用方式。
    - `async_client.py`，通过异步的方式调用api，通过SSE协议来支持流式输出。
    - `normal_client.py`，通过同步的方式调用api，为常规的HTTP协议，Post请求，不支持流式输出，请求一次需要等模型生成完所有文字后，才能返回。
    - `openai_normal_client.py`，通过`openai`模块直接调用自己部署的api，该示例为非流式调用，请求一次需要等模型生成完所有文字后，才能返回。。
    - `openai_stream_client.py`，通过`openai`模块直接调用自己部署的api，该示例为流式调用。
    - 

11. 尝试网页对话（可选，需要先部署api）。运行下面的命令，然后打开本地浏览器，访问：[http://127.0.0.1:7860](http://127.0.0.1:7860/) 即可

    ```
    python3 web_demo.py
    ```

    

    - 默认配置的web_demo.py如下：

    ```
    demo.queue().launch(share=False, inbrowser=True)
    ```

    

    - 如果是服务器运行，建议改成这样

    ```
    demo.queue().launch(server_name="0.0.0.0", share=False, inbrowser=False) 
    ```

    

    - web_demo参数说明
      - `share=True`: 代表将网站穿透到公网，会自动用一个随机的临时公网域名，有效期3天，不过这个选项可能不太安全，有可能造成服务器被攻击，不建议打开。
      - `inbrowser=True`: 部署服务后，自动打开浏览器，如果是本机，可以打开。如果是服务器，不建议打开，因为服务器也没有谷歌浏览器给你打开。
      - `server_name="0.0.0.0"`: 允许任意ip访问，适合服务器，然后你只需要输入`http://[你的ip]: 7860`就能看到网页了，如果不开这个选择，默认只能部署的那台机器才能访问。
      - `share=False`：仅局域网/或者公网ip访问，不会生成公网域名。
      - `inbrowser=False`： 部署后不打开浏览器，适合服务器。







#### 大模型chat版本中的解码器（Qwen）：

他会有前面的提示词和后面的提示词和role：

```
<|im_start|>system You are a helpful assistant.<|im_end|> <|im_start|>user 你是谁<|im_end|> <|im_start|>assistant 
```

输出的时候就按照字符数长度截断

```python
trim_decode_tokens = *tokenizer*.decode(*tokens*[:eod_token_idx], *errors*=*errors*)[*raw_text_len*:]

eos_token_id=151643
```

