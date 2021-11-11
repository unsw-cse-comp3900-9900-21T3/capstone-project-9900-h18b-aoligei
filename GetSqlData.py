import pandas as pd
import pymysql


def read_data_from_sql():
    db = pymysql.connect(
        host='comp9323db.c4ewkd5opwpk.us-east-2.rds.amazonaws.com',
        port=3306,
        user='hello',
        password='93239323',
        db='develop',
    )
    cursor = db.cursor()
    cursor.execute('''select * from Product_product''')
    data = cursor.fetchall()
    columnsDes = cursor.description
    columnsNames = [columnsDes[i][0] for i in range(len(columnsDes))]
    df = pd.DataFrame([list(i) for i in data], columns=columnsNames)
    # data = pd.DataFrame(list(data))

    cursor.close()
    db.close()
    return df


def read_score_data_from_sql():
    db = pymysql.connect(
        host='comp9323db.c4ewkd5opwpk.us-east-2.rds.amazonaws.com',
        port=3306,
        user='hello',
        password='93239323',
        db='develop',
    )
    cursor = db.cursor()
    cursor.execute('''select AVG(score),product_id,COUNT(score)  from Product_score group by product_id''')
    data = cursor.fetchall()
    columnsDes = cursor.description
    columnsNames = [columnsDes[i][0] for i in range(len(columnsDes))]
    df = pd.DataFrame([list(i) for i in data], columns=columnsNames)
    # data = pd.DataFrame(list(data))

    cursor.close()
    db.close()
    return df

# data = read_data_from_sql()
# score_data = read_score_data_from_sql()
#
#
# data.to_csv('product.csv')
# score_data.to_csv('score.csv')
#
# print(data.head(5))
# print(score_data.head(20))
#
# data['id'] = data['id'].astype('int')
# score_data['id'] = score_data['product_id'].astype('int')
# print(score_data.head())
# # merge two dataframe
# data_and_score = data.merge(score_data, on='id')
#
# print(data_and_score.__len__())

