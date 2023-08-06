# YT_Downloader

Package for aquiring binary data for YT videos with age restrictions.

# Usage

To use in your project include 'import YTDownloader'

Create a class object passing a url (for a YouTube video) string like:
	yt = YTDownloader.AgeRestrictedYTVideo(<url-here>)
	
Query if video is age restricted like:
	age_restricted = yt.is_age_restricted()
	
Either way, a binary object for the video is returned by:
	bytes_obj = yt.get_video()

