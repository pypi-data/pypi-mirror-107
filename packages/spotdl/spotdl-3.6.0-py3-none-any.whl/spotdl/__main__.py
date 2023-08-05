# ! Basic necessities to get the CLI running
import signal
import sys
import argparse
import os

# ! The actual download stuff
from spotdl.download.downloader import DownloadManager
from spotdl.search.songObj import SongObj
from spotdl.search.spotifyClient import SpotifyClient
# ! Song Search from different start points
from spotdl.search.utils import (
    get_playlist_tracks,
    get_album_tracks,
    get_artist_tracks,
    get_saved_tracks,
    search_for_song,
)
from spotdl.download import ffmpeg

# ! Usage is simple - call:
#   'python __main__.py <links, search terms, tracking files separated by spaces>
# ! Eg.
# !      python __main__.py
# !          https://open.spotify.com/playlist/37i9dQZF1DWXhcuQw7KIeM?si=xubKHEBESM27RqGkqoXzgQ
# !          'old gods of asgard Control'
# !          https://open.spotify.com/album/2YMWspDGtbDgYULXvVQFM6?si=gF5dOQm8QUSo-NdZVsFjAQ
# !          https://open.spotify.com/track/08mG3Y1vljYA6bvDt4Wqkj?si=SxezdxmlTx-CaVoucHmrUA
# !
# ! Well, yeah its a pretty long example but, in theory, it should work like a charm.
# !
# ! A '.spotdlTrackingFile' is automatically  created with the name of the first song in the
# ! playlist/album or the name of the song supplied. We don't really re re re-query YTM and Spotify
# ! as all relevant details are stored to disk.
# !
# ! Files are cleaned up on download failure.
# !
# ! All songs are normalized to standard base volume. the soft ones are made louder,
# ! the loud ones, softer.
# !
# ! The progress bar is synched across multiple-processes (4 processes as of now), getting the
# ! progress bar to synch was an absolute pain, each process knows how much 'it' progressed,
# ! but the display has to be for the overall progress so, yeah... that took time.
# !
# ! spotdl will show you its true speed on longer download's - so make sure you try
# ! downloading a playlist.
# !
# ! still yet to try and package this but, in theory, there should be no errors.
# !
# !                                                          - cheerio! (Michael)
# !
# ! P.S. Tell me what you think. Up to your expectations?

# ! Script Help
help_notice = '''
To download a song run,
    spotdl [trackUrl]
    ex. spotdl https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b

To download a album run,
    spotdl [albumUrl]
    ex. spotdl https://open.spotify.com/album/4yP0hdKOZPNshxUOjY0cZj

To download a playlist, run:
    spotdl [playlistUrl]
    ex. spotdl https://open.spotify.com/playlist/37i9dQZF1E8UXBoz02kGID

To download all songs from an artist run:
    spotdl [artistUrl]
    ex. spotdl https://open.spotify.com/artist/1fZAAHNWdSM5gqbi9o5iEA

To download your saved songs, run:
    spotdl --user-auth saved

To change output format run:
    spotdl [songUrl] --output-format mp3/m4a/flac/opus/ogg
    ex. spotdl [songUrl] --output-format opus

To use ffmpeg binary that is not on PATH run:
    spotdl [songUrl] --ffmpeg path/to/your/ffmpeg.exe
    ex. spotdl [songUrl] --ffmpeg C:\ffmpeg\bin\ffmpeg.exe

To ignore your ffmpeg version run:
    spotdl --ignore-ffmpeg-version

To search for and download a song, run, with quotation marks:
Note: This is not accurate and often causes errors.
    spotdl [songQuery]
    ex. spotdl 'The Weeknd - Blinding Lights'

To resume a failed/incomplete download, run:
    spotdl [pathToTrackingFile]
    ex. spotdl 'The Weeknd - Blinding Lights.spotdlTrackingFile'

    .spotdlTrackingFiles are automatically created when a download starts and deleted on completion

You can queue up multiple download tasks by separating the arguments with spaces:
    spotdl [songQuery1] [albumUrl] [songQuery2] ... (order does not matter)
    ex. spotdl 'The Weeknd - Blinding Lights'
            https://open.spotify.com/playlist/37i9dQZF1E8UXBoz02kGID ...

You can use the --debug-termination flag to figure out where in the code spotdl got stuck.

spotDL downloads up to 4 songs in parallel, so for a faster experience,
download albums and playlist, rather than tracks.
'''


