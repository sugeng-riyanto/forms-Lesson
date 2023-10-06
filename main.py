from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'



@app.route('/')
def index():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM submissions')
    submissions = cursor.fetchall()
     # Calculate sum and average for each column
    data=submissions
    column1_sum = sum(row[3] for row in data)
    column2_sum = sum(row[4] for row in data)
    column1_avg = column1_sum / len(data)
    column2_avg = column2_sum / len(data)
    row_sums = [sum(row[3:]) for row in data]
    name_isian=  (row[1] for row in data)

    conn.close()
    return render_template('index.html', name_isian=name_isian, submissions=submissions, column1_sum=column1_sum, column2_sum=column2_sum, column1_avg=column1_avg, column2_avg=column2_avg, row_sums=row_sums)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        fullname = request.form['fullname']
        suggest = request.form['suggest']
        rating = request.form['rating']
        coming = request.form['coming']
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO submissions (fullname, suggest, rating,coming) VALUES (?, ?, ?, ?)',
                       (fullname, suggest, rating,coming))
        conn.commit()
        conn.close()
        flash('Code submitted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=["GET"])
def delete(id):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()#
    cur.execute("DELETE FROM submissions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("data was delete successfully")
    return redirect( url_for('index'))


@app.route('/update')
def update():
    return render_template('update.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    if request.method == 'POST':
        fullname = request.form['fullname']
        suggest = request.form['suggest']
        rating = request.form['rating']
        coming = request.form['coming']
        cursor.execute('UPDATE submissions SET fullname=?, suggest=?, rating=?, coming=? WHERE id=?', (fullname, suggest, rating, coming, id))
        conn.commit()
        flash('Data was updated successfully', 'success')
        return redirect(url_for('index'))
    else:
        cursor.execute('SELECT * FROM submissions WHERE id=?', (id,))
        submissions = cursor.fetchone()
        conn.close()
        return render_template('update.html', i=submissions)



if __name__ == '__main__':
    app.run(debug=True)