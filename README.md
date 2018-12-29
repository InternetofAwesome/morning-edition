# NPR Morning Edition Podcast Feed Creator  

I wanted a way that didn't depend on legacy API keys to get my morning podcast feed.  
This tool creates a a feed from scraping NPR's website to create the feed. It's a bit limited, in that it does not go back in time farther than the NPR archive page for ME, but it fulfills my needs.  
_This is intended for personal use. It's not a performant implementation, and will probably run up you AWS bill if you hand out the URL and/or don't enable a pretty low throttling rate. This may be an issue for me, even_  
  
## Details  
I created this to be run as an AWS lambda function, which can be used via API gateway. There are scripts in the repo that are designed to be used with the AWS CLI to update the lambda function.  
You will need to have the AWS CLI installed for most of these to work. If you're running Windows, you're already doing it wrong.  
  
`update.sh` - Update your lambda function. This create a `.zip` file with the dependencies required for the script to run, and upload the package to AWS Lambda. _This may not work if you're running something other than 64-bit Linux._  
`run.sh` - Run the lambda function  
`run.py` - Test the script locally  
`function.py` - The heavy lifting. This does the work to scrape NPR's site and creating the feed  

## AWS Config Details
I'll caveat this by saying, I'm by no means an AWS expert. Here's what I did:  
1. Create the lambda function, and call it `morning-edition`. Make sure it's in the default region configured when you did `aws configure`. Configure this as a `GET` event.    
1. This is a long-ish running function. Increase your Lambda timeout to ~10 seconds. For my use case, which is personal, this is fine. 
1. Create an API gateway function that uses your lambda, and make sure it uses the `GET` method.
1. Make a mapping template in API gateway for `application/rss+xml`. Delete the others.  
1. Paste the following into the mapping template, otherwise your API will return the XML enclosed in text, which will break things: `$input.path('$')`  
1. For the Integration Request portion of API gateway, point it to your Lambda function. In my case, `morning-edition`  
  
That's probably it... If you have issues, feel free to ask questions, or contribute.
