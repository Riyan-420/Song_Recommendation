from flask import Blueprint, render_template
from flask_login import login_required
from admin_utils import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 🎛️ Control Room — Admin Dashboard
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

# 🎶 Drop the Beat — Add new songs
@admin_bp.route('/add-song')
@login_required
@admin_required
def add_song():
    return render_template('admin/add_song.html')

# 🎯 Sound Tracker — Manage (update/delete) existing songs
@admin_bp.route('/manage-songs')
@login_required
@admin_required
def manage_songs():
    return render_template('admin/manage_songs.html')

# 👥 Spy on Fans — View/Delete Users
@admin_bp.route('/manage-users')
@login_required
@admin_required
def manage_users():
    return render_template('admin/manage_users.html')

# 📰 What’s New? — Launch new song notifications
@admin_bp.route('/notifications')
@login_required
@admin_required
def notifications():
    return render_template('admin/notifications.html')

# 🗑️ Graveyard — Recycle bin (restore deleted users or songs)
@admin_bp.route('/graveyard')
@login_required
@admin_required
def graveyard():
    return render_template('admin/graveyard.html')
