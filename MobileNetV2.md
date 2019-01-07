# MobileNetV2 倒置残差和线性瓶颈  

[参考博客](https://blog.csdn.net/u011995719/article/details/79135818)  
[论文地址](https://arxiv.org/pdf/1801.04381.pdf)  

[toc]  

## 摘要  

&emsp;&emsp;在本文中，我们描述了一种新的移动网络结构MobileNetV2，它提高了移动网络在多类型任务和基准以及不同网络尺寸范围的最佳性能。我们还介绍了一种有效地使用轻量级网络进行目标检测的新颖架构SSDLite。并且我们将Deeplabv3进行修剪后构建出一种用于移动语义分割的模型，称为Mobile Deeplabv3。  
&emsp;&emsp;MobileNetV2基于倒置残差结构，并且在窄boottleneck层中有快捷连接。中间的扩大层使用轻量级的深度卷积来过滤特征作为非线性的来源。另外，我们发现在窄层中去除非线性来保持表现能力是很重要的，我们证明了这可以提高性能并且直观地启发了我们网络的设计。  
&emsp;&emsp;最后，我们的方法允许输入/输出域与转换的表达性分离，这为进一步分析提供了方便的框架。我们测量我们在ImageNet分类，COCO物体检测，VOC图像分割上的表现。我们评估准确性与乘法加法（MAdd）测量的操作次数，实际延迟和参数数量之间的权衡。  

## 1.介绍  

&emsp;&emsp;神经网络在机器智能领域有革命性地作用，比如在图像识别任务中超过了人类的识别准确率。然而，提高准确率的同时带来了新的代价：先进的网络需要的高计算能力超越了许多手机和嵌入式应用计算能力。  
&emsp;&emsp;本文介绍了一种新的为移动和资源受限环境特殊定制的神经网络结构。我们的网络在保持相同准确率的情况下通过减少计算量和内存需求，推动了移动定制计算机视觉模型的水平。  
&emsp;&emsp;我们主要贡献是一种新的层模块：具有线性瓶颈的倒置残差。这个模块采用了一种低维的压缩表示作为输入，首先扩展成高维然后使用轻量级深度卷积过滤。随后使用线性卷积将特征投影回低维表示。官方实现TensorFlow-Slim提供一部分操作。  
&emsp;&emsp;该模块可以在任何现代框架中使用标准操作有效地实现，并允许我们的模型使用标准基准测试在多个性能点上击败最新技术。此外，这种卷积模块特别适用于移动设计，因为它可以通过永远不会完全实现大型中间张量来显着减少推理期间所需的内存占用。这减少了许多嵌入式硬件设计中对主存储器访问的需求，这些设计提供了少量非常快速的软件控制的高速缓冲存储器。  

## 2.实际工作  

&emsp;&emsp;在最近几年，调整深度神经网络的架构以在准确率和性能之间有一个最佳平衡成为一个积极研究的领域。早期的网络如AlexNet,VGGNet,GoogLeNet以及ResNet，这些网络的设计都进行了大量的手工体系结构搜索和训练算法改进。最近在网络架构探索上有了很多进展，比如超参数还有各种网络修剪方法以及连通性学习。大量的工作也致力于内部卷积模块的连接架构的改变，比如ShuffleNet[20]或引入了稀疏性[21]和其它[22]。  
&emsp;&emsp;最近，[23, 24, 25, 26]引入了架构探索的新方向，将遗传算法和强化学习加入了其中。然而一个缺点是得到的网络最终会十分复杂。本文的目的是找到然后是神经网络更好地运作并用它指导最简单的网络设计。我们的方法应该被视为[23]描述方法的一种互补和相近的工作。在这种情况下，我们的方法类似于[20,22]所采用的方法并允许进一步改善性能，同时提供内部操作的一部分。我们的网络设计基于MobileNetV1。保留了它的简洁性而且不要求任何特殊操作就能显著提升准确率，实现了移动应用的多图像分类和检测任务的最新技术。  

## 3.预备、讨论和直觉  

### 3.1.深度可分离卷积  

&emsp;&emsp;深度可分离卷积是现在很多高效神经网络模块的关键部分，并且我们也将其应用到我们的网络中。基础思想是使用分解的版本代替全卷积层，将全卷积层分为深度卷积和点卷积两个部分。第一次深度卷积是使用单个卷积滤波器在每个输入通道上进行轻量级滤波。第二次点卷积使用1x1的卷积主要负责通过计算输入通道的线性组合来建立新的特征。  
&emsp;&emsp;标准卷积在输入通道为$d_{i}$输出通道为$d_{j}$，卷积和大小为$k*k$的情况下计算量为$h*w*d_{i}*d_{j}*k^2$。深度可分离卷积的计算量为$$h*w*d_{i}*(k^2+d_{j})(1)$$，实验证实深度可分离卷积在性能上与常规卷积几乎相同，但计算量大致变为原来的$1/k^2$。我们使用的k为3。  

### 3.2.线性瓶颈  

@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Figure1.png"  
![Figure1](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobielNetV2_Figure1.png)  
&emsp;&emsp;思考一个深度神经网络由n层组成$L_{i}$，每个$L_{i}$有$h_{i}*w_{i}*d_{i}$激活张量。这节我们讨论这些张量的基础特性，我们将这些张量视为$h_{i}*w_{i}$个像素点的$d_{i}$维的容器。非正式地，对于一个真实图片的输入集合，我们说激活层集合组成了“多方面兴趣”。长期以来，人们一直以为神经网络的多方面兴趣可以嵌入到低维的子空间中。换句话说，当我们查看深度卷积层的所有单个d通道像素时，在这些值中编码的信息实际上位于某些流形中，而这些流形又可嵌入到低维子空间中。  
&emsp;&emsp;乍一看，这些事实可以简单地通过减少层的尺寸来捕获和利用从而减少操作空间的尺寸。这在MobileNetV1中成功地通过宽度乘数有效地平衡计算量和准确率。遵循这种直觉，这种宽度乘数方法允许人们减少激活空间的尺寸，直到感兴趣的流体经过整个空间。然而，当我们回想深度卷积网络实际上在每次坐标变换时都有非线性时比如ReLU，这种直觉会崩溃。例如，应用于1D空间中的线的ReLU产生“射线”，与在Rn空间中一样，它通常产生具有n关节的分段线性曲线。  
@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Figure2.png"  
![Figure2](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Figure2.png)  
&emsp;&emsp;很容易看出，在通常情况下，ReLU转换层的结果有非零的体积S，通过对输入进行线性转换B获得测绘内部S的点，这意味部分对应于全维输出的输入空间受限于线性变换。换句话说，<font color=#ff000 size=3>深度网络仅仅在非零部分具有线性分类器的能力。</font>  
&emsp;&emsp;在另一方面<font color=#ff000 size=3>当ReLU合并通道时，必然会损失通道信息。</font>但是我们如果有很多通道，并且激活流形中有一个机构，那么信息可能会保留在其它通道中。在附录中，我们展示了如果输入流形能够被嵌入到激活空间的显著低维子空间中，之后ReLU变换会保留信息同时在可表达功能集中引入所需的复杂性。  
&emsp;&emsp;总而言之，我们强调了两个属性，这两个属性表明感兴趣的流形应位于高纬度激活空间的低纬度子空间：  

* 1.如果感兴趣的流形在ReLU变换后保持了非零量，与线性变换相同。  

* 2.ReLU在保留输入流形的全部信息是十分重要的，但是仅在输入流形位于输入空间的低维子空间时有效。  

&emsp;&emsp;这两个见解为我们提供了优化存在的神经网络结构的经验暗示：假如感兴趣的流形是低维的，我们能够在卷积模块中插入线性瓶颈来捕获它。通过实验证明，<font color=#ff000 size=3>线性模块是十分重要的，因为它阻止非线性破坏太多信息。</font>在第六节中， 在第6节中，我们凭经验证明，在瓶颈中使用非线性层确实会使性能受到几个百分点的影响，从而进一步验证了我们的假设3。 我们注意到在[29]中报告了有助于非线性的类似报告，其中从传统残差块的输入中去除了非线性并且导致CIFAR数据集的性能提高。  
&emsp;&emsp;对于本文的其余部分，我们将利用瓶颈卷积。 我们将输入瓶颈尺寸与内部尺寸之间的比率称为膨胀比。  

### 3.3.残差倒置  

@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Figure3.png"  
![Figure3](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Figure3.png)  
&emsp;&emsp;瓶颈网络和残差块十分相似，其中每个块包含一个输入，之后是几个瓶颈，然后是扩展。然而，受到瓶颈模块实际上包含所有必要信息的直观启发，虽然扩展层仅仅作为伴随张量的非线性变换的实现细节，但我们在瓶颈之间直接使用快捷方式。  
&emsp;&emsp;图3提供了设计差异的示意图。 插入快捷方式的动机类似于经典残差连接的动机：我们希望提高梯度在乘数层上传播的能力。 然而，倒置设计的内存效率要高得多（详见第5节），并且在我们的实验中效果稍好一些。  
@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Table1.png"  
![Table1](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Table1.png)  
&emsp;&emsp;瓶颈卷积的运行时间和参数数量。基本结构如表一所示。对于大型为$h*w$的块，扩展因子为t，内核大小为k，输入通道为$d^{'}$输出通道为$d^{''}$，矩阵乘法计算总量为$$h*w*d^{'}*t(d^{'}+k^{2}+d^{''})$$与（1）相比多了额外的项,因为我们确实有一个额外的1×1卷积，但是我们网络的性质允许我们使用更小的输入和输出维度。 在表3中，我们比较了MobileNetV1，MobileNetV2和ShuffleNet之间每个分辨率所需的大小。  

### 3.4.信息流动的说明  

&emsp;&emsp;我们的架构有个很有趣的特性：它能够对构建块（瓶颈块）的输入输出域进行自然分离，这是一种将输入转换为输出的非线性函数。前者可以看出每层网络的容量，后者可以看做是表现能力。这与传统的卷积模块存在差异，包括常规网络和分离网络，它们的容量和表现力混在一起并且是输出层深度的函数。  
&emsp;&emsp;特别是，在我们的例子中，当内层深度为0时，由于快捷连接，底层卷积是身份函数。当膨胀比小于1时，这是一个经典的残余卷积块[8,30]。但是，出于我们的目的，我们表明膨胀率大于1是最有用的。  
&emsp;&emsp;这种解释使我们能够将网络的表现力与其容量分开研究，并且我们认为有必要进一步探索这种分离，以便更好地理解网络属性。  

## 4.网络结构  

@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Table2.png"  
![Table2](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Table2.png)  
&emsp;&emsp;现在描述我们的网络细节。如前面所述的基础模块是带有残差模块的深度可分离卷积。模块细节在表一。MobileNetV2的结构包括32层滤波器，如表二所示结构，有19层residual bottleneck(17?)。我们使用ReLU6做非线性计算，因为它在低精度运算上有很好的鲁棒性。我们使用3x3的卷积核，并且使用dropout和batch normalization。  
&emsp;&emsp;除第一层外，我们在整个网络中使用恒定的扩展速率。在我们的实验中，我们发现5到10之间的扩展速率导致几乎相同的性能曲线，较小的网络通过略小的扩展速率获得更好的结果，而较大的网络具有稍微更好的性能和更大的扩展速率。  
&emsp;&emsp;对于我们所有的主要实验，我们使用应用于输入张量大小的扩展因子6。例如，对于采用64通道输入张量并产生具有128个通道的张量的瓶颈层，中间扩展层则为64·6 = 384个通道。  
&emsp;&emsp;平衡超参数：我们通过使用输入图像分辨率和宽度乘数作为可调超参数来定制我们的架构到不同的性能点，可以根据所需的精度/性能权衡进行调整。 我们的主要网络（宽度乘数1,224×224）具有3亿乘法的计算成本，并使用340万个参数。我们探索性能权衡，输入分辨率从96到224，宽度乘数从0.35到1.4。网络计算成本范围从7M MAdds到585M MAdds，而模型大小在1.7M和6.9M参数之间变化。
&emsp;&emsp;一个小的实现差异，[27]是对于小于1的乘数，我们将宽度乘数应用于除最后一个卷积层之外的所有层。这可以提高较小网络的性能。  

## 5.实验记录  

### 5.1.存取效率推断  

@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Figure4.png"  
![Figure4](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Figure4.png)  
&emsp;&emsp;内存的大小由瓶颈张量的大小决定，而不是瓶颈内部张量的大小决定的（并且更大）。  
&emsp;&emsp;我们的瓶颈残差模块先扩展后压缩。  

@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Figure5.png"  
![Figure5](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Figure5.png)  

@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Figure6.png"  
![Figure6](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Figure6.png)  

## 6.实验

### 6.1.ImageNet分类  

&emsp;&emsp;训练设置：我们使用TensorFlow训练我们的模型[31]。 我们使用标准的RMSPropOptimizer，将衰减和动量设置为0.9。我们在每一层之后使用批量标准化，标准重量衰减设置为0.00004。在MobileNetV1 [27]设置之后，我们使用0.045的初始学习率和每个时期0.98的学习率衰减率。我们使用16个GPU异步工作器，批量大小为96。  

&emsp;&emsp;结果:我们将我们的网络与MobileNetV1，ShuffleNet和NASNet-A模型进行比较。表4显示了一些选定模型的统计数据，其完整性能图如图5所示。  
@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Table4.png"  
![Table4](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Table4.png)  

### 6.2.目标检测  

&emsp;&emsp;我们评估和比较MobileNetV1和MobileNetV2在SSD在COCO数据集上中特征提取的性能，我们也比较了YOLOv2和单个SSD作为基准。  
&emsp;&emsp;SSDLite：我们将SSD的预测层的常规卷积全部替换为深度分离卷积，这种模型适用于移动设备，称为SSDlite，SSDlite显著地减少了计算量和参数，如表5所示。表6显示了所有的计算结果。  
@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Table5.png"  
![Table5](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Table5.png)  

@import "E:\GitHub\Interview-question-collection\picture\MobileNetV2_Table6.png"  
![Table6](https://github.com/holyhond/Interview-question-collection/blob/master/picture/MobileNetV2_Table6.png)  

### 6.3.语义分割  

### 6.4.强化学习  

## 7.讨论和未来工作  