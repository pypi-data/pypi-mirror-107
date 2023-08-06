
![PyPI - Wheel](https://img.shields.io/pypi/wheel/UrbanDictApi?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/UrbanDictApi?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/TanmayArya-1p/UrbanDictApi?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/tanmayarya-1p/urbandictapi?style=for-the-badge)



## `pip install urbandictapi`




### Definitions :
* <a href="#worddefinitionwordstr--meaningstr--examplestr--authoruser--timestampstr">WordDefinition</a>
* <a href="#usernamestr--hrefstr">User</a>
### Functions :
* <a href="#querydefinitionsqstr--singlefalse">Query.definitions</a>
* <a href="#getuserdefinitionsuuser">GetUserDefinitions</a>
* <a href="#getuserdefinitionsuuser">CategoryDefinitions</a>
* <a href="#wordoftheday">WordofTheDay</a>

# Import
```py
from UrbanDictAPI.main import Query ,WordofTheDay , CategoryDefinitions , GetUserDefinitions
```
# Definitions
* ###  `WordDefinition(word:str , meaning:str , example:str , author:User , timestamp:str)`

    ### Attributes 
    * `word`
    * `meaning` - meaning of word.
    * `example` - example for the usage of the word.
    * `author` - <a href="#usernamestr--hrefstr">User</a> object
    * `timestamp` - Time of publishing of definition.
    * `data` - Includes further information. (eg: Likes and Dislikes)
***
* ### `User(name:str , href:str)`
    ### Attributes
    * `name` - Name of User.
    * `href` - href to User profile.
    * `data` - Includes further information about User.


# Functions

* ### `Query.definitions(q:str , single=False)`
    ### 
    Query words by `q`.
    ### 
    Returns a list of <a href="#worddefinitionwordstr--meaningstr--examplestr--authoruser--timestampstr">WordDefinition</a> objects if `single=False`.
    If `single=True` then a single <a href="#worddefinitionwordstr--meaningstr--examplestr--authoruser--timestampstr">WordDefinition</a> object will be returned(Top Result).
    ###
    Big O of single=True < Big O of single=False
***
* ### `GetUserDefinitions(u:User)`
    ###
    Get a list of <a href="#worddefinitionwordstr--meaningstr--examplestr--authoruser--timestampstr">WordDefinition</a> objects of all the definitions published by a user in their lifetime.
***
* ### `CategoryDefinitions(cat:str)`
    ###

    <details>
    <summary>There are 8 Categories to choose form</summary>
    <ul>
    <li>College</li>
    <li>Food</li>
    <li>Internet</li>
    <li>Music</li>
    <li>Name</li>
    <li>Relegion</li>
    <li>Sports</li>
    <li>Work</li>
    </ul>
    </details>

    Returns a list of most popular <a href="#worddefinitionwordstr--meaningstr--examplestr--authoruser--timestampstr">WordDefinition</a> objects from that category.

***
* ### `WordofTheDay()`
    ###
    Returns a dict of <a href="#worddefinitionwordstr--meaningstr--examplestr--authoruser--timestampstr">WordDefinition</a> objects of the days.
    <details>
    <summary>Example Output</summary>
    <code>
    {'May 28 Word of the Day': WordDefinition(word="elder goth" , meaning="A goth who has been part of the subculture since 
    it originally came about, or a goth over the age of 40." , example="Eriks dad is an Elder goth" , author=User(name="Solinium" , href="https://www.urbandictionary.com/author.php?author=Solinium" , data={}) , timestamp="by Solinium May 30, 2008" , data={'upvotes': 85, 'downvotes': 8}), 'May 27 Word of the Day': WordDefinition(word="danger wank" , meaning="The 
    act of extreme masturbation. You must "knock one out" whilst in close proximity to any of the following; Your mum, a nun, your boss, a member of parliament, George Michael. A person with capabilities to act upon catching you mid self-abuse 
    obvisouly ups the ante. Ejaculation must be reached before your danger wank target comes (no pun intended) to investigate.  The higher the chances of being discovered with one's pants down, pulling one's war face is obviously where the danger comes from. The more danger involved the harder (or softer) it is to complete the task in hand (snigger). The more dangerous the better. The chance of being arrested, pummeled by an angry father or having your hand severed by an arab's sabre means that you are a pro "Danger wanker."" , example=""I was in my bedroom and i shouted downstairs, "Mum there's call the police there's a madman with a set of steak knives hacking me to pieces!" As soon as I heard her scream, I dropped my trousers and commenced the danger wank. As I heard her stomp up the stairs I knew i had to be quick so i upped the pace, i heard her stumble on the top step, which bought me some time. Unfortunately for me I timed my finish badly. As 
    my mum barged through the door armed with a rollign pin I chugged all over her. I spent the evening in A&E with concusion.  Now thats what i call extreme DW"" , author=User(name="johnnynika" , href="https://www.urbandictionary.com/author.php?author=johnnynika" , data={}) , timestamp="by johnnynika May 30, 2006" , data={'upvotes': 2295, 'downvotes': 359}), 'May 26 Word of the Day': WordDefinition(word="bi wife energy" , meaning=""Bi wife energy" is a term that was coined through a song by the user @/cringelizard on Tik Tok to describe the energy that Misha Collins radiates, explaining it with the fact that he is married to a bisexual woman, Victoria Vantoch. The full song can be found on all music streaming services and YouTube.People with bi wife energy are fiercely supportive of the LGBTQ+ community, their love for their spouse, if they have one, is strong and people sometimes assume they are queer.In their first video about this, @/cringelizard referred to Misha as a "hetero guy", but amended in a later added verse that the actor does not like labels.The term "bi wife energy" can be used for people of all genders, regardless of relationship status, although "bi husband energy" haHe has bi wife energy" , example=""You know Misha Collins?" "You're talking about that actor, right? The one that radiates bi wife energy?""Amy Santiago has so much bi wife (bi husband) energy!"" , author=User(name="notoriouswriter" , href="https://www.urbandictionary.com/author.php?author=notoriouswriter" , data={}) , timestamp="by notoriouswriter March 21, 2021" , data={'upvotes': 487, 'downvotes': 1154}), 'May 25 Word of the Day': WordDefinition(word="bad" , meaning="someone who is sexy beyond mean" , example="dam she hella bad." , author=User(name="NiSHA..hit ma aim" , href="https://www.urbandictionary.com/author.php?author=NiSHA..hit%20ma%20aim" , data={}) , timestamp="by NiSHA..hit ma aim November 14, 2009" , data={'upvotes': 2837, 'downvotes': 803}), 'May 24 Word of the Day': WordDefinition(word="geriatrocity" , meaning="The horror and shame of getting old; especially when approaching the age of gray hair and arthritis." , example="Yo dude, Darryl is turning 40 next year.  That's what I call geriatrocity." , author=User(name="shrimphead" , href="https://www.urbandictionary.com/author.php?author=shrimphead" , data={}) , timestamp="by shrimphead February 28, 2009" , data={'upvotes': 1170, 'downvotes': 484}), 'May 23 Word of the Day': WordDefinition(word="Sussy Baka" , meaning="A spicy way to insult your degenerate friends.“Sussy” and “sus” are words used in the videogame Among Us to describe someone shifty or suspicious.Baka roughly translates to idiot in Japanese and is a common phrase expressed by tsundere characters in anime/manga.Originally coined to insult A2B2 user TSUNDEREBOY, the meme spread from discord to TikTok and propagated in the following days." , example="Sussy Baka over here be selling merch on his OnlyFans." , author=User(name="theanimeman69" , href="https://www.urbandictionary.com/author.php?author=theanimeman69" , data={}) , timestamp="by theanimeman69 May 12, 2021" , data={'upvotes': 1900, 'downvotes': 586}), 'May 22 Word of the Day': WordDefinition(word="cultural reset" , meaning="A moment that is generally agreed to have had a significant influence on pop culture and everyday life. While the term was coined by Rose McGowan in context of the #MeToo movement, and is mostly associated with the K-pop community, the phenomenon is universal and a basic component of how culture works.Real world events such as social/political movements, 
    the election of a new U.S. President, major catastrophes and disasters, as well as entertainment such as movies, music and TV, can all function as cultural resets. Notable cultural resets in relatively recent memory include:* The Beatles ap* The COVID-19 pandemic" , example=""The Nineties politically started with the fall of the Berlin Wall on November 9, 1989 and the Soviet Union dissolving on December 26, 1991, and ended with both the 2000 Presidential election which saw the victory of George W. Bush and the terrorist attacks on September 11, 2001 which left people so stupefied that it functioned as something of a cultural reset button." - TV Tropes' article on the 1990s" , author=User(name="Spike from Degrassi" , href="https://www.urbandictionary.com/author.php?author=Spike%20from%20Degrassi" , data={}) , timestamp="by Spike 
    from Degrassi February 09, 2021" , data={'upvotes': 1193, 'downvotes': 516})}
    </code>
    </details>
***
