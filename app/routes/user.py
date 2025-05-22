from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from app.models import User
from app import db
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')

@user_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.email = request.form.get('email')
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_user.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/edit_profile.html')

@user_bp.route('/users')
@login_required
def index():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    users = User.query.all()
    return render_template('user/index.html', users=users)

@user_bp.route('/users/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('user.new'))
        
        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            is_admin=is_admin
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('User created successfully', 'success')
        return redirect(url_for('user.index'))
    
    return render_template('user/new.html')

@user_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.is_admin = request.form.get('is_admin') == 'on'
        
        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            user.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('user.index'))
    
    return render_template('user/edit.html', user=user)

@user_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(id)
    
    # Prevent deleting own account
    if user.id == current_user.id:
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('user.index'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('user.index')) 