import argparse
import json
import requests
from selenium import webdriver


PUNCTUATION = '~!@#$%^&*(){}[]\\|:;"\'<,>?/'
ESC_TABLE = str.maketrans(PUNCTUATION, '_' * len(PUNCTUATION))


def download_webcast(session, url, target):
    url, cookies = get_webcast_info(session, url)
    download_file(url, cookies, target)


def get_webcast_info(browser, webcast_url, blank_when_done=True):
    browser.get(webcast_url)
    viewer_iframe = browser.find_element_by_css_selector(
        '#aspnetForm > iframe:nth-child(11)').get_attribute('src')
    browser.get(viewer_iframe)
    browser.find_element_by_id('basicVersionToggle').click()
    player_iframe = browser.find_element_by_css_selector(
        '#embedControl > iframe:nth-child(1)').get_attribute('src')
    browser.get(player_iframe)
    url = browser.find_element_by_id('player').get_attribute('href')
    cookies = selenium_cookies_to_requests(browser.get_cookies())
    if blank_when_done:
        browser.get('about:blank')
    return (url, cookies)


def download_file(url, cookies, target, block_size=131072):
    with open(target, 'wb') as f:
        resp = requests.get(url, cookies=cookies, stream=True)
        i = 0
        for block in resp.iter_content(block_size):
            f.write(block)
            i += 1
            print('Got: {} * {}b'.format(i, block_size))


def get_webcasts_on_page(browser, url, blank_when_done=True):
    browser.get(url)
    links = browser.find_elements_by_css_selector(
        '#ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_GV > tbody > tr '
        '> td:nth-child(4) > a:nth-child(2)')
    webcasts = []
    for link in links:
        webcasts.append({
            'title': link.text,
            'url': parse_ivle_href(link.get_attribute('href'))
        })
    if blank_when_done:
        browser.get('about:blank')
    return webcasts


def parse_ivle_href(href):
    url = href[33:]
    url = 'https://ivle.nus.edu.sg' + url[:url.find('\'')]
    return url


def get_logged_in_browser(session, blank_when_done=True):
    browser = webdriver.Firefox()
    browser.get('https://ivle.nus.edu.sg/default.aspx')
    browser.add_cookie({
        'name': 'ivle12',
        'domain': 'ivle.nus.edu.sg',
        'value': session,
        'path': '/'
    })
    browser.implicitly_wait(10)
    if blank_when_done:
        browser.get('about:blank')
    return browser


def selenium_cookies_to_requests(cookies):
    result = {}
    for c in cookies:
        result[c['name']] = c['value']
    return result


def str_to_filename(string):
    return string.translate(ESC_TABLE)


def handle_ivle_media_list(args):
    browser = get_logged_in_browser(args.ivle12)
    webcasts = get_webcasts_on_page(browser, args.medialist)
    for w in webcasts:
        print('Downloading {}...'.format(w['title']))
        path = str_to_filename(w['title']) + '.mp4'
        video_url, cookies = get_webcast_info(browser, w['url'])
        if not args.s:
            download_file(video_url, cookies, path)
        else:
            print(video_url)

    if not args.s:
        browser.quit()


def handle_single_webcast(args):
    browser = get_logged_in_browser(args.ivle12)
    url = parse_ivle_href(args.webcast)
    video_url, cookies = get_webcast_info(browser, url)
    if not args.s:
        download_file(video_url, cookies, 'video.mp4')
        browser.quit()
    else:
        print(video_url)


def main(args):
    if args.medialist:
        handle_ivle_media_list(args)
    elif args.webcast:
        handle_single_webcast(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('IVLE Webcast Downloader')
    parser.add_argument('ivle12', type=str, help='Session Cookie')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--medialist', type=str, help='A webcast directory')
    group.add_argument('--webcast', type=str, help='A single webcast')
    parser.add_argument('-s', action='store_true', required=False,
                        help='Simulate by printing video_url; do not actually'
                        ' download')
    args = parser.parse_args()
    main(args)
