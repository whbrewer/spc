import sys, math, random
from bio import DNA

class CAI(DNA):
    """Class representing DNA as a string sequence."""
    baselists = [['Val','GTT','GTC','GTA','GTG'],
                 ['Ala','GCT','GCC','GCA','GCG'],
                 ['Asp','GAT','GAC'],
                 ['Glu','GAA','GAG'],
                 ['Gly','GGT','GGC','GGA','GGG'],
                 ['Phe','TTT','TTC'],
                 ['Leu','TTG','TTA','CTT','CTC','CTA','CTG'],
                 ['Lle','ATT','ATC','ATA'],
                 ['Met','ATG'],
                 ['Ser','TCT','TCC','TCA','TCG','AGT','AGC'],
                 ['Pro','CCT','CCC','CCA','CCG'],
                 ['Thr','ACT','ACC','ACA','ACG'],
                 ['Tyr','TAT','TAC'],
                 ['His','CAT','CAC'],
                 ['Gln','CAA','CAG'],
                 ['Asn','AAT','AAC'],
                 ['Lys','AAA','AAG'],
                 ['Arg','AGA','AGG','CGG','CGA','CGC','CGT'],
                 ['Trp','TGG'],
                 ['Cys','TGT','TGC'],
                 ['Stop','TAA','TAG','TGA']]

    def __init__(self, data, end):
        self.base = ['A','T','C','G']
        self.seq = ''
        self.p_base = []
        self.p_pair = []
        self.p_codon = {}
        self.max_C = {}
        self.end = int(end)

        self.n = len(data)
        self.output = ''

        self.seq = data
        self.d = []
        self.cal = []

    def create(self):
        self.seq = ''
        for i in range(self.n):
            rnum = random.random()
            if rnum < self.p_base[0]:
                self.seq = self.seq+'A'
            if rnum > self.p_base[0] and rnum<self.p_base[0]+self.p_base[1]:
                self.seq = self.seq+'T'
            if rnum > self.p_base[0]+self.p_base[1] and rnum<self.p_base[0]+self.p_base[1]+self.p_base[2]:
                self.seq = self.seq+'C'
            if rnum > self.p_base[0]+self.p_base[1]+self.p_base[2] and rnum<self.p_base[0]+self.p_base[1]+self.p_base[2]+self.p_base[3]:
                self.seq = self.seq+'G'

    def occurrence(self):
        """calculate the probability of each base"""
        for i in range(4):
            self.p_base.append(self.seq.count(self.base[i])/float(len(self.seq)))

        for i in range(4):
            for j in range(4):
                self.p_pair.append(self.p_base[i]*self.p_base[j])
                #print('%s  :  %0.3f'%(self.base[i]+self.base[j],self.p_pair[i*4+j]*100)+'%')

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    self.p_codon[self.base[i]+self.base[j]+self.base[k]] = self.p_base[i]*self.p_base[j]*self.p_base[k]
                    #print('%s : %d :  %0.3f'%(self.base[i]+self.base[j]+self.base[k],i*16+j*4+k,self.p_codon[self.base[i]+self.base[j]+self.base[k]]))

        return self.p_base

    def codon_analysis(self):
        for i in range(len(self.baselists)):
            sumv = maxv = 0
            for j in range(1, len(self.baselists[i])):
                sumv += self.p_codon[self.baselists[i][j]]
            for j in range(1, len(self.baselists[i])):
                self.p_codon[self.baselists[i][j]] = self.p_codon[self.baselists[i][j]]/sumv
                if maxv < self.p_codon[self.baselists[i][j]]:
                    maxv = self.p_codon[self.baselists[i][j]]
            self.max_C[self.baselists[i][0]] = maxv
        
    def generate_dinucleotide(self):
        for i in range(4):
            for j in range(4):
                self.d.append(self.base[i]+self.base[j])

    def calculate_E(self):
        pa1 = self.seq.count('a')/float(len(self.seq))
        pt1 = self.seq.count('t')/float(len(self.seq))
        pc1 = self.seq.count('c')/float(len(self.seq))
        pg1 = self.seq.count('g')/float(len(self.seq))
        self.list = [pa1,pt1,pc1,pg1]
        for i in range(4):
            for j in range(4):
                c = self.list[i]*self.list[j]
                self.cal.append(c)

    # def observed(self):
    #     for i in range(16):
    #         E = (len(self.seq)-1)*self.cal[i]
    #         x2 = (self.seq.count(self.d[i])-E)**2/E
    #         r = self.d[i]
    #         if (r[0] == r[1]):
    #             c = 1 + 2*math.sqrt(self.cal[i]) - 3*self.cal[i]
    #         else:
    #             c = 1 - 3*self.cal[i]
    #         m = x2/c
    #         #print('%s : E = %f  x2/c = %f'%(self.d[i],E,m))


    def codons(self, seq):
        """Return list of codons for the dna string"""
        s = seq
        end = len(s) - (len(s) % 3) - 1
        codons = [ s[i:i+3] for i in range(0, end, 3) ]
        return codons

    # Calculate the value of CAI of the given sequence
    def CAI(self):             
        query = self.seq[0:self.end]
        qlist = self.codons(query)
        cail = []
        pristr = ''
        output = ''

        # Match every codon of the given sequence with the codons of amino 
        # acid represented in dictionary
        for item in qlist:
            target = []
            for cod in self.baselists:
                for don in cod:
                    if item == don:
                        target = cod
            cail.append(target)
        i = 0
        caipro = 1

        # Call the value of percentage from dictionary and calculate the CAI
        for item in cail:       
            itemcaipro = self.p_codon[qlist[i]]/self.max_C[item[0]]
            self.output += str(qlist[i]) + ': ' + str(itemcaipro)[0:5] + '\n'
            caipro *= itemcaipro
            i += 1
        caipro = pow(caipro, 3/self.end)
        output +=  "\nResult     :     CAI  =  " + str(caipro)[0:5] + '\n'

        return output

    def show(self):
        query = self.seq[0:self.end]
        qlist = self.codons(query)
        out = []
        pristr = ''
        output = "CODON ANALYSIS\n\n"

        # Search the codons of a given sequence with the element of amino acid
        for item in qlist:            
            target = []
            for cod in self.baselists:
                for don in cod:
                    if item == don:
                        target = cod
            out.append(target)
        for item in qlist:
            pristr += item + '\t'
        output += str(pristr) + '\n'

        # Output the proportions of all of codons belonging to the same amino acid which has the analyzing codon 
        for i in range(1,7):           
            pristr = ''    
            for item in out:
                try:
                    pristr += str(self.p_codon[item[i]])[0:5] + '\t'
                except:
                    pristr += '\t'
            output += str(pristr)

        # Output all codons belonging to the same amino acid which has the analyzing codon            
        for i in range(1, 7):           
            pristr = ''    
            for item in out:
                try:
                    pristr += item[i] + '\t'
                except:
                    pristr += '\t'
            output += str(pristr)

        return output

if __name__  ==  "__main__":
    s = "GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCATTTGGTATTTTCGTCTGGGGGGTATGCACGCGATAGCATTGCGAGACGCTGGAGCCGGAGCACCCTATGTCGCAGTATCTGTCTTTGATTCCTGCCTCATCCTATTATTTATCGCACCTACGTTCAATATTACAGGCGAACATACTTACTAAAGTGTGTTAATTAATTAATGCTTGTAGGACATAATAATA" 
    cai = CAI(s, 100)
    cai.occurrence()
    cai.codon_analysis()
    print cai.show()
    print cai.CAI()
    print cai.output
