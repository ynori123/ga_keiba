import matplotlib.pyplot as plt
import datetime
import random

def log(result):
    # resultから統計情報のログを取得
    log = result[1]

    # 各世代の最大適応度、最小適応度、平均適応度を取得
    max_fitness_values = log.select("max")
    min_fitness_values = log.select("min")
    avg_fitness_values = log.select("avg")

    # 世代数を取得
    generations = range(len(max_fitness_values))

    # 最大適応度、最小適応度、平均適応度をプロット
    plt.plot(generations, max_fitness_values, label="Max Fitness")
    plt.plot(generations, min_fitness_values, label="Min Fitness")
    plt.plot(generations, avg_fitness_values, label="Avg Fitness")

    # グラフのタイトルとラベルを設定
    plt.title("Fitness through the Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    
    plt.legend()
    
    plt.savefig(f"./graphs/{str(datetime.datetime.now())}.png", dpi=300)
    # plt.show()
