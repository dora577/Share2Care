from sqlalchemy import text

def fetchProducts(keyword, db):
    if keyword == "*":
        query = "SELECT * from Products LIMIT 12"
    else:
        query = f"SELECT * from Products WHERE name like '%{keyword}%'  limit 12"

    result = db.engine.execute(text(query))

    data =  [u._asdict() for u in result.all()]


    return data


def fetchWishlist(user_id, db):

    query = f"""SELECT wishId, productId, name, price, imageURL, quantity, portion 
                FROM (SELECT * FROM Wishes 
                WHERE userId = {user_id} AND status = 0) as W 
                NATURAL JOIN Products"""
    result = db.engine.execute(text(query))

    wishlist = [u._asdict() for u in result.all()]
    
    return wishlist

def almostProducts(db):

    recom_query = f"""SELECT *, quantity - (MOD(total_portion,quantity))  as rest 
                    FROM (SELECT productId, sum(portion) as total_portion 
                            FROM Wishes WHERE status = 0 GROUP BY productId) as W 
                    NATURAL JOIN Products
                    WHERE quantity > 1 and total_portion mod quantity >=  quantity * 0.80 LIMIT 4"""
    result_recommendation = db.engine.execute(text(recom_query))


    recom_data = [u._asdict() for u in result_recommendation.all()]

    return recom_data

def fetchTopProducts(user_id, db):

    query = f"""SELECT *
                FROM Products NATURAL JOIN  (SELECT productId, count(productId) as times_ordered
							                FROM (SELECT userId FROM users u WHERE userId = {user_id}) as u
							                        NATURAL JOIN Wishes w
                                                    GROUP BY productId
                                                    ORDER BY times_ordered DESC
                                                    limit 8) AS P"""


    result = db.engine.execute(text(query))

    # topProducts = {}

    # for u in result.all():
    #     temp = u._asdict()
    #     topProducts 

    topProducts = [u._asdict() for u in result.all()]

    
    return topProducts

def randomProducts(db):
    query = f"SELECT * FROM Products ORDER BY RAND() LIMIT 4;"
    result = db.engine.execute(text(query))
    rndProds = [u._asdict() for u in result.all()]
    return rndProds

def prodsById(prods, db):

    sqllist = ','.join(prods)
    query = f"SELECT * FROM Products WHERE productId IN ({sqllist});"
    print(query)
    result = db.engine.execute(text(query))
    rndProds = [u._asdict() for u in result.all()]
    return rndProds



def getOrders(user_id, db):

    query = f"""SELECT productId, name, portion, orderId, imageURL, substr(convert_tz(orderDate, '+00:00','-06:00'),1,16) as orderDate
                FROM Wishes NATURAL JOIN Products NATURAL JOIN Orders
                WHERE userId = {user_id} AND status = 1 AND fullfiled = 0;"""

    result = db.engine.execute(text(query))

    orders = [u._asdict() for u in result.all()]

    return orders

    