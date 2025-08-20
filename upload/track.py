import traceback
from database.general import session_scope, FirstTrack
from utils.logger import logger_1st


def upload_track_data(track: dict, overwrite: bool = False):
    try:
        with session_scope() as session:
            existing_track = session.query(FirstTrack).filter(FirstTrack.track_id == track['track_id']).first()
            if existing_track:
                if overwrite:
                    existing_track.track_name = track.get('track_name')
                    existing_track.country_id = track.get('country_id')
                    existing_track.country_name = track.get('country_name')
                    existing_track.timezone = track.get('timezone')
                    existing_track.isdst = track.get('isdst')
                    existing_track.timezone_offset = track.get('timezone_offset')
                    existing_track.code = track.get('code')
                    existing_track.video_code = track.get('video_code')
                    existing_track.track_type_id = track.get('track_type_id')

            else:
                new_track = FirstTrack(
                    track_id = track.get('track_id'),
                    track_name = track.get('track_name'),
                    country_id = track.get('country_id'),
                    country_name = track.get('country_name'),
                    timezone = track.get('timezone'),
                    isdst = track['isdst'],
                    timezone_offset = track['timezone_offset'],
                    code = track.get('code'),
                    video_code = track.get('video_code'),
                    track_type_id = track.get('track_type_id'),
                )
                session.add(new_track)
        return True
    except Exception as e:
        logger_1st.error(f'upload_track_data(): {e}')
        logger_1st.error(traceback.format_exc())
        return False
    