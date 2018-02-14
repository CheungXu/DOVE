# -*- coding:utf-8 -*-  

import random,math
import numpy as np

"""
CLASS: Person

PROPERTY:
id：Person ID(unique value).
spouse: The ID of person's spouse(-1 refer to no spouse).
spouse_num: The rank of spouse in love list.
change_num: The times of change spouse of person.
accepted_threshold: The worst spouse that person can accept in love list.

FUNCTION:
marriage_with(): Establish relation link between two person.
dismarriaged(): Break relation link.
spouse_num_add_1(): Add 1 to spouse_num.
set_spouse_num(): Set set_spouse_num to specified value.
print_all(): Print person information.
"""
class Person(object):
    def __init__(self, person_id,feature_list,weight_list):
        if not isinstance(person_id,int) or not isinstance(feature_list,list) or not isinstance(weight_list,list):
            print person_id
            print feature_list
            print weight_list
            raise ValueError
        elif not len(feature_list) == len(weight_list):
            raise ValueError
        self.__id = person_id
        self.__feature_num = len(feature_list)
        self.__feature_list = feature_list
        self.__weight_list = weight_list
        self.__spouse = -1
        self.__spouse_num = -1
        self.__change_num = 0
        self.__accepted_threshold = 0
        self.__love_list = []
        self.__value_list = []
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
        if num<0 :
            return False
        else:
            self.__accepted_threshold = num - 1
            return True
    def set_love_list(self,love_list):
        self.__love_list = love_list
    def get_love_list(self):
        return self.__love_list
    def get_id(self):
        return self.__id
    def get_feature_list(self):
        return self.__feature_list
    def get_feature_num(self):
        return self.__feature_num
    def set_value_list(self,value_list):
        self.__value_list = value_list
    def get_value_list(self):
        return self.__value_list
    def get_weight_list(self):
        return self.__weight_list
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
        print 'Feature_List: ', self.__feature_list
        print 'Weight_List: ',self.__weight_list
        print 'Spouse: ', self.__spouse
        print 'Change_num: ', self.__change_num
        if len(self.__love_list) > 0:
            print 'Love_List: ', self.__love_list
        if len(self.__value_list) > 0:
            print 'Value_List: ', self.__value_list


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
    def __init__(self, person_id, feature_list, weight_list):
        Person.__init__(self,person_id,feature_list,weight_list)
        self.__activity = True
        self.__target_iter = 0

    def refresh_love_list(self,target_features): 
        np_list = np.dot(np.array(self.get_weight_list()), np.array(target_features))
        self.set_value_list(np.round(np_list,2).tolist())
        self.__target_num = len(np_list)
        order = {}
        for i in range(len(np_list)):
            order[i] = round(np_list[i],2)
        self.set_love_list([par[0] for par in sorted(order.items(), key=lambda d:d[1], reverse = True)])
          
    def next_target(self):
        if self.__target_iter < self.get_accepted_threshold() and self.__target_iter< self.__target_num - 1:
            self.__target_iter = self.__target_iter + 1
            return True
        else:
            return False
        
    def go_after(self, receiver, log):
        if not isinstance(receiver,Suitor):
            raise ValueError
        husband_id = receiver.get_spouse()
        love_list = receiver.get_love_list()
        person_id = receiver.get_id()
        self_id = self.get_id()
        rank = love_list.index(self_id)
        accepted_threshold = receiver.get_accepted_threshold()
        log.write('    Suitor Rank:'+str(rank)+'\n')
        change_husband = True
        if husband_id != -1:
            husband_rank = love_list.index(husband_id)
            log.write('    Husband Rank: '+str(husband_rank)+'\n')
            if rank > husband_rank:
                change_husband = False
        elif rank > accepted_threshold:
                change_husband = False
        if change_husband:
            log.write('    Succeed: ')
            receiver.marriage_with(self_id)
            receiver.refresh_spouse_num(rank+1)
            self.marriage_with(person_id)
            self.set_spouse_num(self.__target_iter+1)
            log.write(str(self_id) + ' married with  '+str(person_id)+'\n')
            return True
        else:
            log.write('    Failed\n')
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
        love_list = self.get_love_list()
        return love_list[self.__target_iter]

    def is_activity(self):
        return self.__activity

    def threw_away(self,suitor):
        suitor.be_thrown()

    def refresh_spouse_num(self,num):
        self.set_spouse_num(num)



"""
CLASS: Receiver

FUNCTION:
threw_away(): Threw spouse.
refresh_spouse_num():Refresh spouse num after threw.

"""
#class Receiver(Person):
    


