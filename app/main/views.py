from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import get_movies,get_movie,search_movie
from .forms import ReviewForm
# from ..models import Review
from ..models import Reviews, User
from flask_login import login_required
from .. import db,photos
from flask_login import login_required, current_user

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Welcome to watchlist","email/welcome_user",user.email,user=user)

        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)

# Views
# @app.route('/')
# def index():

#     '''
#     View root page function that returns the index page and its data
#     '''

#     message = 'Hello World'
#     return render_template('index.html',message = message)
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to The perfect pictch'
    # Getting popular movie
    popular_pitches = get_pitches('popular')
    upcoming_pitch = get_pitches('upcoming')
    now_showing_pitch = get_pitches('now_playing')

    return render_template('index.html', title = title, popular = popular_pitch, upcoming = upcoming_pitch, now_showing = now_showing_pitch )

    # search_movie = request.args.get('movie_query')

    # if search_movie:
    #     return redirect(url_for('search',movie_name=search_movie))
    # else:
        
@main.route('/pitch/<int:id>')
def pitch(pitch_id):

    '''
    View piches page function that returns the piches details page and its data
    '''
    return render_template('piches.html',id = pitch_id)
@main.route('/pitch/<int:id>')
def pitch(id):

    '''
    View pitch page function that returns the pitch details page and its data
    '''
    piches = get_piches(id)
    title = f'{piches.title}'
    reviews = Reviews.get_reviews(piches.id)

    return render_template('pitch.html',title = title,pitch = pitch,reviews = reviews)
@main.route('/search/<pitch_name>')
def search(pitch_name):
    '''
    View function to display the search results
    '''
    pitch_name_list = pitch_name.split(" ")
    pitch_name_format = "+".join(pitch_name_list)
    searched_pitches = search_movie(pitch_name_format)
    title = f'search results for {pitch_name}'
    return render_template('search.html',pitches = searched_pitches)
@main.route('/pitches/review/new/<int:id>', methods = ['GET','POST'])
def new_review(id):
    form = ReviewForm()
    pitch = get_pitch(id)

    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(pitch.id,title,pitch.poster,review)
        new_review.save_review()
        return redirect(url_for('main.pitch',id = pitch.id ))

    title = f'{pitch.title} review'
    return render_template('new_review.html',title = title, review_form=form, pitch=pitch)

    @main.route('/user/<uname>/update/pic',methods= ['POST'])
    @login_required
 def update_pic(uname):
      user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
    # @main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
# @login_required
# def new_review(id):
#     form = ReviewForm()
#     movie = get_movie(id)
#     if form.validate_on_submit():
#         title = form.title.data
#         review = form.review.data

        # Updated review instance
        new_review = Review(pitch_id=pitch.id,pitch_title=title,image_path=pitch.poster,pitch_review=review,user=current_user)

        # save review method
        new_review.save_review()
        return redirect(url_for('.pitch',id = pitch.id ))

    title = f'{pitch.title} review'
    return render_template('new_review.html',title = title, review_form=form, pitch=pitch)

    