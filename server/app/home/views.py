#coding=utf-8

from flask import render_template
from flask import request

from . import home

from db.university import University

uni = University()

@home.route('/home', methods=['GET'])
def homepage():
    """
    Render the homepage template on the / route
    """
    print 'hello you!'
    return render_template('home/home.html')


@home.route('/home', methods=['POST'])
def show_university():
    """
    Render the dashboard template on the /dashboard route
    """
    enti = {k: request.values[k].encode('utf-8') for k in request.values}
    for k in ['major','batch','score']:
        if k not in enti:
            print '{} 参数值为空'.format(k)

    universities_info = uni.university_can_apply(enti['score'], enti['batch'], enti['major'])
    return render_template('home/applicable_university.html', universities_info=universities_info)