"""
CLASS: Matching

PROPERTY:
suitors: A set of instance of CLASS Suitors.
receivers: A set of instance of CLASS Receivers.
suitor_avg_rank: Save sutior average rank in receivers.
receivers_avg_rank:Save receiver average rank in suitors.

FUNCTION:
avg_rank()：Caculate receivers_avg_rank and suitor_avg_rank.
start(): Start match experiment.
"""
class Matching(object):
    def __init__(self, suitors, receivers):
        self.__log = open('log.txt','w')
        self.__match_done = False
        self.__pre_change = True
        self.__now_change = True
        self.__times = 0
        self.__index = 0
        self.__suitors = suitors
        self.__receivers = receivers
        self.__suitor_features = []
        self.__receiver_features = []
        for i in range(self.__suitors[0].get_feature_num()):
            self.__suitor_features.append([])
            self.__receiver_features.append([])
        self.__suitor_avg_rank = []
        self.__receiver_avg_rank = []
        
        for i in range(len(self.__suitors)):
            self.__suitor_avg_rank.append(0.0)
            features = self.__suitors[i].get_feature_list()
            for j in range(len(features)):
                self.__suitor_features[j].append(features[j])
        for i in range(len(self.__receivers)):
            self.__receiver_avg_rank.append(0.0)
            features = self.__receivers[i].get_feature_list()
            for j in range(len(features)):
                self.__receiver_features[j].append(features[j])
                
        for i in range(len(self.__suitors)):
            self.__suitors[i].refresh_love_list(self.__receiver_features)
        for i in range(len(self.__receivers)):
            self.__receivers[i].refresh_love_list(self.__suitor_features)
            
    def __del__(self):
        self.__log.close()
        self.__suitor_features = []
        self.__receiver_features = []
        self.__suitor_avg_rank = []
        self.__receiver_avg_rank = []
        
    def avg_rank(self):
        self.__suitor_ranks  = []
        self.__receiver_ranks = []
        for i in range(len(self.__suitors)):
            self.__suitor_ranks.append([])
        for i in range(len(self.__receivers)):
            self.__receiver_ranks.append([])
        for i in range(len(self.__suitors)):
            love_list = self.__suitors[i].get_love_list()
            for j in range(len(love_list)):
                index = love_list[j]
                self.__receiver_avg_rank[index] = self.__receiver_avg_rank[index] + j + 1
                self.__receiver_ranks[index].append(j+1)     
        for i in range(len(self.__receiver_avg_rank)):
            self.__receiver_avg_rank[i] = self.__receiver_avg_rank[i] / float(len(self.__suitors))
        for i in range(len(self.__receivers)):
            love_list = self.__receivers[i].get_love_list()
            for j in range(len(love_list)):
                index = love_list[j]
                self.__suitor_avg_rank[index] = self.__suitor_avg_rank[index] + j + 1
                self.__suitor_ranks[index].append(j+1)
        for i in range(len(self.__suitor_avg_rank)):
            self.__suitor_avg_rank[i] = self.__suitor_avg_rank[i] / float(len(self.__receivers))
        self.__suitor_std_rank = [round(np.std(l),2) for l in self.__suitor_ranks]
        self.__receiver_std_rank = [round(np.std(l),2) for l in self.__receiver_ranks]

    def __add_index(self):
        self.__index += 1
        if self.__index == len(self.__suitors):
            self.__times += 1
            self.__index = 0
            if not self.__pre_change and not self.__now_change:
                self.__match_done = True
                self.__log.write('DONE')
            else:
                self.__pre_change = self.__now_change
                self.__now_change = False
        return True
    
    def step(self):
        if self.__match_done:
            return False
        suitor = self.__suitors[self.__index]
        spouse = suitor.get_spouse()
        if spouse == -1 and suitor.is_activity():
            self.__now_change = True
            target = suitor.get_target()
            self.__log.write('  STEP '+str(self.__index) + '\n')
            self.__log.write('    '+str(self.__index)+' target  '+str(target)+'\n')
            if target == -1:
                self.__add_index()
                return True
            else:
                husband = self.__receivers[target].get_spouse()
                if suitor.go_after(self.__receivers[target],self.__log):
                    if husband >= 0:
                        self.__receivers[target].threw_away(self.__suitors[husband])
                        self.__log.write('    '+str(target)+' threw away '+str(husband)+'\n')
        self.__add_index()
        return True
            
    def epoch(self):
        self.__log.write('EPOCH '+str(self.__times)+'\n')
        for i in range(self.__index, len(self.__suitors)):
            self.__index = i
            self.step()
    
    def start(self):
        self.avg_rank()
        while True:
            self.epoch()
            if self.__match_done:
                break
        return True

    def is_done(self):
        return self.__match_done
    
    def print_suitors(self):
        print 'id  spouse  change_num  spouse_rank  avg_rank  std_rank'
        for i in range(len(self.__suitors)):
            print self.__suitors[i].get_id(), '    ', \
                  self.__suitors[i].get_spouse(), '       ', \
                  self.__suitors[i].get_change_num(), '         ', \
                  self.__suitors[i].get_spouse_num(), '       ', \
                  self.__suitor_avg_rank[i], '       ', \
                  self.__suitor_std_rank[i]

    def print_receivers(self):
        print 'id  spouse  change_num  spouse_rank  avg_rank  std_rank'
        for i in range(len(self.__receivers)):
            print self.__receivers[i].get_id(), '    ',\
                  self.__receivers[i].get_spouse(), '       ',\
                  self.__receivers[i].get_change_num(), '         ',\
                  self.__receivers[i].get_spouse_num(), '       ',\
                  self.__receiver_avg_rank[i], '       ',\
                  self.__receiver_std_rank[i]
    
    def save_init_information(self,save):
        save.write('SUI_LIST\n')
        for i in range(len(self.__suitors)):
            line = str(self.__suitors[i].get_id()) \
                   + '   L: ' + str(self.__suitors[i].get_love_list()) \
                   + '   F: ' + str(self.__suitors[i].get_feature_list()) \
                   + '   W: ' + str(self.__suitors[i].get_weight_list()) \
                   + '   V: ' +str(self.__suitors[i].get_value_list()) + '\n'
            save.write(line)
        save.write('\nREC_LIST\n')
        for i in range(len(self.__receivers)):
            line = str(self.__receivers[i].get_id()) \
                   + '   L: ' + str(self.__receivers[i].get_love_list()) \
                   + '   F: ' + str(self.__receivers[i].get_feature_list()) \
                   + '   W: ' + str(self.__receivers[i].get_weight_list()) \
                   + '   V: ' +str(self.__receivers[i].get_value_list()) + '\n'
            save.write(line)
            
    def save_suitors(self,save):
        save.write('id  spouse  change_num  spouse_rank  avg_rank  std_rank\n')
        for i in range(len(self.__suitors)):
            line = str(self.__suitors[i].get_id()) + '    ' \
                   + str(self.__suitors[i].get_spouse()) + '       '\
                   + str(self.__suitors[i].get_change_num()) + '         '\
                   + str(self.__suitors[i].get_spouse_num()) + '       ' \
                   + str(self.__suitor_avg_rank[i]) + '       ' \
                   + str(self.__suitor_std_rank[i]) + '\n'
            save.write(line)

    def save_receivers(self,save):
        save.write('id  spouse  change_num  spouse_rank  avg_rank  std_rank\n')
        for i in range(len(self.__receivers)):
            line = str(self.__receivers[i].get_id()) + '    ' \
                   + str(self.__receivers[i].get_spouse()) + '       '\
                   + str(self.__receivers[i].get_change_num()) + '         '\
                   + str(self.__receivers[i].get_spouse_num()) + '       ' \
                   + str(self.__receiver_avg_rank[i]) + '       ' \
                   + str(self.__receiver_std_rank[i]) + '\n'
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
                
    def get_avg_rank(self):
        return self.__suitor_avg_rank, self.__receiver_avg_rank
    def get_std_rank(self):
        return self.__suitor_std_rank,  self.__receiver_std_rank
    def get_spouse_rank(self):
        return [s.get_spouse_num() for s in self.__suitors], [r.get_spouse_num() for r in self.__receivers]
    


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
    def __sigmoid(self,value):
        return 1.0/(1.0+math.exp(-value))
    def get_feature(self):
        return self.__feature_list
    
    def create_feaure(self):
        self.__clear()
        for i in range(self.__person_num):
            f_list = np.round(np.random.normal(5,2,self.__feature_num),2)
            self.__feature_list.append(f_list.tolist())
        return self.__feature_list
    
    def create_feature_sigmoid(self):
        self.__clear()
        for i in range(self.__person_num):
            f_list = np.round(np.random.normal(0,4,self.__feature_num),2)
            self.__feature_list.append(f_list.tolist())
        for i in range(self.__person_num):
            for j in range(self.__feature_num):
                self.__feature_list[i][j] = round(self.__sigmoid(self.__feature_list[i][j]),2)
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
                self.__feature_list[i][j] = round((self.__feature_list[i][j] - min_feature[j]) / length[j], 2)
                
        return self.__feature_list


