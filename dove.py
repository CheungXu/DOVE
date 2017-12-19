# -*- coding:utf-8 -*-  

import random
import numpy as np

"""
CLASS: Person

PROPERTY:
id：Person ID(unique value).
love_list: Person's love rank list.
sex: Person's sex(not used yete).
spouse: The ID of person's spouse(-1 refer to no spouse).
spouse_num: The rank of spouse in love list.
change_num: The times of change spouse of person.
accepted_threshold: The worst spouse that person can accept in love list.

FUNCTION:
marriage_with(): Establish relation link in two person.
dismarriaged(): Break relation link.
spouse_num_add_1(): Add 1 to spouse_num.
set_spouse_num(): Set set_spouse_num to specified value.
print_all(): Print person information.
"""
class Person(object):
    def __init__(self, person_id,feature_list,value_list):
        if not isinstance(person_id,int) or not isinstance(feature_list,list) or not isinstance(value_list,list):
            raise ValueError
        elif not len(feature_list) == len(value_list):
            raise ValueError
        self.__id = person_id
        self.__list = []
        self.__feature_num = len(feature_list)
        self.__feature_list = feature_list
        self.__value_list = value_list
        self.__spouse = -1
        self.__spouse_num = -1
        self.__change_num = 0
        self.__accepted_threshold = 0
    def marriage_with(self, person_id):
        self.__spouse = person_id
        self.__change_num = self.__change_num + 1
        return self.__spouse
    def dismarriaged(self):
        self.__spouse = -1
        self.__spouse_num = -1
    def spouse_num_add_1(self):
        self.__spouse_num = self.__spouse_num + 1
    def set_spouse_num(self, num):
        if num < 0 or num > self.__accepted_threshold + 1:
            return False
        else:
            self.__spouse_num = num
            return True
    def set_accepted_threshold(self,num):
        if num<0 or num > (len(self.__list)-1):
            return False
        else:
            self.__accepted_threshold = num - 1
            return True
    def get_id(self):
        return self.__id
    def get_list(self):
        return self.__list
    def get_spouse(self):
        return self.__spouse
    def get_change_num(self):
        return self.__change_num
    def get_spouse_num(self):
        return self.__spouse_num
    def get_accepted_threshold(self):
        return self.__accepted_threshold
    def print_all(self):
        print 'ID:', self.__id
        print 'List:', self.__list
        print 'Spouse:', self.__spouse
        print 'Sex:', self.__sex
        print 'Change_num:', self.__change_num


"""
CLASS: Suitor

PROPERTY: Inherit from CLASS Person
target_iter: Target index in love list.
activity: Suitor state(Stop search when activity is False).

FUNCTION:
go_after(): Try to establish relation link to someone.
__refused():Called when establish relation link failed.
be_thrown():Called when relation link was break by spouse.
get_target(): Return the target of suitor.
next_target(): Move target to next available person.
"""
class Suitor(Person):
    def __init__(self, person_id, feature_list, value_list):
        Person.__init__(self,person_id,feature_list,value_list)
        self.__activity = True
        self.__target_iter = 0
        
    def next_target(self):
        if self.__target_iter < self.get_accepted_threshold():
            self.__target_iter = self.__target_iter + 1
            return True
        else:
            return False
        
    def go_after(self, receiver):
        if not isinstance(receiver,Receiver):
            raise ValueError
        husband_id = receiver.get_spouse()
        love_list = receiver.get_list()
        person_id = receiver.get_id()
        self_id = self.get_id()
        rank = love_list.index(self_id)
        accepted_threshold = receiver.get_accepted_threshold()
        print 'rank:', rank
        change_husband = True
        if husband_id != -1:
            husband_rank = love_list.index(husband_id)
            print 'husband_rank', husband_rank
            if rank > husband_rank:
                change_husband = False
        elif rank > accepted_threshold:
                change_husband = False
        if change_husband:
            receiver.marriage_with(self_id)
            receiver.refresh_spouse_num(rank+1)
            self.marriage_with(person_id)
            self.set_spouse_num(self.__target_iter+1)
            print 'merriage  ', self_id,person_id
            return True
        else:
            self.__refused()
            return False
        
    def __refused(self):
        res = self.next_target()
        if not res:
            self.__activity = False
        return res
        
    def be_thrown(self):
        self.dismarriaged()
        return self.__refused()
    
    def get_target(self):
        love_list = self.get_list()
        return love_list[self.__target_iter]

    def is_activity(self):
        return self.__activity

"""
CLASS: Receiver

FUNCTION:
threw_away(): Threw spouse.
refresh_spouse_num():Refresh spouse num after threw.

"""
class Receiver(Person):
    def threw_away(self,suitor):
        suitor.be_thrown()
    def refresh_spouse_num(self,num):
        self.set_spouse_num(num)


