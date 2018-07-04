# FP-tree
FPtree python实现


根据[FP Tree算法原理总结](http://www.cnblogs.com/zhengxingpeng/p/6679280.html) 实现的FP Tree
使用起来很简单
```
import FP_tree as fpt

fp_tree = fpt.FPTree(min_support=2)
data = ['ABCEFO','ACG','EI','ACDEG','ACEGL','EJ','ABCEFP','ACD','ACEGM','ACEGN']
# or
#data = [['A', 'B', 'C', 'E', 'F', 'O'],
# ['A', 'C', 'G'],
# ['E', 'I'],
# ['A', 'C', 'D', 'E', 'G'],
# ['A', 'C', 'E', 'G', 'L'],
# ['E', 'J'],
# ['A', 'B', 'C', 'E', 'F', 'P'],
# ['A', 'C', 'D'],
# ['A', 'C', 'E', 'G', 'M'],
# ['A', 'C', 'E', 'G', 'N']]
fp_tree.fit(data)

print(fp_tree.freq_pattern_dict_)
```

