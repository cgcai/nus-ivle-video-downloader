IVLE Video Downloader
=====================

A quick hack to download webcasts for offline viewing.

## Downloading a single file

    $ python3 dl.py <ivle12 cookie here> --webcast "javascript:void(winopenprompt('../bank/media/viewmedia.aspx?MediaItemID=xxx&ChannelID=yyy','470','430','yes','yes'))"

## Downloading all files on the IVLE Multimedia page:

    $ python3 dl.py <ivle12 cookie here> "https://ivle.nus.edu.sg/media/multimedia.aspx?ChannelID=xxx&ClickFrom=Outline"

## Known Issues
This is a hack. We don't handle errors.

## Why does the downloaded file only have audio?
Probably the fault of the webcast. (This is why you should actually attend lectures.)

## Why Selenium?
Because IVLE's media server uses JavaScript to create the `<video>` tag.
