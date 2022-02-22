from flask import Flask, render_template
app = Flask(__name__,static_url_path="/static")

@app.route('/')
def hello():
    return '<h1>Hello!</h1><p>I am Konjac. </p>' + \
    	   '<br /></br /><a href="/bio">Read my Bio</a>' + \
    	   '<br /></br /><a href="/socials">Connect with me through social media</a>'

@app.route('/bio')
def bio():
	return '<h1>This is my bio!</h1><p>This is Konjac and currently a junior' + \
		   ' CS major at UC Berkeley!</p><br /></br /><a href="/socials">Let’s connect?</a>'


@app.route('/socials')
def social():
	return '<a href="https://www.linkedin.com/in/konjac-huang/">LinkedIn</a>'