
from flask import Blueprint, render_template, request, url_for,flash, g
from app import db
from sqlalchemy import text
from flask_login import login_required, current_user
from models import Products

main = Blueprint('main', __name__)



cart_prods =[]

@main.route('/',methods=['GET', 'POST'])
def products():
    from utilities import fetchProducts, almostProducts

    page = request.args.get('page',1,type=int)

    keyword = request.args.get('keyword',"*",type = str)
        
        
        
    if request.method== 'POST':

        if request.form.get('keyword'):
            keyword = request.form['keyword']
        # print("Inside post")
        # print(cart_prods)
        if request.form.get("id"):
            # print("I am here")
            prod_id = request.form.get("id")
            action = "add" if request.form.get("action")=="Add to cart" else "remove"
            if action=="add":
                cart_prods.append(prod_id)
            else:
                cart_prods.remove(prod_id)

    
    if keyword == "*":
        pagination = Products.query.paginate(page = page, per_page = 12)


    else:
        pagination = Products.query.filter(Products.name.contains(keyword)).paginate(page = page, per_page = 12)

    data = [u.__dict__ for u in pagination.items]


    recom_data = almostProducts(db)

    

    return render_template("products.html", keyword = keyword,pagination = pagination, data = data, recom_data = recom_data, cart_prods =cart_prods, products = True)




@main.route('/mywishlist', methods =["POST", "GET"])
@login_required
def mywishlist_update():

    user_id=current_user.userId
    from utilities import fetchWishlist, randomProducts, prodsById, fetchTopProducts
    if cart_prods:
        Prods = prodsById(cart_prods, db)
    else:
        Prods = []
    # else:
    #     Prods = fetchTopProducts(user_id, db)
    current_wishlist = fetchWishlist(user_id,db)
    #last_wishId = db.engine.execute(text("SELECT WishId FROM Wishes ORDER BY WishId DESC LIMIT 1")).first()[0]
    
    if request.method == "POST":
       # getting input with name = fname in HTML form
       size = int(request.form.get("size")) 
       upd_wishlist = []
       for i in range(size):
        upd_wishlist.append({"product_id": request.form.get(f"item_id_{i+1}"), "portion":request.form.get(f"quantity_{i+1}")})
        # print(upd_wishlist)
       
       for itemset in upd_wishlist:
        queryFind = f"SELECT wishId, userId, productId, portion FROM Wishes WHERE userId={user_id} and productId={itemset['product_id']} and status=0"
        prev_wish = db.engine.execute(text(queryFind)).first()
        if prev_wish and int(prev_wish._asdict()['portion']) == int(itemset['portion']):
            continue

        if prev_wish and int(prev_wish._asdict()['portion']) != int(itemset['portion']):
            queryDel = f"DELETE FROM Wishes WHERE wishId={prev_wish['wishId']} and status=0"

            db.engine.execute(text(queryDel))
        
        
        queryInfoFromId = f"SELECT productId, quantity FROM Products WHERE productId={itemset['product_id']}"
        prodQuantity = int(db.engine.execute(text(queryInfoFromId)).first()._asdict()['quantity'])
        for i in range(int(itemset['portion'])//prodQuantity):
            queryAdd = f"CALL createOrder({itemset['product_id']}, {user_id}, {prodQuantity})"
            # print(queryAdd)
            db.engine.execute(text(queryAdd))
        if int(itemset['portion'])%prodQuantity!=0:
            queryAdd = f"CALL createOrder({itemset['product_id']}, {user_id}, {int(itemset['portion'])%prodQuantity})"
            # print(queryAdd)
            db.engine.execute(text(queryAdd))
        
       for wish in current_wishlist:
        exists = 0
        for itemset in upd_wishlist:
            if int(itemset['product_id'])==wish['productId']:
                exists=1
        if exists==0:
            queryDel = f"DELETE FROM Wishes WHERE userId={user_id} and productId={wish['productId']} and status=0"
            # print(queryDel)
            db.engine.execute(text(queryDel))
       current_wishlist = fetchWishlist(user_id,db)
        
            
    return render_template("mywishlist.html", wishlist=True, rndProds=Prods, current_wishlist=current_wishlist, size=len(current_wishlist))

@main.route('/myorders')
@login_required
def myorders():

    from utilities import getOrders

    current_orders = getOrders(current_user.userId, db)


    return render_template("myorders.html", orders=True, current_orders = current_orders)


@main.route('/myPage')
@login_required
def mypage():
    
    from utilities import fetchTopProducts

    topProducts = fetchTopProducts(current_user.userId, db)

    return render_template("mypage.html", page=True, topProducts = topProducts)


