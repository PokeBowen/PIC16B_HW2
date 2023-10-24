# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    """
    
    """
    
    name = 'tmdb_spider'
    
    start_urls = ["https://www.themoviedb.org/movie/5255-the-polar-express"]
    
    def parse(self, response):
        """
        
        """
        
        yield response.follow("/movie/5255-the-polar-express/cast", callback = self.parse_full_credits)
        
    def parse_full_credits(self, response):
        """
        
        """
        
        # go into first <section class="panel pad">
        # go into each <div class="info">
        # grab first (out of the three) <a href="[link here]"> for each actor
        # make the links full links, push into list
        crew = response.css("section.panel")[0]
        cast_links = crew.css("div.info a::attr(href)").getall()
        #how to get only every 3rd link? :first-of-type::attr(href)
        
        iterable = response.follow_all(cast_links, callback = self.parse_actor_page)
        for item in iterable:
            yield item
        
    def parse_actor_page(self, response):
        """
        
        """
        actor_name = response.css("div.title h2.title a::text").get()
        
        acted_in_block = response.css("table.card")
        acted_in_list = response.css("a.tooltip bdi::text").getall()
        
        for movie_or_TV_name in acted_in_list:
            Dict = {"actor": actor_name, "movie_or_TV_name" : movie_or_TV_name} 
            yield Dict
        