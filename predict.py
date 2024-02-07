def predict(best_ind, clf, data):
    # 新たなデータの取得
    # この部分は、新たなデータを取得する具体的な方法によります
    # ここでは、新たなデータをX_newとします
    X_new = data.drop(['arrival', 'popularity'], axis=1)
    # 新たなデータから最適な特徴量を選択
    X_new_selected = X_new.iloc[:, [i for i, val in enumerate(best_ind) if val]]

    # 新たなデータに対する予測を行う
    predictions = clf.predict(X_new_selected)

    
    print("-"*30, "予測結果", "-"*30)
    data['予想順位'] = predictions
    print(data)
