#!/usr/bin/env python
"""
Example code showing wordclouds extraction from Arxiv papers
============================================================
- Runs on python3.
- requirements: quote_plus(from url_lib or urllib.parse), wordcloud, matplotlib,re,time,math,textwrap,feedparser
Note: Arxiv API: ti-title, abs-abstract,cat-subject category,id-for id number, all-all   are the possible search fields.
"""

import extractarxiv


def single_topic(search_string,numresults):
    """
    This function prints wordcloud image for a single 'search keyword' evolution. Ex: 'exoplanet'
    Inputs:
        search - search for which 'term'
        field - to be given as  (as thats the field that interests us :P)
        maxhits - index of first data to be retrived. (make sure there are enough articles)
        blockcount - batch size for each phase. for ex: 500. [1,500],[501-1000],[1001-1501] etc forms individual wordclouds
        numresults - number of query items to be returned

    Output:
        Displays a single wordcloud image. not saved on local file.
    """
    extractarxiv.single_entry(search_string,'all',numresults)
    
    
def research_field_evolution(search,field,maxhits,blockcount,numresults):
    """
    This function prints multiple wordcloud images for a 'category' evolution split into batches (batchsize = blockcount)
    Inputs:
        search - search for which 'keyword'
        field - to be given as 'cat' for category or 'ti' for title
        maxhits - index of first data to be retrived. (make sure there are enough articles)
        blockcount - batch size for each phase. for ex: 500. [1,500],[501-1000],[1001-1501] etc forms individual wordclouds
        numresults - number of query items to be returned
    Output:
        Displays indiviudal wordcloud images for each batch (i.e. blockcount). not saved on local file.
    """
    extractarxiv.multiple_arxiv_wordcloud_category(search,field,maxhits,blockcount)
    


def research_field_evolution_subplots(search,field,maxhits,blockcount,numresults):
    """
    This function prints single plot containing subplots of wordcloud images for a 'search keyword' evolution. Ex: 'exoplanets'. 
    Also, function automatically chooses number of rows and columns for subplots, based on number of batches processed.
    i.e: 5 batches=> 2rowsx3cols 5subplots   14 batches=> 4rowsx4cols 14 subplots
    Inputs:
        search - search for which 'keyword'
        field - to be given as 'ti' (as we are interested in 'how the number of article titles containing the specific keyword has evolved)
        maxhits - index of first data to be retrived. (make sure there are enough articles)
        blockcount - batch size for each phase. for ex: 500. [1,500],[501-1000],[1001-1501] etc forms individual wordclouds
        numresults - number of query items to be returned
    Output:
        Displays a single plot file containing subplots of wordcloud image for each batch. also saved as '.png' file locally.
    """
    extractarxiv.plot_evolution(search,field,maxhits,blockcount)

    
def Main():
    numresults=50 # number of articles per batch
    
    """
    search for articles containing keyword="exoplanet" and plot word cloud of the accumulated titles.
    """
    search_string="exoplanet"
    print("plot - single search for: \""+search_string+"\"")
    single_topic(search_string,numresults)    


    """
    search how number of articles with category "astro-ph" have evolved and plot word cloud of the accumulated titles.
    """
    category="astro-ph"# category name
    print("plot - category evolution for: \""+category+"\"")
    research_field_evolution(category,'cat',41000,10000,numresults)


    """
    search for keyword="exoplanet" and see it has evolved over time and plot separate wordcloud plots of the accumulated titles.
    """
    res_topic="exoplanet"    
    print("plot - research topic evolution for: \""+res_topic+"\"")
    research_field_evolution(res_topic,'ti',1000,200,numresults)# has abt 1100 entried till 2016
    
    
    """
    search for keyword="exoplanet" and see it has evolved over time and 
    plot single plot containing wordclouds the accumulated titles batchwise
    Also saves the single final plot as 'keyword.png' locally
    """
    search_string="star"
    print("save figure - research topic evolution (as subplots) for: \""+search_string+"\"")
    research_field_evolution_subplots(search_string,'ti',26000,5000,numresults)    

    
if __name__=="__main__":
    Main()   