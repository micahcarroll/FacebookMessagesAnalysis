# FacebookMessagesAnalysis
A basic visualization of Facebook Messanger data

## Setup

1. Download a copy of your Facebook data (more info here: https://www.facebook.com/help/131112897028467/?helpref=hc_fnav)
2. Add downloaded Facebook data folder to the directory and rename to `facebook-dump`
3. Open `main.py` in a text editor and modify the variable `MY_NAME` to your name as it appears on Facebook

## Visualizations

The visualizations are created with [ggplot](https://github.com/yhat/ggpy).

To see the visualizations of your data, run `main.py`. This can take various minutes, depending on the amount of messages you have.

At the end of the process, you will have two graphs. The first one - an example of which is below - displays the amount of messages received over time by your most frequent contacts on Facebook Messanger.
![ExampleImage1](http://i.imgur.com/4wZEbD9.png)

The second graph, instead, ranks your most frequent contacts in order of importance depending on how much you messaged each over at each moment of time.
An example is illustrated below.

![ExampleImage2](http://i.imgur.com/uRrRGj6.png)
