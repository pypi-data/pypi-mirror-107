# sanstem
Sanstem is a tool used for **stemming** Sanskrit Verbs and Nouns. Stemming is a pre-processing procedure applied for many NLP algorithms by which the suffix of a word is removed to obtain its stem/root form. This tool is built using a simple rule-based approach. 

### Installation
`pip install sanstem`

------------


### Usage
    from sanstem import SanskritStemmer
	
	#create a SanskritStemmer object
	stemmer = SanskritStemmer()

##### Stemming a Noun
    inflected_noun = ' गजेन ' 
    stemmed_noun = stemmer.noun_stem(inflected_noun)
    print(stemmed_noun)
	# output : गज्

##### Stemming a Verb
    inflected_verb = ' गच्छामि '
    stemmed_verb = stemmer.verb_stem(inflected_verb)
    print(stemmed_verb)
	# output : गच्छ्

Please note to only enter a **single word** in  **Devanagari**  text as input to the functions `verb_stem()` and `noun_stem()`.

------------


### Contribute
- Currently the tool can stem only Sansrkrit Verbs and Noun. It can be extend to more parts of speech like adjective, adverb etc.
- The tool can be made flexible to accept Sanskrit input in any convention like IAST, HK, iTrans etc.
- Instead of stemming just a single word, it can be made capable of stemming a sentence or even a whole file.

------------


### Issue
Please [open an issue ](https://github.com/sooraj-nair/sanstem/issues "open an issue ")here in case any bug was encountered. 
Mail id : nairsooraj2000@gmail.com
