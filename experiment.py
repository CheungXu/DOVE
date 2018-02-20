# -*- coding:utf-8 -*-  
import dove
import copy

class Experiments(object):
    def __init__(self,person_num = 20,feature_num = 3):
        self.__person_num = person_num
        self.__feature_num = feature_num
        self.__save_path = '.\\data\\test.txt'
        self.__save = open(self.__save_path,'w')
        self.__man = dove.create_Person(person_num,feature_num,person_num)
        self.__woman = dove.create_Person(person_num,feature_num,person_num)

    def __del__(self):
        self.__person_num  = 0
        self.__save_path = ''
        if self.__save:
            self.__save.close()

    def get_man_num(self):
        return len(self.__man)

    def get_woman_num(self):
        return len(self.__woman)
    
    def write_init_condition(self, matching):
        matching.save_init_information(self.__save)

    def avg_rank(self):
        matching = dove.Matching(self.__man,self.__woman)
        matching.avg_rank()
        """
        self.write_init_condition(matching)
        self.save.write('\nEXP ONE \n')
        self.save.write('SUI_MAN\n')
        matching.save_suitors(self.save)
        self.save.write('REC_WOMAN\n')
        matching.save_receivers(self.save)
        """
        return matching
    
    def unidirectional_match(self):
        matching = dove.Matching(self.__man,self.__woman)
        self.write_init_condition(matching)
        matching.compute_avg_rank()
        self.__save.write('\nEXP ONE \n')
        self.__save.write('SUI_MAN\n')
        matching.save_suitors(self.__save)
        self.__save.write('REC_WOMAN\n')
        matching.save_receivers(self.__save)
        
        return matching

    def unidirectional_match_both_sides(self):
        matching_forward = dove.Matching(self.__man,self.__woman)
        matching_backward = dove.Matching(self.__woman,self.__man)
        self.write_init_condition(matching_forward)
        self.write_init_condition(matching_backward)
        matching_forward.start()
        matching_backward.start()
        self.__save.write('\nEXP ONE \n')
        self.__save.write('SUI_MAN\n')
        matching_forward.save_suitors(self.__save)
        self.__save.write('REC_WOMAN\n')
        matching_forward.save_receivers(self.__save)

        self.__save.write('\nEXP TWO \n')
        self.__save.write('REC_MAN\n')
        matching_backward.save_receivers(self.__save)
        self.__save.write('SUI_WOMAN\n')
        matching_backward.save_suitors(self.__save)

        print 'SUI_MAN:'
        matching_forward.print_suitors()
        print 'REC_WOM:'
        matching_forward.print_receivers()
        print '               '
        print 'REC_MAN:'
        matching_backward.print_receivers()
        print 'SUI_WOM:'
        matching_backward.print_suitors()

        return matching_forward, matching_backward

            
if __name__ == '__main__':
    exp = Experiments(500,5)
    mth = exp.unidirectional_match()
    s_a, r_a = mth.get_avg_rank()
    s_s, r_s = mth.get_std_rank()
    s_r, r_r = mth.get_spouse_rank()
    del exp
    import matplotlib.pyplot as plt
    plt.scatter(s_a,s_r,c='b')
    plt.scatter(r_a,r_r,c='r')
    #plt.scatter(s_a, s_s, c = 'b')
    #plt.scatter(r_a, r_s, c = 'r')
    plt.show()
