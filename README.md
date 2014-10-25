Jobful
======

a crawler of job opportunities. How to run:

Requirements:
  - mongo and Solr

Features:
1. Crawl job positions:
  - scrapy crawl <spider>    # ex. scrapy crawl wm-jobs

2. Start Solr:
  - solr <absolut path to jobful/jobful/solr>

3. Index job positions:
  - python solr_indexer.py
