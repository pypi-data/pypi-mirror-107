## Lightshield Tools

Tools and Code-Sections of the Lightshield Framework that were better fit to be provided through dependency
rather then included in the main project.



### Ratelimiter (WIP)

Multi-Host async ratelimiting service. The clients each sync via a central redis server. 

#### Usage
```python
    from lightshield.proxy import Proxy
    import aiohttp
    
    async def run():
        p = Proxy()
        # Initiate the redis connector in async context
        await p.init(host='localhost', port=5432)
        
        async with aiohttp.ClientSession(headers={'X-Riot-Token': ''}) as session:
            
            # One-off requests directly through the API object.
            await p.request('https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/SILVER/I', session=session)
            
            # Preselect the Method Ratelimit Zone to skip the selection of corresponding limits
            zone = await p.get_endpoint('https://euw1.api.riotgames.com/lol/league-exp/v4/entries/')
            for page in range(1, 10):
                zone.request('https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/SILVER/I?page=%s' % page, session)
```
