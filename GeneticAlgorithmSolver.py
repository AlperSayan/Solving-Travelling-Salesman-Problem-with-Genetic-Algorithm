
import RouteManager as RM
import Route as RT
import random


class GeneticAlgorithmSolver:
    def __init__(self, cities, population_size=50, mutation_rate=0.2, tournament_size=10, elitism=False):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def evolve(self, routes):
        new_route = RM.RouteManager(self.cities, routes.population_size)
        elitism = 0

        if self.elitism:
            new_route.set_route(0, routes.find_best_route())
            elitism = 1

        for i in range(elitism, new_route.population_size):
            route_1 = self.tournament(routes)
            route_2 = self.tournament(routes)
            child_route = self.crossover(route_1, route_2)
            new_route.set_route(i, child_route)

        for i in range(elitism, new_route.population_size):
            self.mutate(new_route.get_route(i))

        return new_route

    def crossover(self, route_1, route_2):
        child = RT.Route(self.cities)

        init_state = int(random.random() * len(route_1))
        final_state = int(random.random() * len(route_2))

        for i in range(0, len(child)):
            if init_state < final_state and init_state < i < final_state:
                child.assign_city(i, route_1.get_city(i))
            elif init_state > final_state:
                if not (init_state > i > final_state):
                    child.assign_city(i, route_1.get_city(i))

        for i in range(0, len(route_2)):
            if not child.__contains__(route_2.get_city(i)):
                for j in range(0, len(child)):
                    if child.get_city(j) is None:
                        child.assign_city(j, route_2.get_city(i))
                        break

        return child

    def mutate(self, route):
        for route_1 in range(0, len(route)):
            if random.random() < self.mutation_rate:
                route_2 = int(len(route) * random.random())

                mutate_city_1 = route.get_city(route_1)
                mutate_city_2 = route.get_city(route_2)

                route.assign_city(route_2, mutate_city_1)
                route.assign_city(route_1, mutate_city_2)

    def tournament(self, routes):
        tournament_route = RM.RouteManager(self.cities, self.tournament_size)
        for i in range(0, self.tournament_size):
            random_val = int(random.random() * routes.population_size)
            tournament_route.set_route(i, routes.get_route(random_val))
        best_route = tournament_route.find_best_route()
        return best_route
