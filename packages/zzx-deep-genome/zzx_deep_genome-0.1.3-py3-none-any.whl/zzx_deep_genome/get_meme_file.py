import numpy as np
import pandas as pd

#要求输入array
def get_meme_input_file(pfms_,meme_path):
    pfms_ = np.array(pfms_)
    ppm = []
    for i in pfms_:
        ppm.append(i/np.sum(i,axis=0))
    
    with open(meme_path,'w')as f:
        f.write('MEME version 5.3.3')
        f.write('\n')
        f.write('\n')
        f.write('ALPHABET = ACGT')
        f.write('\n')
        f.write('\n')
        f.write('strands: + -')
        f.write('\n')
        f.write('\n')
        f.write('Background letter frequencies')
        f.write('\n')
        f.write('A 0.25 C 0.25 G 0.25 T 0.25')
        f.write('\n')
        f.write('\n')
        
        for i in range(len(ppm)):
            f.write('MOTIF\tmotif_ppm'+str(i))
            f.write('\n')
            f.write('letter-probability matrix: alength= 4 w= '+str(len(ppm[i].T)))
            f.write('\n')
            
            for j in ppm[i].T:
                f.write(str(j[0])+'\t'+str(j[1])+'\t'+str(j[2])+'\t'+str(j[3]))
                f.write('\n')
            f.write('\n')