from math import sqrt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from deap import base, creator, tools, algorithms
from data import fix_model_data, fix_predict_model_data
from figure import log

from sklearn.metrics import accuracy_score, make_scorer

def custom_score(y_true, y_pred):
    score = accuracy_score(y_true, y_pred)
    top3_true = set(np.argsort(y_true)[-3:])
    top3_pred = set(np.argsort(y_pred)[-3:])
    if top3_true == top3_pred:
        score *= 1.3 
    return score

# 遺伝的アルゴリズムの適応度関数
def evalFeature(individual):
    if not any(individual): 
        return 0,
    mask = np.array(individual, dtype=bool)
    X_selected = X.iloc[:, mask]
    clf = DecisionTreeClassifier()
    custom_scorer = make_scorer(custom_score)
    scores = cross_val_score(clf, X_selected, Y, cv=5, scoring=custom_scorer)
    return (scores.mean(),)

def ga():
    
    # 遺伝的アルゴリズムの個体を定義
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", np.random.randint, 0, 2)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=X.shape[1])
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalFeature)
    toolbox.register("mate", tools.cxTwoPoint) # 二点交叉
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=200)
    ngen = 100
    
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("min", min)
    stats.register("max", max)
    stats.register("avg", lambda ind: sum(ind) / len(ind))
    
    result = algorithms.eaSimple(population, toolbox, cxpb=0.6, mutpb=0.2, ngen=ngen, stats=stats, verbose=True)
    log(result)

    # 最適な特徴量セットの取得
    best_ind = tools.selBest(population, 1)[0]
    best_features = [f"{X.columns.values[i]}" for i, val in enumerate(best_ind) if val]
    print(best_features)
    X_selected = X.iloc[:, [i for i, val in enumerate(best_ind) if val]]
    clf = RandomForestClassifier()  # ランダムフォレストは特徴量の重要度を提供する
    clf.fit(X_selected, Y)

    # 特徴量の重要度に基づいてソート
    feature_importances = clf.feature_importances_
    features_sorted = sorted(zip(X_selected.columns, feature_importances), key=lambda x: x[1], reverse=True)

    # ソートされた特徴量とその重要度を表示
    print("Features sorted by importance:")
    for feature, importance in features_sorted:
        print(f"{feature}: {importance}")


    from predict import predict
    from testdata import get_test_data
    from improve import improve
    
    test_data_id = ["202206010608", "202206050210", "202206050807"]
    predictions = [None,None,None]
    test_data = [None,None,None]
    test_true = [None,None,None]
    
    for i in range(3):
        test_data[i],test_true[i] = get_test_data(test_data_id[i])
        predictions[i] = predict(best_ind, clf, test_data[i], test_true[i])
        
        accuracy = improve(toolbox, predictions[i], test_true[i])
        
    return result,accuracy

print("fetching data")
data = fix_model_data('中山', 1800, True)
print("data fetched")
# 特徴量とターゲットの分離
X = data.drop(['arrival', 'popularity', 'race_id'], axis=1)
Y = data['arrival']

ga()
