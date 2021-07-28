import os
import numpy as np


def get_item_info(input_file):
    """
    :param input_file: item info file
    :return: a dict:key itemid,value:[title,genre]
    """

    if not os.path.exists(input_file):
        return {}
    item_info = {}  # 用来存放处理后的文本信息，是一个dict字典类型
    linenum = 0
    fp = open(input_file, 'r', encoding='ISO-8859-1')
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split('::')
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemid, title, genre = item[0], item[1], item[2]
        elif len(item) > 3:
            itemid = item[0]
            genre = item[-1]
            title = ",".join(item[1:-1])
        item_info[itemid] = [title, genre]
    fp.close()
    return item_info


def get_ave_score(input_file):
    """
    get item ave rating score
    :param input_file: user rating file
    :return: a dict,key:itemid,value:ave_score
    """
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}
    score_dict = {}
    fp = open(input_file, 'r', encoding='ISO-8859-1')
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split('::')
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if itemid not in record_dict:
            record_dict[itemid] = [0, 0]
        record_dict[itemid][0] += 1
        record_dict[itemid][1] += rating

    fp.close()
    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1] / record_dict[itemid][0], 3)
    return score_dict


def get_train_data(input_file):
    """
    get train data for LFM model train
    :param input_file: user item rating file
    :return: a list:[(userid,itemid,label),(userid1,itemid1,label)]
    """
    if not os.path.exists(input_file):
        return []
    score_dict = get_ave_score(input_file)
    neg_dict = {}
    pos_dict = {}
    train_data = []
    linenum = 0
    score_thr = 4.0  # 定义以4.0为分界线，pos和neg
    fp = open(input_file, 'r', encoding='ISO-8859-1')
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split('::')
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0], item[1], float(item[2])
        if userid not in pos_dict:
            pos_dict[userid] = []
        if userid not in neg_dict:
            neg_dict[userid] = []
        if rating >= score_thr:
            pos_dict[userid].append((itemid, 1))
        else:
            score = score_dict.get(itemid, 0)
            neg_dict[userid].append((itemid, score))
    fp.close()
    for userid in pos_dict:
        data_num = min(len(pos_dict[userid]), len(neg_dict.get(userid, [])))
        if data_num > 0:
            train_data += [(userid, zuhe[0], zuhe[1]) for zuhe in pos_dict[userid]][:data_num]
        else:
            continue
        sorted_neg_list = sorted(neg_dict[userid], key=lambda element: element[1], reverse=True)[:data_num]
        train_data += [(userid, zuhe[0], 0) for zuhe in sorted_neg_list]

    return train_data


def init_model(vector_len):
    """
    :param vector_len: the len of vector
    :return: a ndarray
    """
    return np.random.randn(vector_len)


def model_predict(user_vector, item_vector):
    """
    distance between user_vector and item_vector
    :param user_vector: model produce user vector
    :param item_vector: model produce item vector
    :return: a num
    """
    res = np.dot(user_vector, item_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(item_vector))
    return res


def lfm_train(train_data, F, alpha, beta, step):
    """

    :param train_data: train_data for lfm
    :param F: user vector len,item vector len
    :param alpha: regularization factor
    :param beta: learning rate
    :param step: iteration num
    :return: dict: key itemid,value :list
            dict :key userid,value：list
    """
    user_vec = {}
    item_vec = {}
    for step_index in range(step):
        print(step_index,'/',step)
        for data_instance in train_data:
            userid,itemid,label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F) #初始化，F个参数，标准正态分布
            if itemid not in item_vec:
                item_vec[itemid] = init_model(F) #初始化
            #模型迭代部分
            delta = label - model_predict(user_vec[userid],item_vec[itemid]) #预测与实际的差
            for index in range(F):#index就是f
                #出于工程角度的考虑，这里没有照搬公式的2倍，而是1倍，效果是一样的
                user_vec[userid][index] += beta*(delta*item_vec[itemid][index] - alpha*user_vec[userid][index])
                item_vec[itemid][index] += beta*(delta*user_vec[userid][index] - alpha*item_vec[itemid][index])

            beta = beta * 0.9 #参数衰减，目的是：在每一轮迭代的时候，接近收敛时，能慢一点
    return  user_vec,item_vec


def give_recom_result(user_vec, item_vec, userid):
    """
    use lfm model result give fix userid recom result
    :param user_vec: model result
    :param item_vec: model result
    :param userid:fix userid
    :return:a list:[(itemid,score)(itemid1,score1)]
    """
    fix_num = 10  # 排序，推荐前fix_num个结果
    if userid not in user_vec:
        return []
    record = {}
    recom_list = []
    user_vector = user_vec[userid]
    for itemid in item_vec:
        item_vector = item_vec[itemid]
        res = np.dot(user_vector, item_vector) / (np.linalg.norm((user_vector) * np.linalg.norm(item_vector)))  # 余弦距离
        record[itemid] = res
        record_list = list(record.items())
        # 排序
    for zuhe in sorted(record.items(), key=lambda rec: record_list[1], reverse=True)[:fix_num]:
        itemid = zuhe[0]
        score = round(zuhe[1], 3)
        recom_list.append((itemid, score))
    return recom_list


def ana_recom_result(train_data, userid, recom_list):
    """
    debug recom result for userid
    :param train_data: train data for userid
    :param userid: fix userid
    :param recom_list: recom result by lfm
    :return: no return
    """
    item_info = get_item_info("./ml-1m/movies.dat")
    # print("该用户曾给过好评的电影如下：")
    # for data_instance in train_data:
    #     tmp_userid, itemid, label = data_instance
    #     if tmp_userid == userid and label == 1:
    #         print(item_info[itemid])
    print("前n个推荐电影为：")
    cnt = 1
    for zuhe in recom_list:
        print(cnt, item_info[zuhe[0]])
        cnt += 1


def model_train_process(userid):
    """
    test lfm model train
    :return:
    """
    train_data = get_train_data("./ml-1m/ratings.dat")
    user_vec, item_vec = lfm_train(train_data, 50, 0.01, 0.1, 50)
    recom_list = give_recom_result(user_vec, item_vec, userid)
    print(recom_list)
    ana_recom_result(train_data, userid, recom_list)

    return user_vec, item_vec


# train_data = get_train_data("./ml-1m/ratings.dat")
# print(train_data)
# print(len(train_data))

model_train_process('8')
