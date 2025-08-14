def process_track_data(data: dict)-> dict:
    track_data = []
    tracks = data.get('tracks', [])
    for track in tracks:
        track_id = track.get('trackID')
        track_name = track.get('name')
        country_id = track.get('countryid')
        country_name = track.get('countryName')
        timezone = track.get('timezone')
        isdst = track.get('isdst')
        timezone_offset = track.get('timezoneOffset')
        code = track.get('code')
        video_code = track.get('videoCode')
        track_type_id = track.get('trackType')
        track_data.append({
            'track_id': track_id,
            'track_name': track_name,
            'country_id': country_id,
            'country_name': country_name,
            'timezone': timezone,
            'isdst': isdst,
            'timezone_offset': timezone_offset,
            'code': code,
            'video_code': video_code,
            'track_type_id': track_type_id
        })
    return track_data



