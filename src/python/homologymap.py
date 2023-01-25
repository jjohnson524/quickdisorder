# this function takes a fixed presentation of a fundamental group G=<a1,a2, ... a_n | r_1 ... r_m >
#where G^ab = Z and computes the map to homology where the image of each generator is recorded.

from sage.all import *

def element_count(word, element):
    count = 0
    for i in word:
        if i == element.lower():
            count = count+1
        elif i == element.upper():
            count = count-1
    return count

def total_element_count(word, gen_set):
    total_count = []
    for i in gen_set:
        total_count.append(element_count(word,i))
    return total_count

def augmented_diagonal(A):
    return [A[i,i] for i in range(len(A.rows()))]

class homology_map:
     def __init__(self, G, use_specific_generator = None):
         self.group = G
         # put in assertion on G ?

         my_homology_map = []

         self.group_gens = G.generators()

         my_relators = G.relators()

         relation_matrix_data =[]
         if use_specific_generator == None:
             new_row = [1]
             for i in self.group_gens[:-1]:
                 new_row.append(0)
             
         else:
             new_row = []
             for i in range(len(self.group_gens)):
                 if i == use_specific_generator:
                     new_row.append(1)
                 else:
                     new_row.append(0)
         new_row.append(1) # this is a guess on where the first generator goes, we will clean it up later....
                    
                 
         relation_matrix_data.append([x for x in new_row])
         
         for r in my_relators:
             new_row = []
             for g in self.group_gens:
                  new_row.append(element_count(r, g))
             new_row.append(0) # this words are all the identity so they are homologically trivial
             
             relation_matrix_data.append([x for x in new_row])

         my_matrix = matrix(relation_matrix_data).row_space().matrix() # the rest of this computation assumes the homology is Z

         aug_diag = [x for x in augmented_diagonal(my_matrix)]

         new_M1 = copy(my_matrix) # matricies of this form are immutable 
         for i in range(len(aug_diag)):
             if aug_diag[i] != 1:
                 new_M1[i,i] = 1
                 for j in range(len(aug_diag)):
                     if j != i:
                         new_M1[j,len(self.group_gens)] = my_matrix[j,len(self.group_gens)]*aug_diag[i]

         #print('new_M1', new_M1)
         
         self.homology_data_matrix = new_M1.row_space().matrix()    

         #print('data so far', [G, relation_matrix_data, aug_diag,'\n', homology_data_matrix] )
     def homology_image(self, word):
         word_weights = total_element_count(word, self.group_gens)
         weight  = 0

         for i in range(len(word_weights)):
             weight = word_weights[i]*self.homology_data_matrix[i,len(self.group_gens)]+weight
         return weight

     def get_homology_data_matrix(self):
         return self.homology_data_matrix
