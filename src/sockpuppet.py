import os
import json
import pickle

from util import get_videos, get_common_videos

PUPPET_DIR = '../../analysis/puppets'
PUPPETS = {}
METADATA = {}
SLANTS = {}
TOP_DAILY = {}

def load_puppets():
    with open('cache/sockpuppets.txt') as f:
        PUPPET_LIST = f.read().strip().split('\n')
        PUPPET_LIST = [p for p in PUPPET_LIST if os.path.exists(os.path.join(PUPPET_DIR, p))]
        PUPPET_LIST = PUPPET_LIST[:100000]

    for puppetId in PUPPET_LIST:
        ideology = puppetId.split(',')[0]
        if ideology not in PUPPETS:
            PUPPETS[ideology] = []
        PUPPETS[ideology].append(puppetId)

def load_metadata():
    global METADATA
    with open('cache/metadata.pickle', 'rb') as f:
        METADATA = pickle.load(f)

def load_slants():
    global SLANTS
    with open('cache/slant-estimates.pickle', 'rb') as f:
        SLANTS = pickle.load(f)

def load_dailytop():
    global TOP_DAILY
    with open('cache/top-daily.pickle', 'rb') as f:
        TOP_DAILY = pickle.load(f)

def get_num_sock_puppets(ideology):
    return len(PUPPETS[ideology])

def get_sock_puppet(ideology, puppetId):
    puppet = PUPPETS[ideology][puppetId]
    with open(os.path.join(PUPPET_DIR, puppet)) as f:
        sockpuppet = json.load(f)
    sockpuppet['metadata'] = get_metadata(get_videos(sockpuppet))
    sockpuppet['slants'] = get_slants(get_videos(sockpuppet))
    return sockpuppet

def get_top_videos(date):
    topVideos = dict(TOP_DAILY[date])
    videos = set()
    for label in topVideos:
        for video in topVideos[label]:
            videos.add(video)
    topVideos['metadata'] = get_metadata(videos)
    topVideos['slants'] = get_slants(videos)
    topVideos['common_videos'] = get_common_videos(topVideos)
    return topVideos

def get_metadata(videos):
    metadata = {}
    for videoId in videos:
        metadata[videoId] = METADATA.get(videoId, {})
    return metadata

def get_slants(videos):
    slants = {}
    for videoId in videos:
        slants[videoId] = SLANTS.get(videoId, {})
    return slants
    
def get_dates():
    return sorted(TOP_DAILY.keys())

load_puppets()
load_metadata()
load_slants()
load_dailytop()
