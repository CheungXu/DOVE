import random

class person(object):
    def __init__(self, person_id, love_list, sex):
        self.__id = person_id
        self.__list = love_list
        self.__sex = sex
        self.__spouse = -1
        self.__spouse_num = 1
        self.__change_num = 0
    def marriage_with(self, person_id):
        self.__spouse = person_id
        self.__change_num = self.__change_num + 1
        return self.__spouse
    def dismarriaged(self):
        self.__spouse = -1        
    def spouse_num_add_1(self):
        self.__spouse_num = self.__spouse_num + 1
    def set_spouse_num(self, num):
        self.__spouse_num = num
    def del_list_0(self):
        del self.__list[0]
    def get_id(self):
        return self.__id
    def get_list(self):
        return self.__list
    def get_spouse(self):
        return self.__spouse
    def get_sex(self):
        return self.__sex
    def get_change_num(self):
        return self.__change_num
    def get_spouse_num(self):
        return self.__spouse_num
    def print_all(self):
        print 'ID:', self.__id
        print 'List:', self.__list
        print 'Spouse:', self.__spouse
        print 'Sex:', self.__sex
        print 'Change_num:', self.__change_num

class suitor(person):
    def go_after(self, receiver):
        husband_id = receiver.get_spouse()
        love_list = receiver.get_list()
        person_id = receiver.get_id()
        self_id = self.get_id()
        rank = love_list.index(self_id)
        print 'rank:', rank
        change_husband = True
        if husband_id != -1:
            husband_rank = love_list.index(husband_id)
            print 'husband_rank', husband_rank
            if rank > husband_rank:
                change_husband = False
        if change_husband:
            receiver.marriage_with(self_id)
            receiver.refresh_spouse_num(rank+1)
            self.marriage_with(person_id)
            print 'merriage  ', self_id,person_id
            return True
        else:
            self.__refused()
            return False
    def __refused(self):
        love_list = self.get_list()
        if len(love_list) > 0:
            self.del_list_0()       
            self.spouse_num_add_1()
            return True
        else:
            return False
    def be_thrown(self):
        self.dismarriaged()
        return self.__refused()
    def get_target(self):
        love_list = self.get_list()
        if len(love_list) > 0:
            return love_list[0]
        else:
            return -1

class receiver(person):
    def threw_away(self,suitor):
        suitor.be_thrown()
    def refresh_spouse_num(self,num):
        self.set_spouse_num(num)


class experiment(object):
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
                if spouse == -1:
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

class list_randomer(object):
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

def create_Suitors(love_lists):
    suis = []
    for i in range(len(love_lists)):
        sui = suitor(i,love_lists[i],1)
        suis.append(sui)
    return suis

def create_Receivers(love_lists):
    recs = []
    for i in range(len(love_lists)):
        rec = receiver(i,love_lists[i],1)
        recs.append(rec)
    return recs
