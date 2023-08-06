# ParallelSoup
A library that utilizes BeautifulSoup to provide multi threaded scrapping, reducing the total time involved in the scrapping process

<br />

## Aim
The library should implement the following affectively: (this list can be extended in future):
* Parallelization (I mean duh, you didn't see the repo name or what...)
* Should consider the fact that user already has serial BeautifulSoup code
* Adding to above point: should be easier for user too just use our library
* All parts of the library should be documented
* All parts of the library should have unit tests written for verification of their functionality
* Showcase written examples for different sorts of scrapping

<br />

## Example
A small example of scraping imdb with ParallelSoup with goodness of 8 threads
```py
from parallelsoup import ParallelSoup

urls = []
for i in range(0, 10):
    urls.append("https://www.imdb.com/search/title/?countries=in&adult=include&start=" + str(50*i + 1) + "&ref_=adv_nxt")

def extractor(soup):
    data = []
    for item in soup.findAll('div', attrs={'class':'lister-item mode-advanced'}):
        title = item.find('div', attrs={'class':'lister-item-content'}).h3.a
        if title != None:
            data.append(title.text)
    return data

ps = ParallelSoup(8, urls, extractor)
ps.start()
dataParallel = ps.get()
print(dataParallel)
```

## Issues
This library is still in development, for reporting any bugs or suggestions please open a new issue [here](https://github.com/sarthakpranesh/ParallelSoup/issues)
