# -*- coding: UTF-8 -*-
"""
reCAPTCHA v2 via proxy solving example
"""

import os

import requests
from lxml import html
from unicaps import CaptchaSolver, exceptions
from unicaps.proxy import ProxyServer

URL = 'https://www.google.com/search?complete=0&hl=en&q=unicaps&num=100&start=1&filter=0&pws=0'
POST_URL = 'https://www.google.com/sorry/index'
API_KEY = os.getenv('2CAPTCHA_API_KEY', default='YOUR_API_KEY')
PROXY = os.getenv('HTTP_PROXY_SERVER', default='http://<LOGIN>:<PASSWORD>@<YOUR_PROXY_ADDRESS>:<PORT>')


def solve(service_name, api_key):
    """ Get and solve CAPTCHA """

    # User-Agent
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/84.0.4147.89 Safari/537.36")

    # init captcha solver
    solver = CaptchaSolver(service_name, api_key)

    # make a session, set proxy and User-Agent
    session = requests.Session()
    session.proxies.update(dict(http=PROXY, https=PROXY))
    session.headers.update({'User-Agent': user_agent})
    # go to URL
    response = session.get(URL)

    # parse page and get site-key
    page = html.document_fromstring(response.text)

    recaptcha_tag = page.cssselect('.g-recaptcha')
    if not recaptcha_tag:
        print('reCAPTCHA didn\'t appear for Google search (a good proxy used!)')
        return

    # extract sitekey and data-s values
    site_key = recaptcha_tag[0].attrib['data-sitekey']
    data_s = recaptcha_tag[0].attrib['data-s']

    # parse form data
    page_form_data = page.xpath('//form//input')
    form_data = {}
    for input_data in page_form_data:
        form_data[input_data.xpath('@name')[0]] = input_data.xpath('@value')[0]

    # solve reCAPTCHA
    try:
        solved = solver.solve_recaptcha_v2(
            site_key=site_key,
            page_url=URL,
            data_s=data_s,
            proxy=ProxyServer(PROXY),
            user_agent=user_agent,
            cookies=session.cookies.get_dict()
        )
    except exceptions.UnicapsException as exc:
        print('reCAPTCHA v2 (via proxy) solving exception: %s' % exc)
        return

    # add token to form data
    form_data['g-recaptcha-response'] = solved.solution.token

    # post form data
    response = session.post(POST_URL, data=form_data)
    page = html.document_fromstring(response.text)

    # check the result
    search_results = [link.attrib.get('href') for link in page.xpath('//div[@class="r"]/a')]
    if search_results:
        print('reCAPTCHA v2 (proxy) solved successfully!')
        # report good CAPTCHA
        solved.report_good()
    else:
        print('reCAPTCHA v2 (proxy) wasn\'t solved!')
        # report bad CAPTCHA
        solved.report_bad()


if __name__ == '__main__':
    solve('2captcha.com', API_KEY)
