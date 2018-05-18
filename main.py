from flask import Flask, session, redirect, url_for, escape, request, render_template
import rank_contributors

app = Flask(__name__)
hotword = ''
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['query'] = request.form['query']
        return redirect(url_for('search'))
    else:
        return render_template('index.html')

@app.route('/s', methods=['GET', 'POST'])
def search():
    result = rank_contributors.run(session['query'])
    if result:
        users_list = ''
        for user in result:
            users_list += '<a href="https://hy.wikipedia.org/wiki/User:{}">{}</a>\t{}<br />'.format(user[0], user[0], user[1])
        top = '<a href="https://hy.wikipedia.org/wiki/Category:{}">{}</a> Կատեգորիայի էջերի խմբագիրների ցանկ՝ ըստ խմբագրումների ընդհանուր ծավալի (բայթերով)<br /><br />'.format(escape(session['query']), escape(session['query']))
        return render_template('results.html') + top + users_list + render_template('tail.html')
    return render_template('results.html') + 'Չհաջողվեց գտնել արդյունքներ (Գուցե մուտքագրել եք սխալ կատեգորիա՞)' + render_template('tail.html')

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
