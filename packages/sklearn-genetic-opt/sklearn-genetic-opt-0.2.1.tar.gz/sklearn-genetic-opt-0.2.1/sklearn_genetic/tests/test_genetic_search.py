from sklearn_genetic import GASearchCV
from sklearn.datasets import load_digits, load_boston
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils.validation import check_is_fitted
from sklearn.tree import DecisionTreeRegressor
from sklearn.cluster import KMeans
import pytest

data = load_digits()
label_names = data['target_names']
y = data['target']
X = data['data']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


def test_expected_ga_results():
    clf = SGDClassifier(loss='log', fit_intercept=True)
    generations = 8
    evolved_estimator = GASearchCV(clf,
                                   cv=3,
                                   scoring='accuracy',
                                   population_size=6,
                                   generations=generations,
                                   tournament_size=3,
                                   elitism=False,
                                   keep_top_k=4,
                                   continuous_parameters={'l1_ratio': (0, 1), 'alpha': (1e-4, 1)},
                                   categorical_parameters={'average': [True, False]},
                                   verbose=False,
                                   algorithm='eaSimple')

    evolved_estimator.fit(X_train, y_train)

    assert check_is_fitted(evolved_estimator) is None
    assert 'l1_ratio' in evolved_estimator.best_params
    assert 'alpha' in evolved_estimator.best_params
    assert 'average' in evolved_estimator.best_params
    assert len(evolved_estimator) == generations + 1  # +1 random initial population
    assert len(evolved_estimator.predict(X_test)) == len(X_test)
    assert evolved_estimator.score(X_train, y_train) >= 0
    assert len(evolved_estimator.decision_function(X_test)) == len(X_test)
    assert len(evolved_estimator.predict_proba(X_test)) == len(X_test)
    assert len(evolved_estimator.predict_log_proba(X_test)) == len(X_test)
    assert len(evolved_estimator.hof) == evolved_estimator.keep_top_k
    assert 'gen' in evolved_estimator[0]
    assert 'fitness_max' in evolved_estimator[0]
    assert 'fitness' in evolved_estimator[0]
    assert 'fitness_std' in evolved_estimator[0]
    assert 'fitness_min' in evolved_estimator[0]


def test_expected_ga_no_continuous():
    clf = DecisionTreeClassifier()
    generations = 10
    evolved_estimator = GASearchCV(clf,
                                   cv=3,
                                   scoring='accuracy',
                                   population_size=10,
                                   generations=generations,
                                   tournament_size=3,
                                   elitism=True,
                                   categorical_parameters={'criterion': ['gini', 'entropy']},
                                   integer_parameters={'max_depth': (2, 20), 'max_leaf_nodes': (2, 30)},
                                   verbose=False)

    evolved_estimator.fit(X_train, y_train)

    assert check_is_fitted(evolved_estimator) is None
    assert 'criterion' in evolved_estimator.best_params
    assert 'max_depth' in evolved_estimator.best_params
    assert 'max_leaf_nodes' in evolved_estimator.best_params


def test_expected_ga_no_categorical():
    clf = DecisionTreeClassifier()
    generations = 10
    evolved_estimator = GASearchCV(clf,
                                   cv=3,
                                   scoring='accuracy',
                                   population_size=8,
                                   generations=generations,
                                   tournament_size=3,
                                   elitism=True,
                                   continuous_parameters={'min_weight_fraction_leaf': (0, 0.5)},
                                   integer_parameters={'max_depth': (2, 20), 'max_leaf_nodes': (2, 30)},
                                   verbose=False)

    evolved_estimator.fit(X_train, y_train)

    assert check_is_fitted(evolved_estimator) is None
    assert 'min_weight_fraction_leaf' in evolved_estimator.best_params
    assert 'max_depth' in evolved_estimator.best_params
    assert 'max_leaf_nodes' in evolved_estimator.best_params


