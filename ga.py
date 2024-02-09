from math import sqrt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from deap import base, creator, tools, algorithms
from data import fix_model_data, fix_predict_model_data
from figure import log

# 遺伝的アルゴリズムの適応度関数
def evalFeature(individual):
    if not any(individual):  # 個体が全てFalseの場合
        return 0,
    mask = np.array(individual, dtype=bool)
    X_selected = X.iloc[:, mask]
    clf = DecisionTreeClassifier()
    scores = cross_val_score(clf, X_selected, Y, cv=5)
    return (scores.mean(),)

def evalFeatureWithOddsAndArrival(individual):
    # 個体が全てFalseの場合は、評価を行わない
    if not any(individual):
        return 0,
    # 選択された特徴量に基づいてデータセットをフィルタリング
    mask = np.array(individual, dtype=bool)
    X_selected = X.iloc[:, mask]

    # ここに、oddsとarrivalを用いた評価ロジックを実装
    # 例: oddsの平均値を計算し、arrivalの逆数（またはその他の変換）を使用して評価値を計算
    # この部分はプロジェクトの具体的な要件に応じて調整する必要があります
    # 以下は仮の計算例です
    average_odds = X_selected['odds'].mean()  # oddsの平均値
    inverse_arrival = sqrt(1 / X_selected['arrival'].mean())  # arrivalの平均値の逆数

    # 評価値を計算（ここでは、単純な和としていますが、適宜調整してください）
    score = average_odds + inverse_arrival

    return score,
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
    test_data,test_true = get_test_data()
    predictions = predict(best_ind, clf, test_data, test_true)
    print(test_true)
    from improve import improve
    accuracy = improve(toolbox, predictions, test_true)
    log(result)
    
    return result,accuracy

print("fetching data")
data = fix_model_data('中山', 1800, True)
print("data fetched")
# 特徴量とターゲットの分離
X = data.drop(['arrival', 'popularity', 'race_id'], axis=1)
Y = data['arrival']

for i in range(1):
    res = ga()
    if res[1] > 0.99:
        break

