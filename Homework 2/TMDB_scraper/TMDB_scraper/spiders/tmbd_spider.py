# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    """
    A page crawler for themoviedb.org
    
    When run, this crawler will begin to crawl Wikipedia, starting with the page https://www.themoviedb.org/movie/5255-the-polar- express. 
    This crawler attempts to get a full list of every movie and TV show that an actor of _The Polar Express_ has had a role in.
    """
    
    name = 'tmdb_spider'
    
    start_urls = ["https://www.themoviedb.org/movie/5255-the-polar-express"]
    
    # Our first parsing method
    def parse(self, response):
        """
        Parsing method that follows from the start url and goes to the full cast. Yields the follow command to follow onto the full cast page and callback the parse_full_credits parsing method.
        
            Parameters:
                self: the spider class
                response: the page that was crawled
            Yields:
                Follow the link and callback parse_full_credits
        """
        
        # Follow the link to the cast and callback parse_full_credits parsing method
        yield response.follow("/movie/5255-the-polar-express/cast", callback = self.parse_full_credits)
        
    def parse_full_credits(self, response):
        """
        Parsing method that follows from the full cast url and goes into each individual actor's pages. Yields the follow command to follow onto the each of the casts' pages and callback the parse_actor_page parsing method.
        
            Parameters:
                self: the spider class
                response: the page that was crawled
            Yields:
                Follow the link and callback parse_actor_page
        """
        
        # Go into first <section class="panel pad">
        # Go into each <div class="info">
        # getall() <a href="[link here]"> for each actor to get a list of all their links
        crew = response.css("section.panel")[0]
        cast_links = crew.css("div.info a::attr(href)").getall()
        
        # Create an iterable follow_all response object that we can loop through
        iterable = response.follow_all(cast_links, callback = self.parse_actor_page)
        # We can iterate and follow every link in the cast_links
        for item in iterable:
            yield item
        
    def parse_actor_page(self, response):
        """
        Parsing method that follows from each of the cast members' individual links. Yields dictionaries with two key-value pairs, one for actor name and one for the movie or TV name.
        
            Parameters:
                self: the spider class
                response: the page that was crawled
            Yields:
                Dict (dictionary): dictionary of actor name and movie or TV name
        """
        
        # Search for cast member's name in the title
        # get() the text
        actor_name = response.css("div.title h2.title a::text").get()
        
        # Search for the table for the movies they participated in
        acted_in_block = response.css("table.card")
        # Further search inside for the individual movie name
        # getall() the movies and in the form of a list
        acted_in_list = response.css("a.tooltip bdi::text").getall()
        
        # Iterate through the list of movies and TV shows that they have acted in, put them in the dictionary
        for movie_or_TV_name in acted_in_list:
            # Create the dictionary with the two key-value pairs
            Dict = {"actor": actor_name, "movie_or_TV_name" : movie_or_TV_name} 
            yield Dict
        