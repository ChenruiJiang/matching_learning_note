# ShuffleNetV2:高效的CNN结构设计实用指南  

[论文地址](https://arxiv.org/pdf/1807.11164.pdf)

[toc]  

## 摘要

&emsp;&emsp;近年来，神经网络的结构设计极大地被间接度量计算复杂度（如FLOPs）导向，直接度量速度还会被其它因素诸如内存存取消耗和平台特性所影响。因此，我们的工作打算计算目标平台的直接度量，而不仅仅考虑间接度量FLOPs。基于一系列的限制性实验，我们的工作获得了一些有效的网络设计的实用指南。相应地，我们提出了ShuffleNet V2这种新的网络结构。进行了全面的消融实验后，我们证实了再速度和准确率进行权衡的情况下，ShuffleNet V2是最先进的。  

## 1.介绍  

@import "E:\GitHub\Interview-question-collection\picture\ShuffleNetV2_Figure1.png"  
![Figure1](https://github.com/holyhond/Interview-question-collection/blob/master/picture/ShuffleNetV2_Figure1.png)  

&emsp;&emsp;深度神经网络经过最近几年的发展变得更加准确和更加快速。但是在高准确率下计算复杂度这个重要问题被忽略了。实际任务中要求在目标平台（如硬件）和应用场景（如需要低延迟的自动驾驶）这些计算有限制的情况下得到最高的准确率。这激励了一些轻量级网络的研究，并且需要在速度和准确率之间做更好地平衡，此类网络有Xception,MobileNet,MobileNet V2,ShuffleNet和CondenseNet。这些工作中分组卷积和深度卷积有十分重要的作用。  
&emsp;&emsp;计算复杂度采用最广泛的度量是FLOPs。但FLOPs是一个间接度量。它只是一个近似值，而且和我们关注的直接度量如速度或延迟通常情况下是不等的，这种差异已经被许多工作证实。因此，仅仅使用FLOPs作为复杂度度量是不充分的，并且会导致设计的架构不是最优的。  
&emsp;&emsp;导致间接度量（FLOPs）和直接度量（速度）的差异主要有两个。首先FLOPs没有顾忌对速度有影响的几个重要因素。<font color=#ff000 size=3>一个因素是内存访问消耗</font>，这种消耗在某些操作比如分组卷积占有很大一部分运行时间,这可能是大型设备比如GPU的瓶颈。这个成本在网络架构设计的时候不能被忽略。另一个因素是并行度。在相同的FLOPs下，高并行度的网络比低并行度的网络运行更快。  
&emsp;&emsp;<font color=#ff000 size=3>另一个因素是相同的FLOPs需要的运行时间不同</font>,这取决于平台。比如，张量分解被广泛地用于早期的加速矩阵乘法运算。但是最近的研究发现分解在减少了75%FLOPs的情况下在GPU上的速度更慢。我们调查发现最新的CUDNN对3x3的卷积会进行特殊优化，并不能确定3x3的卷积一定比9个1x1的卷积速度慢。  
&emsp;&emsp;根据这些观察结果，我们提出了<font color=#ff000 size=3>两个应该被并用于有效网络架构设计的原则</font>。第一，使用直接度量代替简介度量；第二，在目标平台上计算相同的度量。  
&emsp;&emsp;在我们的工作中，我们遵循这两个原则并提出了一个更有效的网络架构。在第二部分，我们首先分析了两个具有代表性的先进网络的运行时间。之后，我们获得了四个有效网络设计的指导方针，这些方针超出了FLOPs
的考虑范围，而且与平台无关。我们使用专门优化的代码在两个平台（GPU和ARM）上做了一系列控制使用去证实他们，确信我们的结果是最先进的。  
&emsp;&emsp;在第三部分，根据指导方针，我们设计了一个新的网络结构。它是ShuffleNet网络的衍生版本，名为ShuffleNet V2。经过第四部分全面的实验后证实ShuffleNet V2在所有的平台上比之前的网络更快更准确。  

## 2.有效网络设计的实际指导方针  

&emsp;&emsp;我们的研究是在两个广泛采用的硬件上对CNN库进行工业级优化。我们注意到我们的CNN库比大部分开源的CNN库更有效，因此，我们确信我们的观察结果和结论是有力的并且在工业中实践是有意义的。  

@import "E:\GitHub\Interview-question-collection\picture\ShuffleNetV2_Figure2.png"  
![Figure2](https://github.com/holyhond/Interview-question-collection/blob/master/picture/ShuffleNetV2_Figure2.png)  
&emsp;&emsp;其它的设置包括：打开所有的优化项（比如：用于减少小运算带来的计算开支的张量融合）。图片的输入尺寸是$224*224$。每个网络进行随机初始并计算100次，采用平均运行时间。  
&emsp;&emsp;在开始我们的工作前，我们先分析了目前两个最先进的网络ShuffleNet V1和MobiileNet V2的运行时间。它们在ImageNet分类任务中都十分有效和准确。并且它们都被低端设备比如手机广泛应用。虽然我们仅分析这两个网络，但这两个网络代表了现在的趋势。它们的核心是分组卷积和深度卷积，这些操作是目前先进网络的重要组成部分，比如ResNeXt,Xception,MobileNet和CondenseNet。  
&emsp;&emsp;综合的运行时间被不同的运算分解，如图2，我们注意到FLOPs度量仅仅计算卷积部分的花费。尽管卷积占所有运算的大部分，但是其它的运算包括数据输入输出，数据混洗以及逐元素运算也占据了大量的时间。<font color=#ff000 size=3>FLOPs不能够精准地评估运算时间。</font>  
&emsp;&emsp;基于这个观察结果，我们从不同的方面对运行时间提出了细节的分析，并且获得了几个有效网络架构设计的指导指南。  

### G1)相同的通道可以最小化内存存取消耗  

&emsp;&emsp;现在的网络通常采用深度分离卷积，在深度分离卷积中，1x1的卷积占据了绝大部分复杂度。我们开始研究1x1卷积。1x1卷积由两个参数来表示，输入通道数$c_{1}$,输出通道数为$c_{2}$。h和w是特征图的长和宽，1x1卷积的FLOPs是$$B=hwc_{1}c_{2}$$  
&emsp;&emsp;为了简化计算，我们假定计算设备足够存储全部的特征图和参数，这样的话，内存存储消耗$$MAC=hw(c_{1}+c_{2})+c_{1}c_{2}$$从均值不等的情况，我们可以得出:$$MAC\geq 2\sqrt{hwB}+\frac{B}{hw}(1)$$  
&emsp;&emsp;从公式（1）可以看出，<font color=#ff000 size=3>MAC的下限被FLOPs捆绑，输入通道数等于输出通道数的时候MAC达到最小。</font>  
&emsp;&emsp;这个结论只是理论上，实际中很多设备的缓存没有假设的那么大，而且现代计算库通常采用复杂的阻塞策略来充分利用缓存机制。因此，真实的MAC值肯能会偏离理论上的值。为了证实我们的结论，我们随后进行了实验，通过重复堆叠10个构建块来构建基准网络，每一个块包括两个卷积层，第一层输入通道为$c_{1}$，输出通道为$c_{2}$，下一层网络与之相反。  
&emsp;&emsp;表1展示了实验结果，当输入输出通道数比值为1：1时，可以看出MAC值会变得更小并且网络计算速度会更快。  
@import "E:\GitHub\Interview-question-collection\picture\ShuffleNetV2_table1.png"  
![Table1](https://github.com/holyhond/Interview-question-collection/blob/master/picture/ShuffleNetV2_table1.png)  

### G2)过大的分组卷积会提高MAC  

&emsp;&emsp;目前分组卷积是很多先进网络的核心部分，它通过将密集卷积的通道分组进行卷积来减少计算复杂度（FLOPs），因此它可以在与传统结构在FLOPs相同的情况下使用更多的通道，进而提升模型的性能。但是，提升的通道数导致了更大的MAC。  
&emsp;&emsp;从（1）的公式进行推导，FLOPs的值$$B=hwc_{1}c_{2}/g$$1x1的分组卷积中MAC和FLOPs的关系为：$$MAC=hw(c_{1}+c_{2})+\frac{c_{1}c_{2}}{g}$$$$=hwc_{1}+\frac{Bg}{c_{1}}+\frac{B}{hw}(2)$$g是分组数。从公式中可以看出，在给定输入尺寸$c_{1}*h*w$和计算量B,MAC的值与g的值正相关。  
&emsp;&emsp;为了研究在实践过程中的有效性，我们堆积了10个逐点组卷积来构建基准网络。表2展示了在相同的FLOPs情况下运行速度的差异。从表中可以清晰地看出分组数对运行速度的影响。对比分组数为1和分组数为8的实验结果可以看出，分组数为8的模型运行速度是分组数为1的一倍，在ARM上的数独也慢了30%。  
@import "E:\Github\Interview-question-collection\picture\ShuffleNetV2_table2.png"  
![Table2](https://github.com/holyhond/Interview-question-collection/blob/master/picture/ShuffleNetV2_table2.png)  
&emsp;&emsp;因此，我们建议分组数应该基于目标平台和任务认真选择。简单地增加分组数愚蠢的，因为这在曾加准确率的同时也会增加计算量，很可能得不偿失。

### 分裂网络会减少并行度  

&emsp;&emsp;在GoogleNet的一系列网络和自动生成网络中，大量采用的了“多径”网络来提高准确率。使用小的操作（分裂网络）来代替一些大网络会带来准确率的提升，但是由于这种操作对大型计算设备如GPU的并行性不是很友好，而且会在内核启动和同步的时候带来额为消耗，因此它会增加计算量。  
&emsp;&emsp;为了量化分裂网络是如何影响效率的，我们使用不同数量的分类网络制作了一系列网络模块进行实验。每个网络模块包含1-4个1x1的卷积，如何将10个这样的模块堆积在一起组成一个网络，然后它们进行顺序运算或者并行运算。进行的实验效果如表3所示。  
@import "E:\Github\Interview-question-collection\picture\ShuffleNetV2_table3.png"  
![Table3](https://github.com/holyhond/Interview-question-collection/blob/master/picture/ShuffleNetV2_table3.png)  
&emsp;&emsp;表3展示了分裂网络显著地降低了GPU的速度，比如4个分裂网络结构的速度只有1个分类网络结构的1/3。在ARM上的减少相对来说很小。  

### 逐像素操作不可忽视  

&emsp;&emsp;