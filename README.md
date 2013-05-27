lido-temp
=========

This is a web app that charts the water temperature at Brockwell Lido.

It was done on Bank Holiday Monday, 27-May-2013, out of personal interest. I try
to swim as often as I can, temperature is a factor. I rely on the @brockwelllido
tweets to poke me into action in the morning. I have a personal threshold of 14C
(57.2F), below which I would wear a wetsuit - and which therefore involves a bit
more hassle and preparation.

The chart shows each day's recording from @brockwelllido, which I believe comes
from Fusion (who run the pool). There are missing dates, which seem to be Fusion
-related.

Technical
---------

The app itself is a Flask app, hosted on Heroku.

It uses Google Charts, and I upload the data manually, only because I couldn't
be bothered to store the data anywhere, or add a form to upload it.

There is no CSS applied - it's just pure HTML, so will look different in different
browsers.

There is no support for IE, as it uses SVG and is, apparently not supported natively.

I have no intention of fixing any of the above - if you do, please feel free to
contribute.

Contributing
------------

If you wish to contribute, please do so in the normal manner:

* Create an issue in Github against this repo, clearly describing the work you are about to do
* Fork this repo into your own account
* Create a new branch for your work off master
* Make your changes to this branch and push to your repo
* Issue a Pull Request against this repo
* I'll do the merge, and redeploy.

Please write comprehensive commit messages - be as verbose as you like.

