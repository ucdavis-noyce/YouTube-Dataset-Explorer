def map_ideology(ideology):
    return {
        "Left": "Far Left",
        "Center-left": "Left",
        "Center": "Moderate",
        "Center-right": "Right",
        "Right": "Far Right"
    }[ideology]


def get_videos(puppet):
    videos = set()
    for action in puppet['actions']:
        if action['action'] == 'watch':
            videos.add(action['params'])
        if action['action'] == 'get_homepage' or action['action'] == 'get_recommendations':
            for videoId in action['params']:
                videos.add(videoId)
    return videos

def get_common_videos(topVideos):
    sets = [
        set(topVideos.get('Far Left', [])),
        set(topVideos.get('Moderate', [])),
        set(topVideos.get('Far Right', []))
    ]
    return list(set.intersection(*sets))
