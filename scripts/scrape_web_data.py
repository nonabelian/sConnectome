import os
from urllib import urlretrieve

import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    data_folder = 'data' + os.sep

    url = 'https://openfmri.org/dataset/ds000115/'

    req = requests.get(url)

    soup = BeautifulSoup(req.content, 'html.parser')

    ahref_urls = soup.select('.unrevisioned_links')[0].findChildren('a')
    data_urls = []

    for a in ahref_urls:
        data_urls.append(a['href'])

    print '-' * 40
    print 'Data Urls:'
    print '-' * 40
    for du in data_urls:
        print du

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    for u in data_urls:
        filename = u.split('/')[-1]
        save_file = os.path.join(data_folder, filename)

        print 'Downloading ' + filename + ' ... ',

        urlretrieve(u, save_file)

        print 'Done'
