import numpy as np
from openjij import SQASampler
from pyqubo import Array, Constraint, Placeholder

def process(selected_categorys, selected_date):
    # Todo: these lists should be selected from database
    category_names = ['財布', '時計', '香水', 'ネックレス', 'ネクタイ']
    img_paths = ['../static/wallet.png', '../static/watch.png', '../static/perfume.png',
                 '../static/necklace.png', '../static/necktie.png']

    presents_list = [['ポール・スミス', 'ダコダ', 'プラダ'], 
                     ['マーク・ジェイコブズ', 'アルマーニ', 'ディーゼル'], 
                     ['エルメス', 'アリサアシュレイ', 'アバントゥス'], 
                     ['グッチ', 'ライオンハート', 'アルマーニ'], 
                     ['アルマーニ', 'エルメス', 'ヴィヴィアンウェストウッド']]

    price_list = np.array([[25600, 14400, 65900], 
                           [35000, 22100, 14700], 
                           [35000, 3600, 37800],
                           [30500, 11400, 11900],
                           [14600, 24500, 9300]])

    categorys = len(selected_categorys)
    ranks = 3
    days = len(selected_date)

    rank = np.array([list(range(ranks))] * categorys) + 1
    presents = [presents_list[int(i)-1] for i in selected_categorys]
    price = [price_list[int(i)-1] for i in selected_categorys]

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

    result = sampleset.record[0][0].reshape(days, categorys, ranks)

    idx = np.where(result==1)
    result_len = len(idx[0])
    present_name_1 = presents[idx[1][0]][idx[2][0]]
    present_name_2 = presents[idx[1][1]][idx[2][1]]
    present_names = [present_name_1, present_name_2]

    category_1 = int(selected_categorys[idx[1][0]]) - 1 
    category_2 = int(selected_categorys[idx[2][0]]) - 1
    category_names = [category_names[category_1], category_names[category_2]]

    imgs = [img_paths[category_1], img_paths[category_2]]
    
    return result, idx, present_names, category_names, imgs
