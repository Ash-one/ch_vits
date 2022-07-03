# VITS实现的中文TTS
this is a fork of https://github.com/lutianxiong/vits_chinese  
the original version of VITS : https://github.com/jaywalnut310/vits		

VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech		

Espnet连接：github.com/espnet/espnet/tree/master/espnet2/gan_tts/vits

coqui-ai/TTS连接：github.com/coqui-ai/TTS/tree/main/recipes/ljspeech/vits_tts

本项目仅为学习使用  
This project is only for academic purposes

## 基于VITS 实现 48KHZ的 baker TTS 的流程
### 预先准备  
>`apt-get install espeak`  
`pip install -r requirements.txt`  
`cd monotonic_align`  
`python setup.py build_ext --inplace`

### 将标贝标注拷贝到./filelists/
删除2365号和2762号内容，不对中英文混杂进行训练  
或修改2365号和2762内容为如下，此为baker标注错误，并且使用的英文编码无法识别，导致编码失败（本项目不使用这两条数据，会清洗掉）
>002365	这图#2难不成#2是#1P过的#4？
	zhe4 tu2 nan2 bu4 cheng2 shi4 pi1 guo4 de5  

>002762	我是#2善良#1活泼#3、好奇心#1旺盛的#2B型血#4。
	wo3 shi4 shan4 liang2 huo2 po1 hao4 qi2 xin1 wang4 sheng4 de5 bi4 xing2 xie3
### 将标贝音频拷贝到./baker_waves/，启动训练
使用的label为全#0停顿、切分声韵母、无儿化音版  
>`python train.py -c configs/baker_base.json -m baker_base`

一张RTX3090 24G，训练40小时以上

### 推理
修改为对应的模型，进行推理
>`python inference.py`
	



## 可能存在的问题与解决方案：
1. 
>RuntimeError: view_ as_ complex is only supported for float and double tensors, but got a tensor of scalar type: Half  

音频处理时半精度出现的问题，解决方案在[这个issue](https://github.com/jaywalnut310/vits/issues5)

2. 
>RuntimeError: Expected to have finished reduction in the prior iteration before starting a new one. This error indicates that your module has parameters that were not used in producing loss. You can enable unused parameter detection by (1) passing the keyword argument `find_unused_parameters=True` to `torch.nn.parallel.DistributedDataParallel`; (2) making sure all `forward` function outputs participate in calculating loss. If you already have done the above two steps, then the distributed data parallel module wasn't able to locate the output tensors in the return value of your module's `forward` function. Please include the loss function and the structure of the return value of `forward` of your module when reporting this issue (e.g. list, dict, iterable).  

使用DistributedDataParallel函数出现的问题，可在DDP中添加`find_unused_parameters=True`参数，但似乎并不是最优解

3. 
>running build_ext  
copying build/lib.linux-x86_64-3.8/monotonic_align/core.cpython-38-x86_64-linux-gnu.so -> monotonic_align  
error: could not create 'monotonic_align/core.cpython-38-x86_64-linux-gnu.so': No such file or directory

在`monotonic_align`文件夹下再创建一个`monotonic_align`文件夹

4. 本来已经在音素后面强插边界了，VITS又强插边界了，具体是配置参数：`"add_blank": true`

5. 可能影响，随机时长预测，具体配置参数：`use_sdp=True`