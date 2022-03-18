# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:57:48 2021

@author: A curious developer _/\_

@Help: https://developers.google.com/youtube/v3/docs/playlists/list

Install Google Client library :
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

NOTE- Only 3 Things to change in code:
    CLIENT_SECRET_FILE
    playlistId_Source
    playlistId_Target

"""

from Google import Create_Service
import sys
#import pandas as pd

API_NAME  =  'youtube'
# Genrate and paste .json key file below. From google api console - https://console.cloud.google.com/apis/dashboard
# and Enable YouTube Data API v3 & then publish your project
# For help refer: https://www.youtube.com/watch?v=6bzzpda63H0
CLIENT_SECRET_FILE  =  'client_secret_##########################.apps.googleusercontent.com.json'

API_VERSION  =  'v3'
VISIBILITY = 'videoPublishedAt'
SCOPES  = ['https://www.googleapis.com/auth/youtube']

service =  Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Add the Public source (from) and target (to) your playlist ID (not complete url)
playlistId_Source = 'PLl0##########################h8G'
playlistId_Target = 'PLh############################89'

try:
    
    response = service.playlistItems().list(
        part='contentDetails',
        playlistId=playlistId_Source,
        maxResults=50
    ).execute()
    
    playlistItems = response['items']
    nextPageToken = response.get('nextPageToken')
    
    while nextPageToken:
        response = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlistId_Source,
            maxResults=50,
            pageToken=nextPageToken
        ).execute()
    
        playlistItems.extend(response['items'])
        nextPageToken = response.get('nextPageToken')
        
    print("\n" + str(len(playlistItems)) + " Videos found in this playlist.\n");
    
    i = 0;
    
    for video in playlistItems:    
        i=i+1
        print("Video " + str(i) + " cloned")
        
        if(VISIBILITY in video["contentDetails"]):
            print()
            request_body = {
                'snippet': {
                    'playlistId': playlistId_Target,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video['contentDetails']['videoId']
                    }
                }
            }
            service.playlistItems().insert(
                part='snippet',
                body=request_body
            ).execute()        
        else:
            print("[ SKIPPING PRIVATE/DELETED VIDEO ]")
            
    
    print("\nSuccessfully Cloned the complete Playlist :)")

except Exception as e:
    #print(e)
    # Get current system exception
    ex_type, ex_value, ex_traceback = sys.exc_info()
    
    print("\nSome issue popped up during the execution :(\n")
    print("Exception type : %s " % ex_type.__name__)
    print("Exception message : %s" %ex_value)