def console_entry_point():
    '''
    This is where all the console processing magic happens.
    Its super simple, rudimentary even but, it's dead simple & it works.
    '''
    arguments = parse_arguments()
    args_dict = vars(arguments)

    if ffmpeg.has_correct_version(
        arguments.ignore_ffmpeg_version,
        arguments.ffmpeg or "ffmpeg"
    ) is False:
        sys.exit(1)

    for request in arguments.url:
        if 'saved' == request and not arguments.userAuth:
            arguments.userAuth = True
            print("Detected 'saved' in command line, but no --user-auth flag. Enabling Anyways.")
            print("Please Log In...")

    SpotifyClient.init(
        client_id='5f573c9620494bae87890c0f08a60293',
        client_secret='212476d9b0f3472eaa762d90b19b0ba8',
        user_auth=arguments.userAuth
    )

    if arguments.path:
        if not os.path.isdir(arguments.path):
            sys.exit("The output directory doesn't exist.")
        print(f"Will download to: {os.path.abspath(arguments.path)}")
        os.chdir(arguments.path)

    with DownloadManager(args_dict) as downloader:
        if not arguments.debug_termination:
            def gracefulExit(signal, frame):
                downloader.displayManager.close()
                sys.exit(0)

            signal.signal(signal.SIGINT, gracefulExit)
            signal.signal(signal.SIGTERM, gracefulExit)

        for request in arguments.url:
            if 'open.spotify.com' in request and 'track' in request:
                print('Fetching Song...')
                song = SongObj.from_url(request)

                if song is not None:
                    if song.get_youtube_link() is not None:
                        downloader.download_single_song(song)
                    else:
                        print('Skipping %s (%s) as no match could be found on youtube' % (
                            song.get_song_name(), request
                        ))

            elif 'open.spotify.com' in request and 'album' in request:
                print('Fetching Album...')
                songObjList = get_album_tracks(request)

                downloader.download_multiple_songs(songObjList)

            elif 'open.spotify.com' in request and 'playlist' in request:
                print('Fetching Playlist...')
                songObjList = get_playlist_tracks(request)

                downloader.download_multiple_songs(songObjList)

            elif 'open.spotify.com' in request and 'artist' in request:
                print('Fetching artist...')
                artistObjList = get_artist_tracks(request)

                downloader.download_multiple_songs(artistObjList)

            elif request.endswith('.spotdlTrackingFile'):
                print('Preparing to resume download...')
                downloader.resume_download_from_tracking_file(request)

            elif request == "saved":
                print('Fetching Saved Songs...')
                songObjList = get_saved_tracks()
                downloader.download_multiple_songs(songObjList)

            else:
                print('Searching for song "%s"...' % request)
                try:
                    song = search_for_song(request)
                    downloader.download_single_song(song)
                except Exception as e:
                    print(e)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="spotdl",
        description=help_notice,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", type=str, nargs="+", help="URL to a song/album/playlist")
    parser.add_argument("--debug-termination", action="store_true")
    parser.add_argument("-o", "--output", help="Output directory path", dest="path")
    parser.add_argument("-of", "--output-format", help="Output format", dest="format",
                        choices={"mp3", "m4a", "flac", "ogg", "opus"}, default="mp3")
    parser.add_argument(
        "--user-auth",
        help="Use User Authentication",
        action='store_true',
        dest="userAuth"
    )
    parser.add_argument("-f", "--ffmpeg", help="Path to ffmpeg", dest="ffmpeg")
    parser.add_argument("--ignore-ffmpeg-version",
                        help="Ignore ffmpeg version", action="store_true")

    return parser.parse_args()


if __name__ == '__main__':
    console_entry_point()
