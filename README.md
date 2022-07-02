# VITS实现的中文TTS
this is a fork of https://github.com/lutianxiong/vits_chinese  
the original version of VITS : https://github.com/jaywalnut310/vits		

VITS: Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech		

Espnet连接：github.com/espnet/espnet/tree/master/espnet2/gan_tts/vits

coqui-ai/TTS连接：github.com/coqui-ai/TTS/tree/main/recipes/ljspeech/vits_tts

本项目仅为学习使用  
This project is only for academic purposes

## 基于VITS 实现 48KHZ的 baker TTS 的流程

apt-get install espeak

pip install -r requirements.txt

cd monotonic_align

python setup.py build_ext --inplace

## 将标贝音频拷贝到./baker_waves/，启动训练

python train.py -c configs/baker_base.json -m baker_base

一张RTX3090 24G，训练40H以上

## 测试
python vits_strings.py

上面的模型训练出来后存在，明显停顿的问题

原因：	

1，本来已经在音素后面强插边界了，VITS又强插边界了，具体是配置参数："add_blank": true

2，可能影响，随机时长预测，具体配置参数：use_sdp=True

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

在monotonic_align文件夹下再创建一个monotonic_align文件夹