"""
CLASS: Experiment

PROPERTY:
suitors: A set of instance of CLASS Suitors.
receivers: A set of instance of CLASS Receivers.
suitor_avg_rank: Save sutior average rank in receivers.
receivers_avg_rank:Save receiver average rank in suitors.

FUNCTION:
avg_rank()：Caculate receivers_avg_rank and suitor_avg_rank.
start(): Start match experiment.
"""
class Experiment(object):
    def __init__(self, suitors, receivers):
        self.__suitors = suitors
        self.__receivers = receivers
        self.__suitor_avg_rank = []
        self.__receivers_avg_rank = []
        for i in range(len(suitors)):
            self.__suitor_avg_rank.append(0.0)
        for i in range(len(receivers)):
            self.__receivers_avg_rank.append(0.0)

    def avg_rank(self):
        print len(self.__suitors)
        print len(self.__receivers)
        for i in range(len(self.__suitors)):
            love_list = self.__suitors[i].get_list()
            for j in range(len(love_list)):
                index = love_list[j]
                self.__receivers_avg_rank[index] = self.__receivers_avg_rank[index] + j + 1
        for i in range(len(self.__receivers_avg_rank)):
            self.__receivers_avg_rank[i] = self.__receivers_avg_rank[i] / float(len(self.__suitors))
        for i in range(len(self.__receivers)):
            love_list = self.__receivers[i].get_list()
            for j in range(len(love_list)):
                index = love_list[j]
                self.__suitor_avg_rank[index] = self.__suitor_avg_rank[index] + j + 1
        for i in range(len(self.__suitor_avg_rank)):
            self.__suitor_avg_rank[i] = self.__suitor_avg_rank[i] / float(len(self.__receivers))            

    def start(self):
        self.avg_rank()
        times = 0
        pre_change = True
        now_change = True
        while True:
            pre_change = now_change
            now_change = False
            print 'TIMES: ', times
            times = times + 1
            for i in range(len(self.__suitors)):
                suitor = self.__suitors[i]
                spouse = suitor.get_spouse()
                if spouse == -1 and suitor.is_activity():
                    now_change = True
                    target = suitor.get_target()
                    print i,'target  ',target
                    if target == -1:
                        continue
                    else:
                        husband = self.__receivers[target].get_spouse()
                        if suitor.go_after(self.__receivers[target]):
                            if husband >= 0:
                                self.__receivers[target].threw_away(self.__suitors[husband])
                                print target,' threw away ',husband
            if not pre_change and not now_change:
                break
        return True

    def print_suitors(self):
        print 'id  spouse  change_num  spouse_rank  avg_rank'
        for i in range(len(self.__suitors)):
            print self.__suitors[i].get_id(), '    ', \
                  self.__suitors[i].get_spouse(), '       ', \
                  self.__suitors[i].get_change_num(), '         ', \
                  self.__suitors[i].get_spouse_num(), '       ', \
                  self.__suitor_avg_rank[i]

    def print_receivers(self):
        print 'id  spouse  change_num  spouse_rank  avg_rank'
        for i in range(len(self.__receivers)):
            print self.__receivers[i].get_id(), '    ',\
                  self.__receivers[i].get_spouse(), '       ',\
                  self.__receivers[i].get_change_num(), '         ',\
                  self.__receivers[i].get_spouse_num(), '       ',\
                  self.__receivers_avg_rank[i]

    def save_suitors(self,save):
        save.write('id  spouse  change_num  spouse_rank  avg_rank\n')
        for i in range(len(self.__suitors)):
            line = str(self.__suitors[i].get_id()) + '    ' \
                   + str(self.__suitors[i].get_spouse()) + '       '\
                   + str(self.__suitors[i].get_change_num()) + '         '\
                   + str(self.__suitors[i].get_spouse_num()) + '       ' \
                   + str(self.__suitor_avg_rank[i]) + '\n'
            save.write(line)

    def save_receivers(self,save):
        save.write('id  spouse  change_num  spouse_rank  avg_rank\n')
        for i in range(len(self.__receivers)):
            line = str(self.__receivers[i].get_id()) + '    ' \
                   + str(self.__receivers[i].get_spouse()) + '       '\
                   + str(self.__receivers[i].get_change_num()) + '         '\
                   + str(self.__receivers[i].get_spouse_num()) + '       ' \
                   + str(self.__receivers_avg_rank[i]) + '\n'
            save.write(line)

    def save_couple_rank():
        save.write('suitor_id  receiver_id  suitor_rank  receiver_rank  avg_rank  rank_diff')
        for i in range(len(self.__suitors)):
            suitor =  self.__suitors[i]
            if suitor.get_spouse() != -1:
                suitor_rank = self.__suitors_avg_rank[i]
                receiver_rank = self.__receivers_avg_rank[i]
                line = str(suitors.get_id()) + '   '\
                       + str(suitors.get_spouse()) + '      '\
                       + str(suitor_rank) + '      '\
                       + str(receiver_rank) + '      '\
                       + str((suitor_rank+receiver_rank)/2) + '     '\
                       + str(abs(suitor_rank-receiver_rank) + '\n')
                save.write(line)


