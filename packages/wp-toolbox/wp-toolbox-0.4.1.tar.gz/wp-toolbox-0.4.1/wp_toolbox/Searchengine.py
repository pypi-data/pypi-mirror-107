from elasticsearch import Elasticsearch

import wp_toolbox.Elements as WP


class Queries(object):
    def __init__(self, url, port):
        self.cursor = Elasticsearch([url + ":" + str(port)])

    def match(self, ind, layer, query, size, source):
        q = {
            "query": {
                "match": {
                    layer: query,
                }
            },
            "size": size,
            "_source": source
        }
        res = self.cursor.search(index=ind, request_timeout=30, body=q)
        results = []
        for record in res["hits"]["hits"]:
            results.append(record["_source"]["subcorpus"])
        return results

    def matchPhrase(self, ind, layer, query, slop, size, source):
        q = {
            "query": {
                "match_phrase": {
                    layer: {
                        "query": query,
                        "slop": slop
                    }
                },                
            },
            
            "size": size,
            "_source": source,
            "track_total_hits": True
        }
        res = self.cursor.search(index=ind, request_timeout=30, body=q)

        return res


class Result():
    def __init__(self, id, score, subcorpus, articleId, token, lemma, pos):
        self.id = id
        self.score = score
        self.subcorpus = subcorpus
        self.articleId = articleId

        self.sentence = WP.Sentence()
        token = token.split(" ")
        lemma = lemma.split(" ")
        pos = pos.split(" ")
        print(token, len(token))
        print(lemma, len(lemma))
        print(pos, len(pos))
        for i in range(0, len(token)):
            t = WP.Token(token[i], lemma[i], pos[i], "", "", -1, -1)
            self.sentence.tokens.append(t)
