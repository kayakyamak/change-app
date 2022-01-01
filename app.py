from flask import Flask, request
from flask import jsonify
app = Flask(__name__)

def change(amount):
    # calculate the resultant change and store the result to res
    res = []
    coins = [1, 5, 10, 25]  # values of pennies, nickels, dimes, and quarteres
    coin_lookup = {25: "quarters", 10: "dimes", 5: "nickels", 1: "pennies"}
    
    # divide the amount*100 (the amount in cents) by a coin value
    # record the number of coins that evenly divide and the remainder
    coin = coins.pop()
    num, rem = divmod(int(amount*100), coin)
    # append the coin type and number of coins that had no remainder
    res.append({num:coin_lookup[coin]})
    
    # while there is still some remainder, continue adding coins to the result
    while rem > 0:
        coin = coins.pop()
        num, rem = divmod(rem, coin)
        if num:
                if coin in coin_lookup:
                    res.append({num:coin_lookup[coin]})
                    
    return res
    
@app.route('/')
def helo():
    """Return a firendly HTTP greeting"""
    print("I am inside hello world")
    return 'Hello World! I can make change at route: /change'
    
@app.route('/change/<dollar>/<cents>')
def changeroute(dollar, cents):
    print(f"Make change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    result = change(float(amount))
    return jsonify(result)

@app.route('/multiple/<dollar>/<cents>')
def mutiplyamount(dollar, cents):
    amount = f"{dollar}.{cents}"
    print(f"This is the ${amount} X 100")
    return jsonify(int(dollar)*100+int(cents))
    
@app.route('/post', methods=['POST'])
def post():
    if request.method == "POST":
        data = request.json
        amount = data["amount"]
        result = change(float(amount))
        return jsonify(result*100)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)