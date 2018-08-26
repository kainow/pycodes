import sqlite3

# 空欄を埋めてsearcher関数を完成させてください。
class searcher:
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        
    def __del__(self):
        self.conn.close()
    
    # 検索
    def get_match_rows(self,q):
        columnlist = 'w0.url'
        tablelist = ''
        conditionlist = ''
        words_list = []

        words = q.split(' ')
        tablenumber = 0
        for word in words:
            wordrow = self.conn.execute("select word from wordlist where word='%s'" %word).fetchone()
            if wordrow :
                words_list.append(word)
                if tablenumber > 0:
                    tablelist += ','
                    conditionlist += ' and w%d.url=w%d.url and ' % (tablenumber-1,tablenumber)
                columnlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                conditionlist+="w%d.word='%s'" % (tablenumber,word) 
                tablenumber += 1
            else:
                print('含まなかった単語を含むページはありません')
                return None,words_list


        sql="select %s from %s where %s" % (columnlist,tablelist,conditionlist)
        
        try:
            cur=self.conn.execute(sql)
        except:
            print('探しているページは見つかりませんでした。')
            row = []
            return None,words_list
        
        rows=[row for row in cur]
        return rows,words_list

    # 正規化
    def normalizescores(self, scores, small_flag=0):
        vsmall = 0.00001
        if small_flag:
            minscore = min(scores.values())
            return dict([(url,float(minscore)/max(vsmall,l)) for (url,l) in scores.items()])
        else:
            # 値が大きいほうが１となる正規化関数を完成させてください。
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(url,float(count) / maxscore) for (url,count) in scores.items()])

    # 単語の出現頻度を計算
    def frequeryscore(self, rows):
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] += 1
        return self.normalizescores(counts)

    # 単語の出現した位置で評価
    def locationscore(self, rows):
        locations = dict([(row[0],1000000) for row in rows])
        for row in rows:
            location = sum(row[1:])
            if location < locations[row[0]]:
                locations[row[0]] = location
            return self.normalizescores(locations, small_flag=1)
    
    # 単語間の距離を評価
    def distancescore(self,rows):
        if len(rows[0]) <= 2:
            return dict([(row[0],1.0) for row in rows])
        mindistance = dict([(row[0],1000000) for row in rows])
        for row in rows:
            dist = sum([abs(row[i] - row[i-1]) for i in range(2,len(row))])
            if dist < mindistance[row[0]]:
                mindistance[row[0]] = dist
        return self.normalizescores(mindistance, small_flag=1)

    # PageRankで重みづけ
    def pagerankscore(self,rows):
        pagerank = dict([(row[0], self.conn.execute("select score from pagerank where url = '%s'" % row[0]).fetchone()[0]) for row in rows])
        return self.normalizescores(pagerank)

    # 重みづけ
    def weightlist(self,rows):
        totalscores = dict([(row[0],0) for row in rows])
        # 評価関数を設定してください。
        # 評価関数の重みは、frequeryscore : 1 , locationscore : 2 , distancescore : 2 ,pagerankscore :3 としてください。
        weights = [(1.0, self.frequeryscore(rows))
                    ,(2.0, self.locationscore(rows))
                    ,(2.0, self.distancescore(rows))
                    ,(3.0, self.pagerankscore(rows))]

        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight * scores[url]
        return totalscores


    # レコメンド
    def query(self, q):
        rows,words = self.get_match_rows(q)
        if not rows:
            return [('探しているページは見つかりませんでした。','')]
        scores = self.weightlist(rows)
        rankedscores = sorted([(score, url) for (url,score) in scores.items()], reverse = 1)
        recommend_list = []
        for i,(score, url) in enumerate(rankedscores[0:10]):
            recommend_list.append((url,score))
        return recommend_list

# program studyで検索してください。
dbname = "webpage.db"
s = searcher(dbname)
query = "program study"
urls_list = s.query(query)
for url,score in urls_list:
    print(score,url)