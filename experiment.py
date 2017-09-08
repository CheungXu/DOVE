# -*- coding:utf-8 -*-  
import dove
import copy

class Experiments(object):
    def __init__(self,person_num = 20):
        self.person_num = person_num
        self.save_path = '.\\data\\test.txt'
        self.save = open(self.save_path,'w')
        random = dove.List_randomer(0,self.person_num)
        self.mans_list = []
        self.womans_list = []
        for i in range(self.person_num):
            self.mans_list.append(copy.copy(random.create_list()))
            self.womans_list.append(copy.copy(random.create_list()))

    def __del__(self):
        self.person_num  = 0
        self.save_path = ''
        self.save.close()
        self.mans_list = []
        self.womans_list = []
        
    def write_init_condition(self):
        self.save.write('MAN_LIST\n')
        for i in range(len(self.mans_list)):
            for j in range(len(self.mans_list[i])):
                self.save.write(str(self.mans_list[i][j]))
                self.save.write(' ')
            self.save.write('\n')
        self.save.write('\nWOMAN_LIST\n')
        for i in range(len(self.womans_list)):
            for j in range(len(self.womans_list[i])):
                self.save.write(str(self.womans_list[i][j]))
                self.save.write(' ')
            self.save.write('\n')

    def __unidirectional_match__(self,suitor,receiver):
        suitor_list = copy.deepcopy(suitor)
        receiver_list = copy.deepcopy(receiver)
        suitor_result = dove.create_Suitors(suitor_list,5)
        receiver_result = dove.create_Receivers(receiver_list,5)
        experiment = dove.Experiment(suitor_result,receiver_result)
        experiment.start()
        return suitor_result,receiver_result,experiment

    def unidirectional_match_both_sides(self):
        suitor_man,receiver_woman,exp1 = self.__unidirectional_match__(self.mans_list,self.womans_list)
        suitor_woman,receiver_man,exp2 = self.__unidirectional_match__(self.womans_list,self.mans_list)

        self.save.write('\nEXP ONE \n')
        self.save.write('SUI_MAN\n')
        exp1.save_suitors(self.save)
        self.save.write('REC_WOMAN\n')
        exp1.save_receivers(self.save)

        self.save.write('\nEXP TWO \n')
        self.save.write('REC_MAN\n')
        exp2.save_receivers(self.save)
        self.save.write('SUI_WOMAN\n')
        exp2.save_suitors(self.save)

        print 'SUI_MAN:'
        exp1.print_suitors()
        print 'REC_WOM:'
        exp1.print_receivers()
        print '               '
        print 'REC_MAN:'
        exp2.print_receivers()
        print 'SUI_WOM:'
        exp2.print_suitors()
            

            
if __name__ == '__main__':
    exp = Experiments(20)
    exp.write_init_condition()
    exp.unidirectional_match_both_sides()
    del exp
