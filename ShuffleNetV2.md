# ShuffleNetV2:高效的CNN结构设计实用指南  

[论文地址](https://arxiv.org/pdf/1807.11164.pdf)

[toc]  

## 摘要

&emsp;&emsp;近年来，神经网络的结构设计极大地被间接度量计算复杂度（如FLOPs）导向，直接度量速度还会被其它因素诸如内存存取消耗和平台特性所影响。因此，我们的工作打算计算目标平台的直接度量，而不仅仅考虑间接度量FLOPs。基于一系列的限制性实验，我们的工作获得了一些有效的网络设计的实用指南。相应地，我们提出了ShuffleNet V2这种新的网络结构。进行了全面的消融实验后，我们证实了再速度和准确率进行权衡的情况下，ShuffleNet V2是最先进的。  

## 1.介绍  

@import "E:\GitHub\Interview-question-collection\picture\ShuffNetV2_Figure1.png"  
![Figure1](https://github.com/holyhond/Interview-question-collection/blob/master/picture/ShuffNetV2_Figure1.png)  

&emsp;&emsp;深度神经网络经过最近几年的发展变得更加准确和更加快速。但是在高准确率下计算复杂度这个重要问题被忽略了。实际任务中要求在目标平台（如硬件）和应用场景（如需要低延迟的自动驾驶）这些计算有限制的情况下得到最高的准确率。这激励了一些轻量级网络的研究，并且需要在速度和准确率之间做更好地平衡，此类网络有Xception,MobileNet,MobileNet V2,ShuffleNet和CondenseNet。这些工作中分组卷积和深度卷积有十分重要的作用。  
&emsp;&emsp;计算复杂度采用最广泛的度量是FLOPs。但FLOPs是一个间接度量。它只是一个近似值，而且和我们关注的直接度量如速度或延迟通常情况下是不等的，这种差异已经被许多工作证实。因此，仅仅使用FLOPs作为复杂度度量是不充分的，并且会导致设计的架构不是最优的。  
&emsp;&emsp;导致间接度量（FLOPs）和直接度量（速度）的差异主要有两个。首先FLOPs没有顾忌对速度有影响的几个重要因素。一个因素是内存访问成本，这种成本在某些操作比如分组卷积占有很大一部分运行时间,这可能是大型设备比如GPU的瓶颈。这个成本在网络架构设计的时候不能被忽略。另一个因素是并行度。在相同的FLOPs下，高并行度的网络比低并行度的网络运行更快。