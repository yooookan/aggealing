import numpy as np
from openjij import SQASampler
from pyqubo import Array, Constraint, Placeholder

def process():
    # プレゼント　リスト
    presents = [['pole_smith', 'dacoda', 'prada'], 
                ['mark_jcobs', 'armani', 'diesel'], 
                ['hermers', 'alisaashley', 'avantus'], 
                ['gucci', 'lion_hart', 'armani'], 
                ['armani', 'hermers', 'vivian_west_wood']]

    # 価格
    price = np.array([[25600, 14400, 65900], 
                    [35000, 22100, 14700], 
                    [35000, 3600, 37800],
                    [30500, 11400, 11900],
                    [14600, 24500, 9300]])

    # 人気ランキング
    rank = np.array([[1, 2, 3], 
                    [1, 2, 3], 
                    [1, 2, 3], 
                    [1, 2, 3],
                    [1, 2, 3]])

    categorys = 5
    ranks = 3

    # プレゼント日数, 2022年, 2023年の 08/24(誕生日) と 12/24（クリスマス）
    days = 4


    x = Array.create(name='x', shape=(days, categorys, ranks), vartype='BINARY')

    day_constr_list = []
    for i in range(days):
        day_constr_list.append((np.sum(x[i, :, :]) - 1)**2)
    constr_1 = np.sum(np.array(day_constr_list))

    catgory_constr_list = []
    for i in range(categorys):
        catgory_constr_list.append((np.sum(x[:, i, :]) - 1)**2)
    constr_2 = np.sum(np.array(catgory_constr_list))

    cost_1 = np.sum(np.multiply(x, price)) # 安いほどよい
    cost_2 = np.sum(np.multiply(x, rank)) # ランクが高いほどよい

    cost_func = cost_1 + Placeholder('rank') * cost_2 + Placeholder('lamb_a') * Constraint(constr_1, label='present') + Placeholder('lamb_b') * Constraint(constr_2, label='category')

    model = cost_func.compile()

    feed_dict = {'rank':100.0, 'lamb_a':50000.0, 'lamb_b':50000.0}
    qubo, offset = model.to_qubo(feed_dict=feed_dict)

    sampler = SQASampler()

    sampleset = sampler.sample_qubo(qubo,num_reads=20)

    decoded_samples = model.decode_sampleset(sampleset=sampleset, feed_dict=feed_dict)
    # for sample in decoded_samples:
    #   print(sample.constraints(only_broken=True))

    result = sampleset.record[0][0].reshape(days, categorys, ranks)

    idx = np.where(result==1)
    present_name = presents[idx[1][0]][idx[2][0]]
    
    return result, idx, present_name 
