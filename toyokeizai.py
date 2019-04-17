def titletag(url):
    try:
        html = requests.get(url,allow_redirects = True)
        soup = BeautifulSoup(html.content,"html.parser")
        
        title_tag = soup.title
        
        if title_tag != None:
            title_long = title_tag.string
            
        ttl_list = title_long.split(' | ')
        title= ttl_list[0]
        
        body = soup.find("div", id = "article-body-inner").test.replace('¥n','').replace('¥xa0','').replace('¥u2003','')
        try:
            page_str= soup.find("div",class= "pagination multipage-end").text.replace('¥n','')
        except:
            page_sum = 1
            
        for i in range(page_sum-1):
            try:
                url0 = url.split('?')
                url = url0[0]
                
                except:
                    pass
                next_url = url + "?page="+str(i+2)
                
                html = requests.get(next_url,allow_redirects = True)
                next_spoup = BeautifulSoup(html.content,"html.parser")
                next_body = next_soup.find("div",id= "article-body-inner").text
                body += next_body
            content = body.replace('¥n','').replace('¥xa0').replace('¥u2003','')
            
            return[title,content]
        except:
            return[None,None]
