import os
from flask import request, current_app
from werkzeug.utils import secure_filename
from .. import db
from ..models import Mural, Language, Artist, ArtistTranslation, MuralPhoto, MuralTranslation
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import uuid


def get_address_from_coordinates(lat, lng, lang_code):
    geolocator = Nominatim()
    try:
        location = geolocator.reverse('{}, {}'.format(lat, lng), language=lang_code)
    except GeocoderTimedOut:
        return 'not available'
    except GeocoderUnavailable:
        return 'not available'
    except Exception as e:
        print('Unidentified exception occurred: {}'.format(str(e)))
        return 'not available'

    try:
        road = location.raw['address']['road']
        if lang_code == 'uk':
            road = road.split(' ')[-1].capitalize() + ' ' + ' '.join(road.split(' ')[:-1])
    except KeyError:
        road = ''

    try:
        house_number = location.raw['address']['house_number']
    except KeyError:
        house_number = ''

    return '{} {}'.format(str(road), house_number)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


def save_file(file, new_name):
    filename = secure_filename(file.filename)
    if allowed_file(filename):
        _, extension = os.path.splitext(filename)
        filename = new_name + extension
        file.save(os.path.join(current_app.config['MURAL_IMG_FOLDER'], filename))
        return True, filename
    else:
        return False, None


def save_mural_from_form(mural, form, languages):
    # mural
    mural.lat = form.lat.data
    mural.lng = form.lng.data

    # artist
    artist_id = form.artist.data
    if artist_id == -1:
        mural.artists = []
    else:
        artist = Artist.query.get(artist_id)
        if artist:
            mural.artists = [artist]

    # save mural
    db.session.add(mural)
    db.session.commit()

    # translations
    for lang in languages:
        mural_translation = mural.get_translation(lang.code)
        if mural_translation is None:
            mural_translation = MuralTranslation()
        mural_translation.language_code = lang.code
        mural_translation.mural_id = mural.id

        # address
        mural_translation.address = ''
        field = getattr(form, 'address_{}'.format(lang.code), None)
        if field:
            if field.data:
                mural_translation.address = field.data
            else:
                mural_translation.address = get_address_from_coordinates(mural.lat, mural.lng, lang.code)

        # name
        mural_translation.name = ''
        field = getattr(form, 'name_{}'.format(lang.code), None)
        if field:
            mural_translation.name = field.data

        # description
        mural_translation.description = ''
        field = getattr(form, 'description_{}'.format(lang.code), None)
        if field:
            mural_translation.description = field.data

        db.session.add(mural_translation)
    db.session.commit()

    # photos
    files = request.files.getlist("photo_files")
    new_name = form.photo_rename_to.data
    if not new_name:
        new_name = uuid.uuid4().hex
    for i, file in enumerate(files):
        was_saved, filename = save_file(file, '{}_{}'.format(new_name, i))
        if was_saved:
            photo = MuralPhoto()
            photo.file_name = filename
            photo.copyright_name = form.photo_copyright_name.data
            photo.copyright_url = form.photo_copyright_url.data
            photo.mural_id = mural.id
            db.session.add(photo)
    db.session.commit()