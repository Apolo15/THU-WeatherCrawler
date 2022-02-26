class Entity_cctvnews:
    def __init__(self, id,time, title, url,url2, title_2, sourceandtime, content, author):
        self.id=id
        self.time = time
        self.title = title
        self.url = url
        self.url2 = url2
        self.title_2 = title_2
        self.sourceandtime = sourceandtime
        self.content = content
        self.author = author

    def print(self):
        print(
              self.id,
              self.time,
              self.title,
              self.url,
              self.url2,
              self.title_2,
              self.sourceandtime,
              self.content,
              self.author,

              )


class Entity_cctvnews_tu:
    def __init__(self, time, title, url):

        self.time = time
        self.title = title
        self.url = url

    def print(self):
        print(
              self.time,
              self.title,
              self.url,

              )



