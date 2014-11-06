import redis
import base64
import md5
import config


class UrlShortener:
    def __init__(self):
        url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
        self.redis = redis.Redis(host=url.hostname, port=url.port,
                                 password=url.password)
        # self.redis = redis.StrictRedis(host=config.REDIS_HOST,
        #                                port=config.REDIS_PORT,
        #                                db=config.REDIS_DB)

    def shortcode(self, url):
        """
        for URLs the potential for collision in the 32 last bits
        of the MD5 hash is rather unlikely.
        The following things happen, in order:
        * compute the md5 digest of the given source
        * extract the lower 4 bytes
        * base64 encode the result
        * remove trailing padding if it exists
        Of course, should a collision happen, we will evict the previous
        key.
        """
        return base64.b64encode(
            md5.new(url).digest()[-4:]).replace('=', '').replace('/', '_')

    def shorten(self, url):
        """
        Set the value of the url to the key.
        Minimal workflow to this.
        Return a dictionary(always xD)
        """
        code = self.shortcode(url)
        try:
            self.redis.set(config.REDIS_PREFIX + code, url)
            return {'success': True,
                    'url': url,
                    'code': code,
                    'shorturl': config.URL_PREFIX + code}
        except:
            return {'success': False}

    def lookup(self, code):
        """
        Lookup the key and return None if the key isn't present
        """
        try:
            return self.redis.get(config.REDIS_PREFIX + code)
        except:
            return None
