# -*- coding:utf-8 -*-  
import dove
import copy

class Experiments(object):
    def __init__(self,person_num = 20,feature_num = 3):
        self.person_num = person_num
        self.feature_num = feature_num
        self.save_path = '.\\data\\test.txt'
        self.save = open(self.save_path,'w')
        self.man = dove.create_Person(person_num,feature_num,person_num)
        self.woman = dove.create_Person(person_num,feature_num,person_num)

    def __del__(self):
        self.person_num  = 0
        self.save_path = ''
        if self.save:
            self.save.close()
        
    def write_init_condition(self, matching):
        matching.save_init_information(self.save)

    def avg_rank(self):
        matching = dove.Matching(self.man,self.woman)
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
        matching = dove.Matching(self.man,self.woman)
        self.write_init_condition(matching)
        matching.compute_avg_rank()
        self.save.write('\nEXP ONE \n')
        self.save.write('SUI_MAN\n')
        matching.save_suitors(self.save)
        self.save.write('REC_WOMAN\n')
        matching.save_receivers(self.save)
        
        return matching

    def unidirectional_match_both_sides(self):
        matching_forward = dove.Matching(self.man,self.woman)
        matching_backward = dove.Matching(self.woman,self.man)
        self.write_init_condition(matching_forward)
        self.write_init_condition(matching_backward)
        matching_forward.start()
        matching_backward.start()
        self.save.write('\nEXP ONE \n')
        self.save.write('SUI_MAN\n')
        matching_forward.save_suitors(self.save)
        self.save.write('REC_WOMAN\n')
        matching_forward.save_receivers(self.save)

        self.save.write('\nEXP TWO \n')
        self.save.write('REC_MAN\n')
        matching_backward.save_receivers(self.save)
        self.save.write('SUI_WOMAN\n')
        matching_backward.save_suitors(self.save)

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
