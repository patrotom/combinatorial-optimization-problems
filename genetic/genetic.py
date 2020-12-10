#!/usr/bin/env python3

import sys
import os
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import random
import copy
import numpy as np
from timeit import default_timer as timer

from lib.solution import Solution
from lib.instance import Instance
from lib.item import Item


class Genetic():
    def __init__(self, inst, opts):
        self.inst = inst
        self.opts = opts
        self.sol = Solution()

    def run(self):
        start = timer()
        self.__run()
        end = timer()

        self.sol.time = end - start
        self.sol.price = self.sol.gen_data["max"][-1]
        self.sol.rel_err = abs(self.sol.price - self.inst.opt_price) / \
                max(self.inst.opt_price, self.sol.price)

    def __run(self):
        self.__init_generation()

        for _ in range(self.opts["g"]):
            gen = []

            gen.append(self.__find_elite())
            while len(gen) < len(self.prev_gen):
                parents = self.__tournament()
                offsprings = self.__crossover(parents)
                offsprings = self.__mutate(offsprings)
                gen += offsprings

            self.prev_gen = gen
            self.__add_sol_data()

    def __init_generation(self):
        self.prev_gen = []
        pop_size = (self.opts["p"], self.inst.size)
        confs = np.random.randint(2, size=pop_size).tolist()

        for conf in confs:
            fitness = self.__calc_fitness(conf)
            self.prev_gen.append(Individual(conf, fitness))
        
        self.__add_sol_data()
    
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
        
        p1, p2 = sorted(random.sample(list(range(self.inst.size)), k=2))
        p_conf1, p_conf2 = parents[0].conf, parents[1].conf

        o_conf1 = p_conf1[:p1] + p_conf2[p1:p2] + p_conf1[p1:]
        o_conf2 = p_conf2[:p2] + p_conf1[p1:p2] + p_conf2[p2:]
        fitness1 = self.__calc_fitness(o_conf1)
        fitness2 = self.__calc_fitness(o_conf2)
        i1 = Individual(o_conf1, fitness1)
        i2 = Individual(o_conf2, fitness2)

        return [i1, i2]

    def __mutate(self, offsprings):
        for offspring in offsprings:
            if random.random() > self.opts["m"]:
                continue
            rand_idx = random.choice(list(range(self.inst.size)))
            offspring.conf[rand_idx] = int(not offspring.conf[rand_idx])
            offspring.fitness = self.__calc_fitness(offspring.conf)
        
        return offsprings

    def __find_fittest_two(self, sample):
        sample = sorted(sample, key=lambda x: x.fitness, reverse=True)
        return [sample[0], sample[1]]

    def __find_elite(self):
        return copy.deepcopy(max(self.prev_gen, key=lambda x: x.fitness))

    def __calc_fitness(self, conf):
        w_sum = self.inst.calc_weight(conf)
        if w_sum <= self.inst.capacity:
            return self.inst.calc_price(conf)
        else:
            return 0
    
    def __add_sol_data(self):
        mean_f = np.mean(list(map(lambda x: x.fitness, self.prev_gen)))
        max_f = max(self.prev_gen, key=lambda x: x.fitness).fitness

        self.sol.gen_data["mean"].append(mean_f)
        self.sol.gen_data["max"].append(max_f)


class Individual():
    def __init__(self, conf, fitness):
        self.conf = conf
        self.fitness = fitness
