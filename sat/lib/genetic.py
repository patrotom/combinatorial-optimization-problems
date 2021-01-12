import copy
import random
import numpy as np
from timeit import default_timer as timer

from sat.lib.solution import Solution


class Genetic:
    def __init__(self, inst, opts):
        self.inst = inst
        self.opts = opts
        self.sol = Solution(inst.vars_num)

    def run(self):
        start = timer()
        self.__run()
        end = timer()

        self.sol.time = end - start
        best_indv = self.__find_elite()
        self.sol.w_sum = best_indv.fitness
        self.sol.conf = best_indv.conf
        self.sol.rel_err = abs(self.sol.w_sum - self.inst.opt_sum) / \
                max(self.inst.opt_sum, self.sol.w_sum)

    def __run(self):
        self.__init_generation()

        for it in range(self.opts["g"]):
            gen = []

            self.elite = copy.deepcopy(self.__find_elite())
            gen.append(self.elite)
            while len(gen) < len(self.prev_gen):
                parents = self.__tournament()
                offsprings = self.__crossover(parents)
                offsprings = self.__mutate(offsprings)
                gen += offsprings

            self.prev_gen = gen
            self.__pandemic()
            if it < int(self.opts["g"] / 2):
                self.__war()

    def __init_generation(self):
        self.prev_gen = []
        pop_size = (self.opts["p"], self.inst.vars_num)
        confs = np.random.randint(2, size=pop_size).tolist()

        for conf in confs:
            fitness = self.__calc_fitness(conf)
            self.prev_gen.append(Individual(conf, fitness))

        self.max_fitness = self.__find_elite().fitness
        self.stale_cnt = 0

    def __tournament(self):
        sample1 = random.sample(self.prev_gen, k=5)
        sample2 = random.sample(self.prev_gen, k=5)

        tour1 = self.__find_fittest_two(sample1)
        tour2 = self.__find_fittest_two(sample2)
        
        parents = self.__find_fittest_two(tour1 + tour2)

        return parents

    def __crossover(self, parents):
        if random.random() > self.opts["c"]:
            return copy.deepcopy(parents)

        p1, p2 = sorted(random.sample(list(range(self.inst.vars_num)), k=2))
        p_conf1, p_conf2 = parents[0].conf, parents[1].conf

        o_conf1 = p_conf1[:p1] + p_conf2[p1:p2] + p_conf1[p2:]
        o_conf2 = p_conf2[:p1] + p_conf1[p1:p2] + p_conf2[p2:]
        fitness1 = self.__calc_fitness(o_conf1)
        fitness2 = self.__calc_fitness(o_conf2)
        i1 = Individual(o_conf1, fitness1)
        i2 = Individual(o_conf2, fitness2)

        return [i1, i2]

    def __mutate(self, offsprings):
        for offspring in offsprings:
            if random.random() > self.opts["m"]:
                continue
            rand_idx = random.choice(list(range(self.inst.vars_num)))
            offspring.conf[rand_idx] = int(not offspring.conf[rand_idx])
            offspring.fitness = self.__calc_fitness(offspring.conf)
        
        return offsprings

    def __find_fittest_two(self, sample):
        sample = sorted(sample, key=lambda x: x.fitness, reverse=True)
        return [sample[0], sample[1]]

    def __find_elite(self):
        return max(self.prev_gen, key=lambda x: x.fitness)

    def __pandemic(self):
        if not self.opts["pan"]:
            return

        if self.stale_cnt < 50:
            if self.elite.fitness == self.max_fitness:
                self.stale_cnt += 1
            else:
                self.max_fitness = self.elite.fitness
                self.stale_cnt = 0
            return

        to_wipe = int(self.opts["p"] / 2)
        kept = sorted(
            self.prev_gen, key=lambda x: x.fitness, reverse=True
        )[:to_wipe]

        pop_size = (self.opts["p"] - to_wipe, self.inst.vars_num)
        confs = np.random.randint(2, size=pop_size).tolist()

        for conf in confs:
            fitness = self.__calc_fitness(conf)
            kept.append(Individual(conf, fitness))

        self.prev_gen = kept
        self.stale_cnt = 0

    def __war(self):
        if not self.opts["war"]:
            return

        if self.stale_cnt < 50:
            if self.elite.fitness == self.max_fitness:
                self.stale_cnt += 1
            else:
                self.max_fitness = self.elite.fitness
                self.stale_cnt = 0
            return

        to_wipe = int(self.opts["p"] / 2)

        kept = random.sample(self.prev_gen, k=to_wipe)

        pop_size = (self.opts["p"] - to_wipe, self.inst.vars_num)
        confs = np.random.randint(2, size=pop_size).tolist()

        for conf in confs:
            fitness = self.__calc_fitness(conf)
            kept.append(Individual(conf, fitness))

        self.prev_gen = kept
        self.stale_cnt = 0

    def __calc_fitness(self, conf):
        fitness = -self.inst.cls_num
        for clause in self.inst.clauses:
            for v in clause:
                idx = abs(v) - 1
                val = int(not conf[idx]) if v < 0 else conf[idx]
                if val == 1:
                    fitness += 1
                    break
        
        if fitness == 0:
            return sum([a * b for a, b in zip(conf, self.inst.weights)])
        elif fitness < 0:
            return fitness


class Individual():
    def __init__(self, conf, fitness):
        self.conf = conf
        self.fitness = fitness
