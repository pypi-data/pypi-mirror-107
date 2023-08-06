# Library imports
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import traceback
pd.options.mode.chained_assignment = None

random_seed = 2021
np.random.seed(random_seed)


def optimize_rfc(x_train, x_test, y_train, y_test, params={}, error_metric="accuracy_score", population_size=50,
                 number_of_generation=10, mutation_rate=0.05, random_seed=2021):
    try:
        rf_parameters = []

        if "n_estimators" in params.keys():
            rf_parameters.append(params["n_estimators"])
        else:
            rf_parameters.append(np.arange(1, 1000))

        if "max_features" in params.keys():
            rf_parameters.append(params["max_features"])
        else:
            rf_parameters.append(['sqrt', 'auto', 'log2', None])

        if "min_samples_leaf" in params.keys():
            rf_parameters.append(params["min_samples_leaf"])
        else:
            rf_parameters.append(np.arange(2, 16))

        if "max_depth" in params.keys():
            rf_parameters.append(params["max_depth"])
        else:
            rf_parameters.append(np.arange(2, 20))

        if "criterion" in params.keys():
            rf_parameters.append(params["criterion"])
        else:
            rf_parameters.append(["gini", "entropy"])

        if "oob_score" in params.keys():
            rf_parameters.append(params["oob_score"])
        else:
            rf_parameters.append([True, False])

        obj = optimizer()
        model, row = obj.best_estimator(x_train, x_test, y_train, y_test, rf_parameters, error_metric,
                                        population_size, number_of_generation, mutation_rate, random_seed)
        return model, row
    except Exception as e:
        print(e)
        traceback.print_exc()


class optimizer():
    def best_estimator(self, x_train, x_test, y_train, y_test, rf_parameters, error_metric, population_size,
                       number_of_generation, mutation_rate, random_seed):

        # -----------------------------------------   Parameter Assertions   -----------------------------------------

        assert type(x_train) is pd.core.frame.DataFrame, 'x_train must be a DataFrame'
        assert type(x_test) is pd.core.frame.DataFrame, 'x_train must be a DataFrame'
        assert type(population_size) is int and population_size > 0, 'Population size must be a positive integer.'
        assert population_size % 2 == 0, 'Population size must be even.'
        assert type(number_of_generation) is int and number_of_generation > 0, \
            'Number of generations must be a non-negative integer.'
        assert type(mutation_rate) is float and 0.0 <= mutation_rate <= 1.0, \
            'Mutation rate must be a float between 0.0 and 1.0.'

        # --------------------------------------------   Model function   --------------------------------------------
        objective_function = lambda i: self.objective(error_metric, i, x_train, x_test, y_train, y_test,
                                                      random_seed=random_seed)
        # ------------------------------------------------------------------------------------------------------------

        population = pd.DataFrame()
        np.random.seed(random_seed)
        population['n_estimators'] = np.random.choice(rf_parameters[0], size=population_size)
        population['max_features'] = np.random.choice(rf_parameters[1], size=population_size)
        population['min_samples_leaf'] = np.random.choice(rf_parameters[2], size=population_size)
        population['max_depth'] = np.random.choice(rf_parameters[3], size=population_size)
        population['criterion'] = np.random.choice(rf_parameters[4], size=population_size)
        population['oob_score'] = np.random.choice(rf_parameters[5], size=population_size)

        population['score'] = population.apply(objective_function, axis=1)

        for g in range(number_of_generation):
            # Pair the population for breeding
            pairs = self.match(population, random_seed)

            # Generate the children
            children = self.crossover(pairs, random_seed)
            if 'score' in children.columns:
                children.drop('score', axis=1, inplace=True)

            # Generate the mutants
            mutants = self.mutate(children, mutation_rate, rf_parameters, random_seed)

            # Collect the population removing any duplicates.
            population = population.append([children, mutants], ignore_index=True, sort=False) \
                .drop_duplicates(subset=children.columns)

            # Score the population, sort it, and terminate the bottom
            population.loc[:, error_metric] = population.apply(objective_function, axis=1)
            population = population.sort_values(by=['score'], ascending=False).iloc[:population_size]

            output_params = population.iloc[0]
            output_params[error_metric] = round(output_params['score'], 2)
            output_params.drop('score', inplace=True)

        return [self.get_model(population.loc[population[error_metric].idxmax()]), output_params]

    def match(self, population, random_seed):
        '''
        Samples from population with higher scores having higher probability of selection.
        '''

        np.random.seed(random_seed)
        length = population.shape[0]
        prob = population['score'] / population['score'].sum()

        indices = np.random.choice(np.arange(length), p=prob, size=length)
        return population.iloc[indices]

    def crossover(self, pairs, random_seed):
        '''
        Performs a random crossover with the entire population as an input.
        '''

        np.random.seed(random_seed)
        length, width = pairs.shape
        width -= 1

        # i is an array which maps indices randomly either to themselves or their pair.
        a = np.random.choice((0, 1), size=length * width)
        a[np.arange(1, length * width, 2)] *= -1
        i = np.arange(length * width) + a

        # Convert the population to a list of genes, and map each gene to itself or its pair using i.
        gene_list = np.array(pairs.drop('score', axis=1)).reshape(-1, order='F')
        return pd.DataFrame(gene_list[i].reshape((-1, width), order='F'), columns=pairs.columns[:-1])

    def mutate(self, population, mutation_rate, rf_parameters, random_seed):
        '''
        Mutate the population with a given mutation rate.
        '''

        length, width = population.shape
        np.random.seed(random_seed)

        pop_array = np.array(population).reshape(-1, order='F')

        # List of all the indices in the 1d gene array which should be changed.
        change_indices = np.random.choice(
            np.arange(length * width),
            size=int(mutation_rate * length * width),
            replace=False
        )

        # Get a list new_values that contains random values for the corresponding index in mut_array.
        change_indices.sort()
        c = [np.random.choice(rf_parameters[i], size=np.logical_and
        (i * length <= change_indices, change_indices < (i + 1) * length).sum()) for i in range(width)]
        new_values = np.concatenate(c)

        # Set the values in the population array at the change indices to the new values.
        pop_array[change_indices] = new_values
        mutants = pd.DataFrame(pop_array.reshape((-1, width), order='F'))
        mutants.columns = population.columns

        return mutants

    def get_model(self, row, random_seed=2021):
        '''
        Return the model specified by the given row.
        '''

        return RandomForestClassifier(
            n_estimators=row[0],
            max_features=row[1],
            min_samples_leaf=row[2],
            max_depth=row[3],
            criterion=row[4],
            oob_score=row[5],
            random_state=random_seed,
            n_jobs=-1
        )

    def get_mape(self, model, error_metric, x_train, x_test, y_train, y_test):
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)

        if error_metric == "accuracy_score":
            error = metrics.accuracy_score(y_test, predictions)
        elif error_metric == "f1_score":
            error = metrics.f1_score(y_test, predictions)
        elif error_metric == "roc_auc_score":
            error = metrics.roc_auc_score(y_test, predictions)

        return error

    def objective(self, error_metric, row, x_train, x_test, y_train, y_test, random_seed):
        '''
        Returns the inverse of the MAPE of the model described by a row.
        '''

        if 'score' in row and row['score'] == row['score']:  # row[error_metric] == row[error_metric]
            return row['score']  # checks that row[error_metric] is not NaN.

        return self.get_mape(self.get_model(row, random_seed=random_seed), error_metric,
                             x_train, x_test, y_train, y_test)