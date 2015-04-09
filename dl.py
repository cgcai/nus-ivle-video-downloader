import argparse
from selenium import webdriver


IVLE_WORKSPACE = 'https://ivle.nus.edu.sg/default.aspx'


class IVLE(object):
    def __init__(self, session):
        self.session = session

    def __del__(self):
        pass

    def get_mp4_url(self, webcast_url):
        browser = IVLE.get_logged_in_browser(self.session)
        browser.get(webcast_url)
        print(browser.current_url)
        browser.quit()

    @staticmethod
    def get_logged_in_browser(session):
        browser = webdriver.Firefox()
        browser.get('https://ivle.nus.edu.sg/default.aspx')
        browser.add_cookie({
            'name': 'ivle12',
            'domain': 'ivle.nus.edu.sg',
            'value': session,
            'path': '/'
        })
        return browser


def main(args):
    ivle = IVLE(args.ivle12)
    ivle.get_mp4_url(args.url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('IVLE Webcast Downloader')
    parser.add_argument('ivle12', type=str, help='Session Cookie')
    parser.add_argument('url', type=str, help='Webcast URL')
    args = parser.parse_args()
    main(args)
