import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from deap import base, creator, tools, algorithms
from data import main

# 遺伝的アルゴリズムの適応度関数
def evalFeature(individual):
    if not any(individual):  # 個体が全てFalseの場合
        return 0,
    mask = np.array(individual, dtype=bool)
    X_selected = X.iloc[:, mask]
    clf = DecisionTreeClassifier()
    scores = cross_val_score(clf, X_selected, y, cv=5)
    return (scores.mean(),)

data = main()
# 特徴量とターゲットの分離
X = data.drop('arrival', axis=1)
y = data['arrival']
# 遺伝的アルゴリズムの個体を定義
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.randint, 0, 2)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=X.shape[1])
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalFeature)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=50)
ngen = 100
result = algorithms.eaSimple(population, toolbox, cxpb=0.6, mutpb=0.2, ngen=ngen, verbose=True, stats=tools.Statistics(lambda ind: ind.fitness.values))

# 最適な特徴量セットの取得
best_ind = tools.selBest(population, 1)[0]
best_features = [i for i, val in enumerate(best_ind) if val]
print(best_features)

