class Image:
    def __init__(self, file, url):
        self.url = url
        self.file = file

class Joke:
    def __init__(self, dict):
        self.category = dict["category"]
        self.type = dict["type"]
        if self.type == "twopart":
            self.joke = {"setup": dict["setup"], "delivery": dict["delivery"]}
        else:
            self.joke = dict["joke"]
        self.flags = Flags(dict["flags"])
        self.id = dict["id"]
        self.safe = dict["safe"]
        self.lang = dict["lang"]
        self.dict = dict

class Flags:
    def __init__(self, flags):
        self.nsfw = flags['nsfw']
        self.religious = flags['religious']
        self.political = flags['political']
        self.racist = flags['racist']
        self.sexist = flags['sexist']
        self.explicit = flags['explicit']
        self.dict = flags
