from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from admin_utils import admin_required
from models.song import Song
from extensions import db
from forms.song_form import SongForm
from models.user import User
from forms.user_form import UserForm
from models.notification import Notification
from forms.notification_form import NotificationForm
import firebase_admin
from firebase_admin import credentials, firestore
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 🎛️ Control Room — Admin Dashboard
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

# 🎶 Drop the Beat — Add new songs
@admin_bp.route('/add-song', methods=['GET', 'POST'])
@login_required
@admin_required
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        song = Song(
            title=form.title.data,
            artist=form.artist.data,
            album=form.album.data,
            genre=form.genre.data,
            year=form.year.data,
            extraversion=form.extraversion.data,
            openness=form.openness.data,
            conscientiousness=form.conscientiousness.data,
            agreeableness=form.agreeableness.data,
            neuroticism=form.neuroticism.data,
            energy=form.energy.data,
            mood=form.mood.data,
            lyrics_importance=form.lyrics_importance.data,
            album_art_url=form.album_art_url.data
        )
        db.session.add(song)
        db.session.commit()
        flash('Song added successfully!', 'success')
        return redirect(url_for('admin.manage_songs'))
    return render_template('admin/add_song.html', form=form)

# 🎯 Sound Tracker — Manage (update/delete) existing songs
@admin_bp.route('/manage-songs')
@login_required
@admin_required
def manage_songs():
    songs = Song.query.filter_by(deleted=False).all()
    return render_template('admin/manage_songs.html', songs=songs)

# 👥 Spy on Fans — View/Delete Users
@admin_bp.route('/manage-users')
@login_required
@admin_required
def manage_users():
    users = User.query.filter_by(deleted=False).all()
    return render_template('admin/manage_users.html', users=users)

# 📰 What's New? — Launch new song notifications
@admin_bp.route('/notifications', methods=['GET', 'POST'])
@login_required
@admin_required
def notifications():
    form = NotificationForm()
    if form.validate_on_submit():
        notif = Notification(
            message=form.message.data,
            sender=None  # Optionally set to current_user.username
        )
        db.session.add(notif)
        db.session.commit()
        flash('Notification sent!', 'success')
        return redirect(url_for('admin.notifications'))
    notifications = Notification.query.order_by(Notification.timestamp.desc()).all()
    return render_template('admin/notifications.html', form=form, notifications=notifications)

# 🗑️ Graveyard — Recycle bin (restore deleted users or songs)
@admin_bp.route('/graveyard')
@login_required
@admin_required
def graveyard():
    deleted_users = User.query.filter_by(deleted=True).all()
    deleted_songs = Song.query.filter_by(deleted=True).all()
    return render_template('admin/graveyard.html', deleted_users=deleted_users, deleted_songs=deleted_songs)

@admin_bp.route('/restore-user/<int:user_id>')
@login_required
@admin_required
def restore_user(user_id):
    user = User.query.get_or_404(user_id)
    user.deleted = False
    db.session.commit()
    flash('User restored successfully!', 'success')
    return redirect(url_for('admin.graveyard'))

@admin_bp.route('/restore-song/<int:song_id>')
@login_required
@admin_required
def restore_song(song_id):
    song = Song.query.get_or_404(song_id)
    song.deleted = False
    db.session.commit()
    flash('Song restored successfully!', 'success')
    return redirect(url_for('admin.graveyard'))

@admin_bp.route('/edit-song/<int:song_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_song(song_id):
    song = Song.query.get_or_404(song_id)
    form = SongForm(obj=song)
    if form.validate_on_submit():
        form.populate_obj(song)
        db.session.commit()
        flash('Song updated successfully!', 'success')
        return redirect(url_for('admin.manage_songs'))
    return render_template('admin/add_song.html', form=form, edit_mode=True, song=song)

@admin_bp.route('/delete-song/<int:song_id>')
@login_required
@admin_required
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    song.deleted = True
    db.session.commit()
    flash('Song deleted successfully!', 'success')
    return redirect(url_for('admin.manage_songs'))

@admin_bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin_bp.route('/delete-user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    user.deleted = True
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/firebase-integration', methods=['GET', 'POST'])
def firebase_integration():
    # Initialize Firebase if not already
    if not firebase_admin._apps:
        cred_path = os.path.join(os.getcwd(), 'firebase_key.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    db_firestore = firestore.client()

    # Get all collection names (as strings)
    collections = [c.id for c in db_firestore.collections()]

    # Handle new collection creation
    if request.method == 'POST' and 'new_collection' in request.form:
        new_collection = request.form['new_collection'].strip()
        if not new_collection:
            flash('Collection name cannot be empty.', 'danger')
            return redirect(url_for('admin.firebase_integration'))
        if new_collection in collections:
            flash('Collection already exists.', 'warning')
            return redirect(url_for('admin.firebase_integration', collection=new_collection))
        # Create a dummy doc to create the collection
        db_firestore.collection(new_collection).add({'_init': True})
        flash(f'Collection "{new_collection}" created!', 'success')
        return redirect(url_for('admin.firebase_integration', collection=new_collection))

    # Determine selected collection
    selected_collection = request.form.get('collection') or request.args.get('collection')
    items = []
    edit_item = None

    if selected_collection:
        collection = db_firestore.collection(selected_collection)

        # Handle add
        if request.method == 'POST' and 'item_name' in request.form:
            item_name = request.form['item_name']
            item_description = request.form.get('item_description', '')
            collection.add({'name': item_name, 'description': item_description})
            flash('Item added to Firebase!', 'success')
            return redirect(url_for('admin.firebase_integration', collection=selected_collection))

        # Handle delete
        delete_id = request.args.get('delete')
        if delete_id:
            doc_ref = collection.document(delete_id)
            doc_ref.delete()
            flash('Item deleted from Firebase!', 'success')
            return redirect(url_for('admin.firebase_integration', collection=selected_collection))

        # Handle edit
        edit_id = request.args.get('edit')
        if edit_id and request.method == 'POST' and 'new_name' in request.form:
            new_name = request.form['new_name']
            new_description = request.form.get('new_description', '')
            doc_ref = collection.document(edit_id)
            doc_ref.update({'name': new_name, 'description': new_description})
            flash('Item updated in Firebase!', 'success')
            return redirect(url_for('admin.firebase_integration', collection=selected_collection))

        # Fetch all items in the selected collection
        for doc in collection.stream():
            data = doc.to_dict()
            data['id'] = doc.id
            items.append(data)

        # If editing, show edit form for that item
        edit_id = request.args.get('edit')
        if edit_id:
            doc = collection.document(edit_id).get()
            if doc.exists:
                edit_item = {'id': doc.id, 'name': doc.to_dict().get('name', ''), 'description': doc.to_dict().get('description', '')}

    return render_template('firebase_integration.html',
                           collections=collections,
                           selected_collection=selected_collection,
                           items=items,
                           edit_item=edit_item)
