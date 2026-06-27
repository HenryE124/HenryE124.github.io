import random
import matplotlib.pyplot as plt

try:
    pop=int(input("Enter a population size: "))
    af1=float(input("Enter an allele frequency of the dominant allele: "))
    gen=int(input("Enter a number of generations: "))
    numsim=int(input("Enter a number of simulation runs: "))
    lif=float(input("Enter an average life expectancy in generations: "))
    kid=float(input("Enter the average number of kids per female: "))
    cc=int(input("Enter a carrying capcity for the population: "))
except ValueError:
    print("Enter valid numbers.")
if af1 >= 1 or af1 <= 0:
    raise Exception("Enter a valid allele frequency between 0 and 1")
if pop == 0 or af1 == 0 or gen == 0 or numsim == 0 or cc==0:
    raise Exception("no inputs can equal 0")

class person:

    def __init__(self, parm, parf):
        self._parm = parm
        self._parf = parf
        self._gender = random.randint(0,1)
        self._age = 0
        if parm is None and parf is None:
            rand1 = random.randint(1,100)
            rand2 = random.randint(1,100)
            if rand1 <= af1*100:
                self._allele1 = 'A'
            else:
                self._allele1 = 'a'
            if rand2 <= af1*100:
                self._allele2 = 'A'
            else:
                self._allele2 = 'a'
        else:
            self._allele1 = parm.get_allele()
            self._allele2 = parf.get_allele()


    def get_allele(self):
        return random.choice([self._allele1, self._allele2])

    def addtopop(self):
        population += self


plt.figure()
plt.title("Allele A Frequency Over Time")
plt.xlabel("Generation")
plt.ylabel("Frequency")
plt.ylim(0, 1)
plt.xlim(0,gen)



for g in range(numsim):
    population = new_population = []
    phistory = []
    history = []
    for h in range(pop):
        population.append(person(None, None))
    for i in range(gen):
        homd = homr = het = 0
        males = [p for p in population if p._gender == 1]
        for j in population[:]:
            j._age += 1
            rand1 = random.uniform(lif-1, lif+1)
            if rand1 >= j._age:
                new_population.append(j)
                if j._gender == 0  and j._age == 2 and males:
                    guy = random.choice(males)
                    rand2 = random.uniform(0,kid*2)
                    for k in range(round(rand2)):
                        new_population.append(person(guy, j))
        if len(new_population) > cc:
            new_population = new_population[-cc:]
        population = new_population
        for l in population:
            if l._allele1 == 'A' and l._allele2 == 'A':
                homd += 1
            elif l._allele1 == 'a' and l._allele2 == 'a':
                homr += 1
            else:
                het += 1
        print("Population size: " + str(len(population)) + ' Generation: ' + str(i+1)
        + " Homozygous Dominants: " + str(homd) + " Homozygous Recessives: " + str(homr)
        + " Heterozygotes: " + str(het))
        history.append([((homd*2 + het)/(2*(homd + het + homr)))])
        phistory.append(len(population))
        plt.plot(history)
        
    print("END OF TRIAL " + str(g + 1))


plt.show()