"""
CLASS: Feature_randomer

PROPERTY:
num: Num of features.
pick_list: List of features.

FUNCTION:
create_feature: Create random features.
"""
class Feature_randomer(object):
    def __init__(self,feature_num,person_num):
        self.__feature_num = feature_num
        self.__person_num = person_num
        self.__feature_list = []
    def __clear(self):
        self.__feature_list = []
    def get_feature(self):
        return self.__feature_list
    def create_feaure(self):
        self.__clear()
        for i in range(self.__person_num):
            f_list = np.round(np.random.normal(5,2,self.__feature_num),2)
            self.__feature_list.append(f_list.tolist())
        return self.__feature_list
    def create_feature_normalisze(self):
        self.__clear()
        for i in range(self.__person_num):
            f_list = np.round(np.random.normal(5,2,self.__feature_num),2)
            self.__feature_list.append(f_list.tolist())
        max_feature = []
        min_feature = []
        for j in range(self.__feature_num):
            max_feature.append(-100)
            min_feature.append(100)
        for i in range(self.__person_num):
            for j in range(self.__feature_num):
                if self.__feature_list[i][j] > max_feature[j]:
                    max_feature[j] = self.__feature_list[i][j]
                if self.__feature_list[i][j] < min_feature[j]:
                    min_feature[j] = self.__feature_list[i][j]
        length = []
        for j in range(self.__feature_num):
            length.append(max_feature[j]-min_feature[j])
        for i in range(self.__person_num):
            for j in range(self.__feature_num):
                self.__feature_list[i][j] = (self.__feature_list[i][j] - min_feature[j]) / length[j]
                
        return np.round(self.__feature_list,2)


class Value_randomer(object):
    def __init__(self,value_num,person_num):
        self.__feature_num = value_num
        self.__person_num = person_num
        self.__value_list = []
    def __clear(self):
        self.__value_list = []
    def get_value_list(self):
        return self.__value_list
    def create_value_list(self):
        self.__clear()
        for i in range(self.__person_num):
            x = np.round(np.random.normal(5,2,self.__feature_num),2)
            min_value = 100
            max_value = -100
            sum_value = 0.0
            for feature in x:
                sum_value = sum_value + feature
            for i in range(len(x)):
                x[i] = np.round(x[i] / sum_value,2)
            self.__value_list.append(x.tolist())
        return self.__value_list

        
        

"""
CLASS: List_randomer

PROPERTY:
bottom,top: The range of random.
pick_list: List of random numbers.

FUNCTION:
create_list: Shuffle random numbers.
"""
class List_randomer(object):
    def __init__(self, bottom, top):
        self.__bottom = bottom
        self.__top = top
        self.__pick_list = []
        num = top - bottom
        for i in range(num):
            self.__pick_list.append(bottom + i)
    def get_pick_list(self):
        return self.__pick_list
    def create_list(self):
        random.shuffle(self.__pick_list)
        return self.__pick_list


#Create Suitors/Receivers by Randomer
def create_Suitors(love_lists, accepted_threshold = 0):
    suis = []
    for i in range(len(love_lists)):
        sui = Suitor(i,love_lists[i],1)
        if accepted_threshold:
            sui.set_accepted_threshold(accepted_threshold)
        suis.append(sui)
    return suis


def create_Receivers(love_lists, accepted_threshold = 0):
    recs = []
    for i in range(len(love_lists)):
        rec = Receiver(i,love_lists[i],1)
        if accepted_threshold:
            rec.set_accepted_threshold(accepted_threshold)
        recs.append(rec)
    return recs


#Load Suitors/Receivers from Record File
def load_Suitors(path,accepted_threshold = 0):
    suis = []
    with open(path, 'r') as f:
        lines  = f.readlines()
    for i in len(lines):
        love_list = []
        data = line[i].strip().split()
        for d in data:
            love_list.append(int(d))
        sui = Suitor(i,love_lists,1)
        if accepted_threshold:
            rec.set_accepted_threshold(accepted_threshold)
        suis.append(sui)
    return suis

def load_Receivers(path,accepted_threshold = 0):
    recs = []
    with open(path, 'r') as f:
        lines  = f.readlines()
    for i in len(lines):
        love_list = []
        data = line[i].strip().split()
        for d in data:
            love_list.append(int(d))
        rec = Receiver(i,love_lists,1)
        if accepted_threshold:
            rec.set_accepted_threshold(accepted_threshold)
        recs.append(rec)
    return recs