def test_negative_criteria():
    data_boston = load_boston()

    y_boston = data_boston['target']
    X_boston = data_boston['data']

    X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(X_boston, y_boston, test_size=0.33, random_state=42)

    clf = DecisionTreeRegressor()
    generations = 10
    evolved_estimator = GASearchCV(clf,
                                   cv=3,
                                   scoring='max_error',
                                   population_size=16,
                                   generations=generations,
                                   tournament_size=3,
                                   elitism=True,
                                   crossover_probability=0.9,
                                   mutation_probability=0.05,
                                   continuous_parameters={'ccp_alpha': (0, 1)},
                                   categorical_parameters={'criterion': ['mse', 'mae']},
                                   integer_parameters={'max_depth': (2, 20), 'min_samples_split': (2, 30)},
                                   criteria='min',
                                   n_jobs=-1)

    evolved_estimator.fit(X_train_b, y_train_b)

    assert check_is_fitted(evolved_estimator) is None
    assert 'ccp_alpha' in evolved_estimator.best_params
    assert 'criterion' in evolved_estimator.best_params
    assert 'max_depth' in evolved_estimator.best_params
    assert 'min_samples_split' in evolved_estimator.best_params
    assert len(evolved_estimator.predict(X_test_b)) == len(X_test_b)
    assert evolved_estimator.score(X_train_b, y_train_b) >= 0


def test_wrong_criteria():
    clf = SGDClassifier(loss='log', fit_intercept=True)
    generations = 8
    with pytest.raises(Exception) as excinfo:
        evolved_estimator = GASearchCV(clf,
                                       cv=3,
                                       scoring='accuracy',
                                       population_size=12,
                                       generations=generations,
                                       tournament_size=3,
                                       elitism=False,
                                       continuous_parameters={'l1_ratio': (0, 1), 'alpha': (1e-4, 1)},
                                       categorical_parameters={'average': [True, False]},
                                       verbose=False,
                                       criteria='maximization')
    assert str(excinfo.value) == "Criteria must be one of ['max', 'min'], got maximization instead"


def test_wrong_estimator():
    clf = KMeans()
    generations = 8
    with pytest.raises(Exception) as excinfo:
        evolved_estimator = GASearchCV(clf,
                                       cv=3,
                                       scoring='accuracy',
                                       population_size=12,
                                       generations=generations,
                                       tournament_size=3,
                                       elitism=False,
                                       continuous_parameters={'l1_ratio': (0, 1), 'alpha': (1e-4, 1)},
                                       categorical_parameters={'average': [True, False]},
                                       verbose=False,
                                       criteria='maximization')
    assert str(excinfo.value) == "KMeans() is not a valid Sklearn classifier or regressor"


def test_wrong_get_item():
    clf = SGDClassifier(loss='log', fit_intercept=True)
    generations = 8
    evolved_estimator = GASearchCV(clf,
                                   cv=3,
                                   scoring='accuracy',
                                   population_size=12,
                                   generations=generations,
                                   tournament_size=3,
                                   elitism=False,
                                   continuous_parameters={'l1_ratio': (0, 1), 'alpha': (1e-4, 1)},
                                   categorical_parameters={'average': [True, False]},
                                   verbose=False,
                                   criteria='max')
    with pytest.raises(Exception) as excinfo:
        value = evolved_estimator[0]
    assert str(excinfo.value) == "This GASearchCV instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator."


def test_iterator():
    clf = DecisionTreeClassifier()
    generations = 10
    evolved_estimator = GASearchCV(clf,
                                   cv=3,
                                   scoring='accuracy',
                                   population_size=15,
                                   generations=generations,
                                   tournament_size=3,
                                   elitism=True,
                                   continuous_parameters={'min_weight_fraction_leaf': (0, 0.5)},
                                   integer_parameters={'max_depth': (2, 20), 'max_leaf_nodes': (2, 30)},
                                   verbose=False)
    evolved_estimator.fit(X_train, y_train)

    i = iter(evolved_estimator)
    assert next(i) == evolved_estimator[0]
    assert next(i) == evolved_estimator[1]


def test_wrong_algorithm():
    clf = SGDClassifier(loss='log', fit_intercept=True)
    generations = 8
    evolved_estimator = GASearchCV(clf,
                                   cv=3,
                                   scoring='accuracy',
                                   population_size=12,
                                   generations=generations,
                                   tournament_size=3,
                                   elitism=False,
                                   continuous_parameters={'l1_ratio': (0, 1), 'alpha': (1e-4, 1)},
                                   categorical_parameters={'average': [True, False]},
                                   verbose=False,
                                   criteria='max',
                                   algorithm='genetic')
    with pytest.raises(Exception) as excinfo:
        evolved_estimator.fit(X_train, y_train)
    assert str(excinfo.value) == "The algorithm genetic is not supported, please select one from ['eaSimple', 'eaMuPlusLambda']"

