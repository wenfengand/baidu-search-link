import requests
import re 
import json 
import time 

link_re = re.compile('w.location.replace\("(.*)"\)')
next_page_re = re.compile('<a href="(.*?)".*下一页')
encrypt_links_re = re.compile('data-tools=\'(.*?)\'')
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}

s = requests.session()
s.headers.update(headers)  
def decrypt_links(urls):
    ret_links = []
    for url in urls:
        ret = s.get(url, headers=headers, allow_redirects=False)

        links = link_re.findall(ret.text)
        if len(links) > 0:
            ret_links.append(links[0])
        else:
            # can't get it from html content, maybe it's in headers
            if 'Location' in ret.headers:
                ret_links.append(ret.headers['Location'])
            else:
                pass 
    return ret_links 
def all_pages(target_domin):
    items = []
    baidu = 'http://baidu.com'
    url = baidu + '/s?wd=site:' + target_domin 

    while url:
        ret = s.get(url, headers=headers) 

        encrypt_links = encrypt_links_re.findall(ret.text) 

        
        for item in encrypt_links:
            encrypt_item = json.loads(item)
            encrypt_item['url'] = decrypt_links([encrypt_item['url']])[0]
            items.append(encrypt_item) 
        

        print('we got %d links ' %(len(items)))
        
        text = ret.text.replace('</a>', '</a>\n')
        next_url = next_page_re.findall(text)
        if  len(next_url)> 0:
            url = baidu + next_url[0]
        else:
            url = None 
        print('next page url', url)
        time.sleep(3)
    return items

if __name__ == '__main__':
    '''
    # test decrypt_links
    urls = ['http://www.baidu.com/link?url=JT8hs4rZuuq4HGyt7e2r6cz9b4DYvu7KcBGiINtjQlOYE3pDQOKvc5zBCThY08WN&wd=&eqid=f1a0ea1c00049fa9000000035cbabaa0']
    real_links = decrypt_links(urls)
    print(real_links)
    '''
    domin = 'blog.stackoverflow.club'
    print(all_pages(domin) )