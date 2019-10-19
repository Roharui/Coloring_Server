
from requests import get
import json

class ColorManager:
    api_url = 'https://api.color.pizza/v1/{0}'
    def api_use(self, url):
        return get(url).text
    def getName(self, code):
        rgb = self.rgbToHex(list(map(int, code)))
        _ = self.api_use(self.api_url.format(rgb))
        json_dict = json.loads(_)['colors'][0]
        return json_dict
    def rgbToHex(self, rgb):
        return '{0:02x}{1:02x}{2:02x}'.format(rgb[0], rgb[1], rgb[2])
        
if __name__ == '__main__':
    a = ColorManager()
    a.getName((0,0,255))