from flask import Flask,render_template,request
import pickle
import numpy as np

app = Flask(__name__)

popular = pickle.load(open("model/popular.pkl","rb"))
pt = pickle.load(open("model/pt.pkl","rb"))
similarity = pickle.load(open("model/similarity.pkl","rb"))
books = pickle.load(open("model/books.pkl","rb"))

@app.route('/')
def index():
    return render_template("index.html",
                           book_name = list(popular['Book-Title'].values),
                           book_author = list(popular['Book-Author'].values),
                           num_rating = list(popular['num_rating'].values),
                           avg_rating = list(popular['avg_rating'].values),
                           image = list(popular['Image-URL-M'].values),
                           image1 = list(popular['Image-URL-L'].values),
                           image2 = list(popular['Image-URL-S'].values)
                           )

@app.route('/recommend')
def recommend():
    return render_template("recommendation.html")

@app.route('/function', methods=['POST'])
def function():
    user_input = str(request.form.get('user_input'))
    print("User Input:", user_input)  # Debugging statement

    # Check if the book exists in the dataset
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
        data = []
        for i in similar_items:
            item = []
            temp = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)
        print("Data to Render:", data)  # Debugging statement
    else:
        print("Book not found in dataset.")  # Handle case where book isn't found
        data = 0
    
    return render_template("recommendation.html", data=data)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/book/<book_title>')
def book_detail(book_title):
    input = str(book_title)

    # //books
    item = []
    da = []
    temp = popular[popular['Book-Title'] == input]
    item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
    item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
    item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
    item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-L'].values))
    item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-S'].values))
    item.extend(list(temp.drop_duplicates('Book-Title')['avg_rating'].values))
    item.extend(list(temp.drop_duplicates('Book-Title')['num_rating'].values))
    da.append(item)
    
    #//recommend
    index = np.where(pt.index == input)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template("shop.html",book=da,data=data)

@app.route("/payment")
def payment():
    return render_template("payment.html")

@app.route("/success")
def success():
    return render_template("successful.html")

if __name__ == "__main__":
    app.run(debug=True)