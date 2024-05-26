### 安装环境

> ubuntu--20.10
>
> GPU--2080ti
>
> cuda--11.0
>
> cudann 8.0.4
>
> paddle 2.2
>
> paddledetection 2.4
>
> ### 安装
>

```
python -m pip install paddlepaddle-gpu==2.2.2.post110 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
```

### 查看环境

> CUDA: nvidia-smi
>
> CUDANN: 
>

### 摔倒检测测试

```
CUDA_VISIBLE_DEVICES=2 python deploy/pphuman/pipeline.py \
    --config deploy/pphuman/config/infer_cfg.yml \
    --model_dir mot=output_inference/mot_ppyoloe_l_36e_pipeline/ kpt=output_inference/dark_hrnet_w32_256x192/ action=output_inference/STGCN \
    --video_file=demo/摔倒.mp4 \
    --enable_action=True \
    --device=gpu
```





### 结果



> mot:  83ms 
>
> kp:154ms