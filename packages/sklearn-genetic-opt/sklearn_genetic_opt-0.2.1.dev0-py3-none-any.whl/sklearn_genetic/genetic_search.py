import numpy as np
import random
from deap import base, creator, tools, algorithms
from sklearn.base import clone, ClassifierMixin, RegressorMixin
from sklearn.model_selection import cross_val_score
from sklearn.base import is_classifier, is_regressor
from sklearn.utils.metaestimators import if_delegate_has_method
from sklearn.utils.validation import check_array, check_is_fitted
from sklearn.metrics import check_scoring
from sklearn.exceptions import NotFittedError
from sklearn_genetic.parameters import Algorithms, Criteria


class GASearchCV(ClassifierMixin, RegressorMixin):
    """
    Hyper parameter tuning using generic algorithms.
    """

    def __init__(self,
                 estimator,
                 cv: int = 3,
                 scoring=None,
                 population_size: int = 20,
                 generations: int = 40,
                 crossover_probability: float = 0.8,
                 mutation_probability: float = 0.1,
                 tournament_size: int = 3,
                 elitism: bool = True,
                 verbose: bool = True,
                 keep_top_k: int = 1,
                 continuous_parameters: dict = None,
                 categorical_parameters: dict = None,
                 integer_parameters: dict = None,
                 criteria: Criteria = 'max',
                 algorithm: Algorithms = 'eaMuPlusLambda',
                 n_jobs: int = 1):
        """

        Parameters
        ----------
        estimator: Sklearn Classifier or Regressor
        cv: int, number of splits used for calculating cross_val_score
        scoring: string, Scoring function to use as fitness value
        population_size: int, size of the population
        crossover_probability: float, probability of crossover operation
        mutation_probability: float, probability of child mutation
        tournament_size: number of chromosomes to perform tournament selection
        elitism: bool, if true takes the |tournament_size| best solution to the next generation
        verbose: bool, if true, shows the metrics on the optimization routine
        keep_top_k: int, number of best solutions to keep in the hof object
        generations: int, number of generations to run the genetic algorithm
        continuous_parameters: dict, continuous parameters to tune, expected a list or tuple with the range (min,max) to search
        categorical_parameters: dict, categorical parameters to tune, expected a list with the possible options to choose
        integer_parameters: dict, integers parameters to tune, expected a list or tuple with the range (min,max) to search
        criteria: str, 'max' if a higher scoring metric is better, 'min' otherwise
        algorithm: str, accepts 'eaSimple' or 'eaMuPlusLambda' as optimization routines. See more details in the deap algorithms documentation
        n_jobs: int, Number of jobs to run in parallel during the cross validation scoring
        """

        self.estimator = clone(estimator)
        self.toolbox = base.Toolbox()
        self.cv = cv
        self.scoring = scoring
        self.pop_size = population_size
        self.generations = generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.tournament_size = tournament_size
        self.elitism = elitism
        self.verbose = verbose
        self.keep_top_k = keep_top_k
        self.algorithm = algorithm
        self.n_jobs = n_jobs
        self.creator = creator
        self.logbook = None
        self.history = None
        self.X = None
        self.Y = None
        self.best_params = None
        self.hof = None
        self.X_predict = None

        if not is_classifier(self.estimator) and not is_regressor(self.estimator):
            raise ValueError("{} is not a valid Sklearn classifier or regressor".format(self.estimator))

        if criteria not in Criteria.list():
            raise ValueError(f"Criteria must be one of {Criteria.list()}, got {criteria} instead")
        elif criteria == Criteria.max.value:
            self.criteria_sign = 1
        elif criteria == Criteria.min.value:
            self.criteria_sign = -1

        if not continuous_parameters:
            self.continuous_parameters = {}
        else:
            self.continuous_parameters = continuous_parameters

        if not categorical_parameters:
            self.categorical_parameters = {}
        else:
            self.categorical_parameters = categorical_parameters

        if not integer_parameters:
            self.integer_parameters = {}
        else:
            self.integer_parameters = integer_parameters

        self.parameters = [*list(self.continuous_parameters.keys()),
                           *list(self.integer_parameters.keys()),
                           *list(self.categorical_parameters.keys())]

        self.continuous_parameters_range = (0, len(self.continuous_parameters))
        self.integer_parameters_range = (self.continuous_parameters_range[1],
                                         self.continuous_parameters_range[1] + len(self.integer_parameters))
        self.categorical_parameters_range = (self.integer_parameters_range[1],
                                             self.integer_parameters_range[1] + len(self.categorical_parameters))

    def register(self):

        self.creator.create("FitnessMax", base.Fitness, weights=[1.0])
        self.creator.create("Individual", list, fitness=creator.FitnessMax)

        attributes = []

        for key, value in self.continuous_parameters.items():
            self.toolbox.register(f"{key}", random.uniform, value[0], value[1])
            attributes.append(getattr(self.toolbox, key))

        for key, value in self.integer_parameters.items():
            self.toolbox.register(f"{key}", random.randint, value[0], value[1])
            attributes.append(getattr(self.toolbox, key))

        for key, value in self.categorical_parameters.items():
            self.toolbox.register(f"{key}", random.choice, value)
            attributes.append(getattr(self.toolbox, key))

        IND_SIZE = 1

        self.toolbox.register("individual",
                              tools.initCycle, creator.Individual,
                              tuple(attributes), n=IND_SIZE)

        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", self.mutate)
        if self.elitism:
            self.toolbox.register("select", tools.selTournament, tournsize=self.tournament_size)
        else:
            self.toolbox.register("select", tools.selRoulette)

        self.toolbox.register("evaluate", self.evaluate)

    def mutate(self, individual):
        gen = random.randrange(0, len(self.parameters))
        parameter_index = self.parameters[gen]

        if gen in range(self.continuous_parameters_range[0], self.continuous_parameters_range[1]):
            parameter = self.continuous_parameters[parameter_index]
            individual[gen] = random.uniform(parameter[0], parameter[1])
        elif gen in range(self.integer_parameters_range[0], self.integer_parameters_range[1]):
            parameter = self.integer_parameters[parameter_index]
            individual[gen] = random.randint(parameter[0], parameter[1])
        elif gen in range(self.categorical_parameters_range[0], self.categorical_parameters_range[1]):
            parameter = self.categorical_parameters[parameter_index]
            individual[gen] = random.choice(parameter)

        return [individual]

    def evaluate(self, individual):
        current_generation_params = {key: individual[n] for n, key in enumerate(self.parameters)}

        self.estimator.set_params(**current_generation_params)
        cv_scores = cross_val_score(self.estimator,
                                    self.X_, self.Y_,
                                    cv=self.cv,
                                    scoring=self.scoring,
                                    n_jobs=self.n_jobs)
        score = np.mean(cv_scores)

        current_generation_params['score'] = score

        self.logbook.record(parameters=current_generation_params)

        return [self.criteria_sign * score]

    @if_delegate_has_method(delegate='estimator')
    def fit(self, X, y):
        """
        Main method of GASearchCV, optimize the hyper parameters of the given estimator
        Parameters
        ----------
        X: training samples to learn from
        y: training labels for each X obversation

        Returns

        fitted sklearn Regressor or Classifier
        -------

        """
        scorer = check_scoring(self.estimator, scoring=self.scoring)

        self.X_ = X
        self.Y_ = y

        self.register()

        pop = self.toolbox.population(n=self.pop_size)
        hof = tools.HallOfFame(self.keep_top_k)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("fitness", np.mean)
        stats.register("fitness_std", np.std)
        stats.register("fitness_max", np.max)
        stats.register("fitness_min", np.min)

        self.logbook = tools.Logbook()

        pop, log = self._select_algorithm(pop=pop, stats=stats, hof=hof)

        self.best_params = {key: hof[0][n] for n, key in enumerate(self.parameters)}

        self.hof = {k: {key: hof[k][n] for n, key in enumerate(self.parameters)} for k in range(self.keep_top_k)}

        self.history = {"gen": log.select("gen"),
                        "fitness": log.select("fitness"),
                        "fitness_std": log.select("fitness_std"),
                        "fitness_max": log.select("fitness_max"),
                        "fitness_min": log.select("fitness_min")}

        self.estimator.set_params(**self.best_params)
        self.estimator.fit(self.X_, self.Y_)

        del self.creator.FitnessMax
        del self.creator.Individual

        return self

    def _select_algorithm(self, pop, stats, hof):

        if self.algorithm == Algorithms.eaSimple.value:

            pop, log = algorithms.eaSimple(pop, self.toolbox,
                                           cxpb=self.crossover_probability,
                                           stats=stats,
                                           mutpb=self.mutation_probability,
                                           ngen=self.generations,
                                           halloffame=hof,
                                           verbose=self.verbose)

        elif self.algorithm == Algorithms.eaMuPlusLambda.value:

            pop, log = algorithms.eaMuPlusLambda(pop, self.toolbox,
                                                 mu=self.generations,
                                                 lambda_=2 * self.generations,
                                                 cxpb=self.crossover_probability,
                                                 stats=stats,
                                                 mutpb=self.mutation_probability,
                                                 ngen=self.generations,
                                                 halloffame=hof,
                                                 verbose=self.verbose)

        else:
            raise ValueError(
                f"The algorithm {self.algorithm} is not supported, please select one from {Algorithms.list()}")

        return pop, log

    @property
    def fitted(self):
        try:
            check_is_fitted(self.estimator)
            is_fitted = True
        except Exception as e:
            is_fitted = False

        has_history = bool(self.history)
        return all([is_fitted, has_history])

    def __getitem__(self, index):
        """

        Parameters
        ----------
        index: slice required to get

        Returns
        -------
        Best solution of the iteration corresponding to the index number
        """
        if not self.fitted:
            raise NotFittedError(
                f"This GASearchCV instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.")

        return {"gen": self.history['gen'][index],
                "fitness": self.history['fitness'][index],
                "fitness_std": self.history['fitness_std'][index],
                "fitness_max": self.history['fitness_max'][index],
                "fitness_min": self.history['fitness_min'][index]}

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        """
        Returns
        -------
        Iteration over the statistics found in each generation
        """
        if self.n < self.generations + 1:
            result = self.__getitem__(self.n)
            self.n += 1
            return result
        else:
            raise StopIteration

    def __len__(self):
        """
        Returns
        -------
        Number of generations fitted
        """
        return self.generations + 1

    @if_delegate_has_method(delegate='estimator')
    def predict(self, X):
        X = check_array(X)
        return self.estimator.predict(X)

    @if_delegate_has_method(delegate='estimator')
    def score(self, X, y):
        X = check_array(X)
        return self.estimator.score(X, y)

    @if_delegate_has_method(delegate='estimator')
    def decision_function(self, X):
        X = check_array(X)
        return self.estimator.decision_function(X)

    @if_delegate_has_method(delegate='estimator')
    def predict_proba(self, X):
        X = check_array(X)
        return self.estimator.predict_proba(X)

    @if_delegate_has_method(delegate='estimator')
    def predict_log_proba(self, X):
        X = check_array(X)
        return self.estimator.predict_log_proba(X)
