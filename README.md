IVLE Video Downloader
=====================

A quick hack to download webcasts for offline viewing.

## Downloading a single file

    $ python3 dl.py <ivle12 cookie here> --webcast "javascript:void(winopenprompt('../bank/media/viewmedia.aspx?MediaItemID=xxx&ChannelID=yyy','470','430','yes','yes'))"

## Downloading all files on the IVLE Multimedia page:

    $ python3 dl.py <ivle12 cookie here> --medialist "https://ivle.nus.edu.sg/media/multimedia.aspx?ChannelID=xxx&ClickFrom=Outline"

## Dependencies
1. Firefox

## Known Issues
This is a hack. We don't handle errors.

1. If you have Silverlight installed, the `<video>` tag won't be generated, and this script will fail. As a workaround, temporarily disable Silverlight. A better solution would be to initialize Selenium with a Firefox profile that has plugins disabled. Feel free to PR this.

## Why does the downloaded file only have audio?
Probably the fault of the webcast. (This is why you should actually attend lectures.)

## Why Selenium?
Because IVLE's media server uses JavaScript to create the `<video>` tag.
