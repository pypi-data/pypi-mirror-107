# Library imports
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from lightgbm import LGBMRegressor

pd.options.mode.chained_assignment = None

random_seed = 2021
np.random.seed(random_seed)


def optimize_lgbmr(x_train, x_test, y_train, y_test, params={}, error_metric="MAPE", population_size=50,
                  number_of_generation=10, mutation_rate=0.05, random_seed=2021):
    try:
        parameters = []

        if "n_estimators" in params.keys():
            parameters.append(params["n_estimators"])
        else:
            parameters.append(np.arange(2, 1000))

        if "max_depth" in params.keys():
            parameters.append(params["max_depth"])
        else:
            parameters.append(np.arange(2, 20))

        if "learning_rate" in params.keys():
            parameters.append(params["learning_rate"])
        else:
            parameters.append([0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

        if "boosting_type" in params.keys():
            parameters.append(params["boosting_type"])
        else:
            parameters.append(["gbdt"])

        if "num_leaves" in params.keys():
            parameters.append(params["num_leaves"])
        else:
            parameters.append(np.arange(2, 15))

        if "reg_alpha" in params.keys():
            parameters.append(params["reg_alpha"])
        else:
            parameters.append([0])

        if "reg_lambda" in params.keys():
            parameters.append(params["reg_lambda"])
        else:
            parameters.append([0])
        obj = Optimizer()
        model, row = obj.best_estimator(x_train, x_test, y_train, y_test, parameters, error_metric,
                                        population_size, number_of_generation, mutation_rate, random_seed)
        return model, row
    except Exception as e:
        print(e)

class Optimizer:

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
        objective_function = lambda i: self.objective(error_metric, i, x_train, x_test, y_train, y_test, random_seed=random_seed)
        # ------------------------------------------------------------------------------------------------------------

        population = pd.DataFrame()
        np.random.seed(random_seed)
        population['n_estimators'] = np.random.choice(rf_parameters[0], size=population_size)
        population['max_depth'] = np.random.choice(rf_parameters[1], size=population_size)
        population['learning_rate'] = np.random.choice(rf_parameters[2], size=population_size)
        population['boosting_type'] = np.random.choice(rf_parameters[3], size=population_size)
        population['num_leaves'] = np.random.choice(rf_parameters[4], size=population_size)
        population['reg_alpha'] = np.random.choice(rf_parameters[5], size=population_size)
        population['reg_lambda'] = np.random.choice(rf_parameters[6], size=population_size)
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
            output_params[error_metric] = round(1 / output_params['score'], 2)
            output_params.drop('score', inplace=True)

        return [self.get_model(population.loc[population[error_metric].idxmax()]), output_params]


    def match(self, population, random_seed):
        '''
        Samples from population with higher scores having higher probability of selection.
        '''

        np.random.seed(random_seed)
        length = population.shape[0]
        population['score'].fillna(0, inplace=True)
        prob = population['score'] / population['score'].sum()

        indices = np.random.choice(np.arange(length), p=prob, size=length)
        return population.iloc[indices]


    def crossover(self, population, random_seed):
        '''
        Performs a random crossover with the entire population as an input.
        '''

        np.random.seed(random_seed)
        length, width = population.shape
        width -= 1

        # i is an array which maps indices randomly either to themselves or their pair.
        a = np.random.choice((0, 1), size=length * width)
        a[np.arange(1, length * width, 2)] *= -1
        i = np.arange(length * width) + a

        # Convert the population to a list of genes, and map each gene to itself or its pair using i.
        gene_list = np.array(population.drop('score', axis=1)).reshape(-1, order='F')
        return pd.DataFrame(gene_list[i].reshape((-1, width), order='F'), columns=population.columns[:-1])


    def mutate(self, population, mutation_rate, rf_parameters, random_seed):
        '''
        Mutate the population with a given mutation rate.
        '''
        try:
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
        except Exception as e:
            print(e)


    def get_model(self, row, random_seed=2021):
        '''
        Return the model specified by the given row.
        '''
        return LGBMRegressor(
            n_estimators=(row[0]),
            max_depth=row[1],
            learning_rate=row[2],
            boosting_type=row[3],
            num_leaves=row[4],
            reg_alpha=row[5],
            reg_lambda=row[6],
            num_iterations=100,
            random_state=random_seed,
            n_jobs=-1
        )


    def get_mape(self, model, error_metric, x_train, x_test, y_train, y_test):
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        list_prediction = list(predictions)
        list_actual = list(y_test.values)

        if error_metric == "MAPE":
            '''
            Calculates the MAPE of a model on given data.
            '''
            error = 0
            for i in range(len(list_prediction)):
                if ((list_prediction[i] == 0) & (list_actual[i] == 0)):
                    error += 0
                elif ((list_prediction[i] != 0) & (list_actual[i] == 0)):
                    error += 100
                else:
                    error += ((abs(list_prediction[i] - list_actual[i])) / list_actual[i]) * 100

            mp = error / len(list_prediction)
        elif error_metric == "RMSE":
            mp = mean_squared_error(list_actual, list_prediction)

        return mp


    def objective(self, error_metric, row, x_train, x_test, y_train, y_test, random_seed):
        '''
        Returns the inverse of the MAPE of the model described by a row.
        '''

        if 'score' in row and row['score'] == row['score']:
            return row['score']

        return 1 / (self.get_mape(self.get_model(row, random_seed=random_seed), error_metric, x_train, x_test, y_train, y_test))




