### 

##### 流程梳理

- 初始化各个类模块

- clip_helper.start()

  ​	开启read线程和dispaly

  - read_fn()	
    - 读取和预处理frame
    - 创建task
    - 将task放入read queue	

  - display_fn()

    - 从dispaly队列读取数据display



### 4.6

#### 分析推理流程解读

- class BaseHumanDetector(metaclass=ABCMeta):

  :作为元类,实现pretction过程,将关键帧的bbox放入bboxs里面

- ​	StdetPredictor

  :推理实现过程,bbox,img....

### 4.8

### 修改过程

task  应该添加

- [x] add    human_detections  result

- [x] add_pose_results:加到self.pose_result

- [x] add skeleton_based action predict result

流程添加

human

- [x] all frame det
- [x] all frame pose

- [x] skeleton_based action predic

- [x] baseVisualizer drew part   line:790
- [x] Add  draw frame to   display  queue



初始化

- [x] humandet   已有
- [x] hrnetpose  
- [x] action init  



其他

- [x] processed_frame修改 



修改args



### 4.11

### 调试一下



h,w ,直接去shape[]前面的值



proposal =keyframe 的 bbox



​	shape[0]应该是人数



scrore 调低一点



### 计算各部分所需要的时间 per clip



display 30 帧  1320ms

read 30帧 1561ms



17s

bbox_det: 10246ms

pose_det:4044ms

action_pre:130ms

draw:57ms



### 要找一个快的检测器

faster_rcnn_r50_caffe_fpn_mstrain_1x_coco.py       2.9s



faster_rcnn/faster_rcnn_r50_caffe_fpn_mstrain_1x_coco-person.py  2.7s



faster_rcnn_r50_fpn_1x_coco.py  2.9s





### 尝试yolo

1050ti

[yolo](https://github.com/open-mmlab/mmdetection/tree/master/configs/yolo)/**yolov3_mobilenetv2_mstrain-416_300e_coco.py**  0.033

bbox_det: 2195ms

pose_det:4044ms

action_pre:430ms

draw:56ms



6857 



提前运行7个task就可以了



> 2080ti
>
> bbox:621ms    30帧   
>
> pose_det:2641ms  30帧
>
> 108ms/per
>
> inference :3464ms  
>
> 设备2080ti
>

| 方案                                                    | bbox_predict(ms) | ours  |      |
| ------------------------------------------------------- | ---------------- | ----- | ---- |
| ours(yolov3_mobilenetv2+hrnet_w32_coco_256x192+poseC3D) | 20ms             | 90ms  | 25ms |
| pphuman(PP-YOLOE+HRNet+ST-GCN)                          | 81ms             | 158ms | 15ms |



pphuman

233帧

bbox:15601

kpt:29191



192ms一帧







