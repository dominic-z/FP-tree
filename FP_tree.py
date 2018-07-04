# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 18:28:02 2018

@author: dom-z
"""


class FPTree():
    '''
    FP tree算法
    每个序列内的项不可重复，如果有重复则会视作同一项
    
    args:
        min_support: int 最小支持度
    
    
    attr:
        root_: Node 根节点，item=None，父节点为None
        item_freq_dict_: dict 记录满足最小支持度的频繁项的出现频次 k=item v=出现的frequency
        header_table_: OrderDict 按支持度从大到小存入的有序dict k=item v=None or Node
        transactions_: list 规范化transactions，去除每一个序列中的不频繁项，并将剩余项目按照支持度从大到小排序
        cond_pattern_base_dict_: dict key=item v=条件模式基
        freq_pattern_dict_: dict key=pattern v=freq
    '''
    def __init__(self, min_support):
        self.min_support = min_support

    def fit(self,transactions):
        '''
        args:
            transacions: iterable obj 每一个元素都是可迭代对象，代表一个序列，每个序列内的重复项都会被视作同一项
        '''
        self.__header_init(transactions)
        self.__construct_tree()
        self.__get_frequent_pattern()
        
    def __header_init(self,transactions):
        '''
        item_freq_dict_与header_table_的初始化
        args:
            transacions: iterable obj 每一个元素都是可迭代对象，代表一个序列，每个序列内的重复项都会被视作同一项
        '''
        from collections import OrderedDict
        
        item_frequency_dict = dict()
        for tran in transactions:
            for item in set(tran):
                freq = item_frequency_dict.get(item, 0)
                item_frequency_dict[item] = freq + 1
        
        self.item_frequency_dict_ = dict()
        for k,v in item_frequency_dict.items():
            if v >= self.min_support:
                self.item_frequency_dict_[k] = v

    
        #sorted_item_list为排序标准
        sorted_item_list = sorted(list(self.item_frequency_dict_.keys()),
                                  key=lambda item:self.item_frequency_dict_[item],
                                  reverse=True)
        self.header_table_ = OrderedDict()
        for item in sorted_item_list:
            self.header_table_[item] = None
            
            
        self.transactions_ = list()
        for tran in transactions:
            tran_with_freq_item = [item for item in set(tran) if item in self.item_frequency_dict_]
            self.transactions_.append(sorted(tran_with_freq_item,
                                             key=sorted_item_list.index))
    def __construct_tree(self):
        '''
        构建FP Tree
        '''
        self.root_ = Node('none',None,count=0)
        for transaction in self.transactions_:
            self.__insert_node(transaction,self.root_)
           
            
    def __insert_node(self, transaction, parent):
        '''
        根据当前的transaction为FP tree插入节点
        args:
            transaction: iterabel obj 代表一个序列
            parent_node: Node 当前序列的父节点
        '''
        first_item = transaction[0]
        child = parent.get_child(first_item)
        if child is None:
            child = parent.add_child(first_item)
            
            next_node = self.header_table_[first_item]
            if next_node is None:
                self.header_table_[first_item] = child
            else:
                while not next_node.next_header_node is None:
                    next_node = next_node.next_header_node
                next_node.next_header_node = child
        else:
            child.count += 1
            
        remaining_transaction = transaction[1:]
        if len(remaining_transaction) > 0:
            self.__insert_node(remaining_transaction,child)
            
    
    def __get_frequent_pattern(self):
        '''
        获取频繁模式以及对应的支持度
        '''

        
        cond_pattern_base_dict = dict()
        for item in self.item_frequency_dict_.keys():
            next_node = self.header_table_[item]
            cond_pattern_base = dict()
            while not next_node is None:
                parent = next_node.parent
                while not parent.parent is None:
                    freq = cond_pattern_base.get(parent.item,0)
                    cond_pattern_base[parent.item] = freq+next_node.count
                    parent = parent.parent
                next_node = next_node.next_header_node
            cond_pattern_base_dict[item] = cond_pattern_base
        
        self.cond_pattern_base_dict_ = dict()
        for item,cond_pattern_base in cond_pattern_base_dict.items():
            freq_cond_pattern_base_dict = dict()
            for k,v in cond_pattern_base.items():
                if v >= self.min_support:
                    freq_cond_pattern_base_dict[k] = v
            self.cond_pattern_base_dict_[item] = freq_cond_pattern_base_dict
        
        
        from itertools import combinations
        self.freq_pattern_dict_ = dict()
        for item,cond_pattern_base in self.cond_pattern_base_dict_.items():
            for size in range(1,len(cond_pattern_base)+1):
                for other_items in combinations(cond_pattern_base.keys(),size):
                    freq_pattern = tuple([item]+[i for i in other_items])
                    self.freq_pattern_dict_[freq_pattern] = min([cond_pattern_base[i] for i in other_items])
        self.freq_pattern_dict_.update(self.item_frequency_dict_)
            
        
        
        
        
        

class Node():
    '''
    FP tree中的节点类
    args:
        item: str 项名称
        parent: Node 该节点的父节点
        count: int 该节点此时的支持度
    attr:
        next_header_node: None or Node 根据项头表的存在的指针，指向下一个Node
        child_dict: dict key=item value=None
    '''
    
    def __init__(self, item, parent, count=1):
        self.item = item
        self.parent = parent
        self.count = count
        self.next_header_node = None
        self.child_dict = dict()
        
    def get_child(self, child_item):
        '''
        从本节点内的子节点中找到item为child_item的子节点
        args:
            child_item:str 子节点的项目名
        return:
            child_node:None or Node 如果不存在则返回None，否则返回子节点
        '''
        child_node = self.child_dict.get(child_item,None)
        
        return child_node
    
    def add_child(self, child_item):
        '''
        如果不存在项目名为child_item的子节点，为本节点添加一个这样的子节点
        args:
            child_item:str 子节点的项目名
        return:
            child: Node 子节点对象
        '''
        if not child_item in self.child_dict:
            child = Node(child_item,self,1)
            self.child_dict[child_item] = child
        return child
        
    def __str__(self):
        string = str(self.item) + ','+str(self.count)
        return string
        
        
        
        
        
   
        
        
        
        
        
        
    
