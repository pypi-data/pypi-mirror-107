# SynChron
Synchronicity (German: Synchronizität) is a concept first introduced by analytical psychologist Carl G. Jung "to describe circumstances that appear meaningfully related yet lack a causal connection.Jung held that to ascribe meaning to certain acausal coincidences can be a healthy, even necessary, function of the human mind—principally, by way of bringing important material of the unconscious mind to attention. This further developed into the view that there is a philosophical objectivity or suprasubjectivity to the meaningfulness of such coincidences, as related to the collective unconscious.

Package contains modules for interacting with online media sources. We call them widgets. They can either send or receive data. This will be more applicable in some cases than others.

- update() - function which retrieves a single update in the format of a dict
- get_multiple(count) - function which retrieves multiple updates in the above format. You can usually use the count parameter with update function as well, but keepign this one in for clarity and compatibility.

## rsswidget 
- Use this whenever possible. It's simplest to get an rss feed if one is available. 

## redditwidget
- Get Reddit posts. This requires Reddit API credentials.
- Consider using the RSS widget with address: https://www.reddit.com/r/news.rss - this works. However, it doesn't support all of the Reddit features

## udemywidget
- Specific functionality to get Udemy course links. This uses the same general process as Reddit, but has been taylored to meet the Udemy case.

## newswidget
- Gets links from Google news search

## twitter widget
- Requires Twitter credentials
- 2-way functionality (read and write posts)

## quote widget
- Random quotes
- Proof of concept widget. Use this to validate your use of this library
- Some of the quotes are pretty good.

## utils
- Common functions have been factored out into utils. These include functions for cleaning up links and URLs.

## Version 1.2
- Added a standard function for universal standardization.
  - This supercedes the get_update and get_multiple functions. However, these have been left in-place for compatibility purposes.
  - Use get_posts() for all interactions from now on.
  - get_posts()
    - **params**: 
      - params={} - all required params -- can be empty if none applied -- important for apis that require auth
      - also **kwargs
    - **returns**: [] of objects, including the following minimal fields
      - title: string
      - description: string
      - author: string
      - url: url
      - tweet: string
      - img: img url
      - tags: string