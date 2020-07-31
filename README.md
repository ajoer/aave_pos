# POS tagging for African-American Vernacular English

This is part of my Master's thesis in 2015. 

The project aimed at improving Part-of-Speech (PoS) tagging for an under-resourced language version, African-American Vernacular English (AAVE). 
I used unsupervised and weakly (or semi-)supervised machine learning methods to improve the accuracy of an out of the box, state-of-the-art PoS tagger, the Rungsted tagger.

The main issue with the tagging accuracy on AAVE data is that there are many out-of-vocabulary (OOV) words. This is due to the dialect, in which word choices can differ from General American, but it is also due to spelling variations in the dialect. 
Since PoS tagging is conducted on written language only, any variation in spelling has a large impact on the tagging accuracy. 

In order to overcome this issue, I want to add annotated AAVE data to the training data of the PoS tagger model, such that the tagger learns the variations in word choice and spelling, and the number of OOV words decreases. 
However, since AAVE is an under-resourced language version, meaning there are no annorated data resources to give to out model, I have to create these annotated resources.

I want to annotate the data automatically, since I need a lot of it to overcome the data bias of the General American data.
I need two data sources; unlabelled AAVE data and some sort of linguistic information about the OOV words that can help me annotate the unlabelled data.

For unlabelled data I use tweets written in the American southeastern states, subtitles from the TV shows The Wire and Boondocks and hiphop lyrics from African-American rappers. 
I restrict the tweets to this geographical area, since the proportion of AAVE speakers is highest here and I only include tweets that contain at least one AAVE spelled word. See [Jorgensen et al. 2015](https://www.aclweb.org/anthology/W15-4302.pdf) for more on this approach.

For linguistic information, I create tag dictionaries using Urban Dictionary, Wiktionary, Hepster's and a list of African-American names, since these are also under-represented in the General American training data.
I add all words in those resources as keys in my tag dictionaries and add all the parts of speech provided by the resources as a list to each key. 
For instance: the word "kisses" can be either a noun or a verb, so I add both to the tag dictionary for "kisses".   

I annotate the AAVE data using the tag dictionaries, and I experiment with different levels of annotation coarseness and bias weights. 
As an example, since  I don't know whether "kisses" is a verb or a noun in the AAVE sentences, I experiment with adding both of the options and adding a penalty weight of 0.5 to both options. 
I also experiment with only including sentences in the training data where all words are unambiguously annotated. In that case all sentences with the word "kisses" would be excluded.

I experimented with two setups for learning from this automatically annotated data; ambiguous learning and selftraining. Ambiguous learning works best. 

For more information on the project, the results, the data and the code, please see the [paper](https://www.aclweb.org/anthology/N16-1130.pdf), or if you really want a deep dive, here's [my thesis](https://drive.google.com/file/d/0B_4p-RZsBhYzM1EzVndIVklQUDQ/view?usp=sharing).

NB: I've recently started cleaning up the original code and data. For now, only the ambiguous learning scenario is supported. Selftraining and visualization modules will be added shortly.
