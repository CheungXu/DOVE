

import dove
import copy
PERSON_NUM = 20
save_path = 'E:\\DOVE\\DOVE\\test.txt'
save = open(save_path,'w')

random = dove.list_randomer(0,PERSON_NUM)
mans_list = []
womans_list = []
for i in range(PERSON_NUM):
    mans_list.append(copy.copy(random.create_list()))
    womans_list.append(copy.copy(random.create_list()))

save.write('MAN_LIST\n')
for i in range(len(mans_list)):
    for j in range(len(mans_list[i])):
        save.write(str(mans_list[i][j]))
        save.write(' ')
    save.write('\n')

save.write('\nWOMAN_LIST\n')
for i in range(len(womans_list)):
    for j in range(len(womans_list[i])):
        save.write(str(womans_list[i][j]))
        save.write(' ')
    save.write('\n')

man_list = copy.deepcopy(mans_list)
woman_list = copy.deepcopy(womans_list)
sui_man = dove.create_Suitors(man_list)
res_woman = dove.create_Receivers(woman_list)

exp1 = dove.experiment(sui_man,res_woman)
exp1.start()

man_list = copy.deepcopy(mans_list)
woman_list = copy.deepcopy(womans_list)

print womans_list
print woman_list
res_man = dove.create_Receivers(man_list)
sui_woman = dove.create_Suitors(woman_list)

exp2 = dove.experiment(sui_woman,res_man)
exp2.start()

print 'SUI_MAN:'
exp1.print_suitors()
print 'RES_WOM:'
exp1.print_receivers()
print '               '
print 'RES_MAN:'
exp2.print_receivers()
print 'SUI_WOM:'
exp2.print_suitors()

save.write('\nEXP ONE \n')
save.write('SUI_MAN\n')
exp1.save_suitors(save)
save.write('RES_WOMAN\n')
exp1.save_receivers(save)

save.write('\nEXP TWO \n')
save.write('RES_MAN\n')
exp2.save_receivers(save)
save.write('SUI_WOMAN\n')
exp2.save_suitors(save)

save.close()
