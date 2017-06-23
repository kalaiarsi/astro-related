from __future__ import print_function
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from re import sub
from time import sleep
from math import sqrt,ceil
from textwrap import wrap
from feedparser import parse


    
def getdata(search='',field='all', start=0, numresults=50):
    """
    Function: uses Arxiv API to retrive data.
    Input:
        search - 'keyword' to search for
        field - as per Arxiv(Note: Arxiv API: ti-title, abs-abstract,cat-subject 
                             category,id-for id number, all-all)
        start - first index of the data batch to be downloaded
        numresults - number of query items to be returned
    Output:
        Validates if the http request was a success (200).
        Returns the 'results' dictionary containing the retrieved data.
    """
    arxiv_url='http://export.arxiv.org/api/'
    full_url=arxiv_url + 'query?search_query='+field+':' + quote_plus(search) + '&start=' + str(start) + '&max_results=' + str(numresults) +'&sortBy=lastUpdatedDate&sortOrder=ascending'
    results = parse(full_url)
    if results.get('status') != 200:
        raise Exception("HTTP error")
    else:
        results = results['entries']
    return results

def wordcloud_arxiv(wordlist,string,saveplot):
    """
    Function:
        Uses wordcloud library to obtain wordcloud of the text 
        (obtained from arxiv and preprocessed)
    Input:
        wordlist - list of all words retrieved from the http request
        string - keyword that was searched for. 
            if keyword is not mentioned, this would refer to the category
        saveplot - boolean status. True: means save to local file.
    Output:
        Returns generated 'wordcloud'
    """
    wordcloud = WordCloud().generate(wordlist)
    if saveplot:
        return(wordcloud)
    else:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        plt.title(string)
    return(wordcloud) 
    
def edit_word_list(wordlist,string):
    """
    Function: Removes the 'keyword' from generated wordlist 
        (as it will occur in all output titles ;) )
    Input:
        wordlist - list of all words retrieved from the http request
        string - keyword that was searched for. 
            if keyword is not mentioned, this would refer to the category
    Output:
        Returns wordlisttext - {keyword,keyword+'s'}     
            ex: keyword="exoplanet". output=wordcloud without :{Exoplanet,Exoplanets}
        All words except keyword are converted to single text content and returned.
    """
    wordlist=filter(None,wordlist)
    wordlist=[word.capitalize() for word in wordlist]
    wordlist=list(filter(lambda word: word != string.capitalize(), wordlist))
    string=string+"s"   
    wordlist=list(filter(lambda word: word != string.capitalize(), wordlist))
    wordlisttext=' '.join(wordlist)   
    return(wordlisttext)

def arxiv_to_wordcloud(results,string,saveplot=False):
    """
    Function: results from arxiv are converted to wordcloud with tags 
        (aka batchnames - updated date of the articles)
    Input:
        results - from http request to arxiv
        string - keyword searched for
        saveplot - boolean value. True => save final plot as a local file.
    Output:
        wowordcloudrdcloud - list of all words found in all titles in the current batch
        tag - titles for each batch. 
            (in format: uploaded date of first article in the batch "to" 
            uploaded date of last article in the batch.)
    """
    if not saveplot:
        tag="Period of entries: "+results[0]["updated"].split('T')[0]+" to "+results[len(results)-1]["updated"].split('T')[0]
        print(tag)
    tag=results[0]["updated"].split('T')[0]+" to "+results[len(results)-1]["updated"].split('T')[0]
    wordlist=[]
    for result in results:
        result_title=result["title"].strip().split(' ')
        for words in result_title:
            words=sub(r'\W+', '', words.strip())
            wordlist.append(words)
    wordcloud=wordcloud_arxiv(edit_word_list(wordlist,string),string,saveplot)
    return(wordcloud,tag)
    
def multiple_arxiv_wordcloud_category(search,field,maxhits,blockcount,saveplot=False,numresults=50):
    """
    Function: loops through multiple batches of wordclouds 
        to find how the wordclouds evolve over timeframe
    Input:
        search - search for which 'keyword'
        field - to be given as 'ti' for title
        maxhits - index of first data to be retrived. 
            (make sure there are enough articles)
        blockcount - batch size for each phase. forms individual wordclouds batches
            for ex: 500. [1,500],[501-1000],[1001-1501] etc 
        saveplot - boolean value. True => save final plot as a local file.
        numresults - number of query items to be returned
    Output:
        Multiple plots showing wordcloud for each batch of titles referred.
    """
    wordcloudlist=[]
    tags=[]
    batchnumber=1
    for period in range(0,maxhits,blockcount):
        results=getdata(search,field,period,numresults)
        if not results:
            print("http request failed")
        wordcloud,tag=arxiv_to_wordcloud(results,search,saveplot)
        if saveplot:
            wordcloudlist.append(wordcloud)
            tags.append(tag)
            print("Adding wordlist for batchnumber:"+str(batchnumber))
            batchnumber+=1
        sleep(5) # min 3 seconds
    if saveplot:
#        title="Wordcloud for search term:"+search+" and field set to:"+field+"\n"
        plot_wordclouds(wordcloudlist,tags,search)

def single_entry(search,field,numresults):
    """
    Function: Generate wordcloud for single batch of keyword search
    Input:
        search - 'keyword' to be serched for
        field - 'ti' or 'cat' . title or category to be searched for, 
            to match the 'search' term
        numresults - number of query items to be returned
    Output:
        Plot showing wordcloud for this search result
    """
    results=getdata(search,field,0,numresults)
    wordcloud,tag=arxiv_to_wordcloud(results,search,True)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    
    
def plot_evolution(search,field,maxhits,blockcount):
    """
    Function: loops through multiple batches of wordclouds to find 
        how the articles in particular 'category' evolve over timeframe
    Input:
        search - search for which 'keyword'
        field - to be given as 'cat' for category
        maxhits - index of first data to be retrived. 
            (make sure there are enough articles)
        blockcount - batch size for each phase. forms individual wordclouds batches
            for ex: 500. [1,500],[501-1000],[1001-1501] etc 
    Output:
        Multiple plots showing wordcloud for each batch of category articles referred.
    """
    multiple_arxiv_wordcloud_category(search,field,maxhits,blockcount,True)
    

def plot_wordclouds(wordcloudlist,tags,search):
    """
    Function: Plots single plot containing wordcloud for multiple batches as subplots. 
    Automatically adjusts number of rows and columns 
        for subplots in plot (according to number batches)
    Input:
        wordcloudlist - list of all generated wordclouds
        tags - titles for subplots (batchnames: Period)
        search - 'keyword' searched for. 
            used as filename to save plot (search.png)
    Output:
        Plot containing batchwise wordclouds as subplots. 
        Save generated plot as a PNG file locally
    """
    count=len(wordcloudlist)
    y=ceil(sqrt(count))
    x=ceil(count/y)
    fig=plt.figure()    
    for cloud,index in zip(wordcloudlist,range(len(wordcloudlist))):
        ax=fig.add_subplot(x,y,index+1)
        ax.imshow(cloud, interpolation='bilinear')
        ax.set_title("\n".join(wrap(tags[index],14)),fontsize=8)
        plt.axis("off")
    plt.suptitle("Evolution of keyword:"+search,fontsize=12)
    plt.show()
    fig.savefig((search+'.png'), dpi=100)
    