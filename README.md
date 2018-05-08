# set_cards

This is a fun little project that I was hoping to put together for some time. My Girfriend likes to play Set (https://www.setgame.com/set) which I think is a fantastic card game. I like the game too the problem is I kinda suck at it :-) and if I lose I do not like it that much anymore. I was hoping to beat her using technology if I cannot do it using my brain.

I attempted an implementation in Mathematica some time ago using some classical vision techniques like image similarity etc. That did not pan out that well. The classifier had a lots of issues you would expect. Different lighting, orientation of the cards etc.

Last year I played with the latest and greatest in DNN and I was amazed how well it works. Now I finally got around to implement a piece of it.

## Limitations

### Software
As this was started/done as part of Udacity Nanodegree it relies on their workspace. I have to figure out how to install all the software so this could be easily replicated outside of that environment.

### Features
Currently this does not solve the whole game. I limited the features to only shape and count. The color and fills are not implemented. I will add them once I get around to collecting the data.

### Input
Currently this does not work that you take a picture of dealt cards and it just does its things. You have to feed it card by card. Something I would like to improve in the future as well.

## Data

I collected around 600 images and they are available for you to experiment. You can download from here

	wget 

The data directory looks like this

	.
	├── card_photos_by_count
	│   ├── one
	│   ├── three
	│   └── two
	├── card_photos_by_shape
	│   ├── diamond
	│   ├── oval
	│   └── s_shape
	├── card_validation_udacity
	│   ├── diamond_shape
	│   ├── one_count
	│   ├── oval_shape
	│   ├── s_shape
	│   ├── three_count
	│   └── two_count
	├── models
	│   ├── 20180507-051118-42b3_epoch_60.0.tar.gz
	│   └── 20180507-052946-5804_epoch_60.0.tar.gz
	├── set_validation
	│   ├── set_1
	│   └── set_2
	└── utils
	    ├── IMG_1051.jpg
	    ├── card_1.jpg
	    ├── card_2.jpg
	    ├── results_count
	    └── results_shape


card_photos_by_count and card_photos_by_count are the directories used to train/test the DNN.

Models are saved trained models that could be used for deployment.

card_validation_udacity contains picture used for validation there is around 100 images I used for validating. They are kept separate so we can make sure the network does not see them during training and it represents the real world out there.


## Training

You are more than welcome to use the data and train with them as you wish. I did the training using outstanding tool from Nvidia called Digits that simplifies the training process singificantly. There is 


## Evaluation

The repo contains 2 scripts for easy evaluation.
One is to estimate how quickly a DNN can respond to a query.

	./eval_speed

The second is to run the validation set through the networks to ascertain accuracy.

	./eval_accuracy
	./eval_shape

Since both networks are independent the accuracy of the whole system is expected to be

	accuracy_of_shape_dn * accuracy_of_count_dn

## Solving sets

I addded a simple python program that contains couple of function that could be used to solve a set.

	import set_cards
	
	cards = [
		{'count': 'three', 'shape': 'oval'},
		{'count': 'three', 'shape': 'diamond'},
		{'count': 'three', 'shape': 's shape'},
		{'count': 'two', 'shape': 'diamond'},
		{'count': 'one', 'shape': 'diamond'}
		{'count': 'two', 'shape': 's shape'}
	]

You can solve it like this

    for found_set in find_sets(cards, ["count", "shape"]):
         print "Set was found %s" % str(found_set)

The program actually does not care what your properties are or what the values are. You have to specify the properties and it checks the sameness or differences in values. So you need to make sure the cards dealt are valid (the rules state there should be 12 etc). This is done so I could easily extend to additional properties.

### Solving from images

There are 2 sample directories with cards from validation set.

	├── set_validation
	│   ├── set_1
	│   └── set_2

You can run them like this

	python eval_set.py set_validation/set_1 job_spec.json

As input it takes a directory with images. the job_spec.json is a simple json like this. This is still a bit shaky. It depends on having the models trained in Digits so the job_spec contains the information what job_id is used to get estimation of prop (I have to figure out how to call the network directly). job_spec.json can look like this.

	[
		["20180508-055305-53fc", "shape"],
		["20180508-051345-7660", "count"]
	]

After a bit of crunching (see below) it should spit out something like

	Set was found ({'count': u'three', 'shape': u'oval'}, {'count': u'one', 'shape': u'diamond'}, {'count': u'two', 'shape': u's shape'})

I have to figure out a better way to do it. The network is Caffe network so I should be able to call it directly. What needs to be done is to reshape the images into format that is eaten by the network. It uses GoogLeNet under the hood and eats 256x256 greyscale pngs.

