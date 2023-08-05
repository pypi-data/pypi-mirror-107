from sklearn_genetic.utils import plot_fitness_evolution
from sklearn_genetic import GASearchCV
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

data = load_boston()

y = data['target']
X = data['data']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

clf = DecisionTreeRegressor()

evolved_estimator = GASearchCV(clf,
                               cv=3,
                               scoring='r2',
                               population_size=8,
                               generations=60,
                               tournament_size=3,
                               elitism=True,
                               crossover_probability=0.9,
                               mutation_probability=0.05,
                               continuous_parameters={'ccp_alpha': (0, 1)},
                               categorical_parameters={'criterion': ['mse', 'mae']},
                               integer_parameters={'max_depth': (2, 20), 'min_samples_split': (2, 30)},
                               criteria='max',
                               n_jobs=-1)

evolved_estimator.fit(X_train, y_train)


def test_plot_created():
    plot = plot_fitness_evolution(evolved_estimator)