class Weight_randomer(object):
    def __init__(self,weight_num,person_num):
        self.__weight_num = weight_num
        self.__person_num = person_num
        self.__weight_list = []
    def __clear(self):
        self.__value_list = []
    def get_weight_list(self):
        return self.__value_list
    def create_weight_list(self):
        self.__clear()
        for i in range(self.__person_num):
            x = np.round(np.random.normal(5,2,self.__weight_num),2)
            min_value = 100
            max_value = -100
            sum_value = 0.0
            for feature in x:
                sum_value = sum_value + feature
            for j in range(len(x)):
                x[j] = np.round(x[j] / sum_value,2)
            res_sum = 0.0
            for j in range(len(x)):
                res_sum += x[j]
            if res_sum != 1.0:
                x[0] -= (res_sum - 1.0)
                x[0] = np.round(x[0],2)
            self.__weight_list.append(x.tolist())
                
        return self.__weight_list


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
def create_Person(person_num, feature_num, accepted_threshold = 0):
    fr = Feature_randomer(feature_num, person_num)
    wr = Weight_randomer(feature_num, person_num)
    features = fr.create_feature_normalisze()  #fr.create_feature_sigmoid()#
    weights = wr.create_weight_list()
    persons = []
    for i in range(person_num):
        person = Suitor(i,features[i],weights[i])
        if accepted_threshold:
            person.set_accepted_threshold(accepted_threshold)
        persons.append(person)
    return persons


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
