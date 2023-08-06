""" This module, namely 'SanskritStemmer'  is used to strip off the suffixes of a sanskrit verb.

    It uses a list of suffixes to check whether the input word endswith any of the suffixes in the list.

     Class
     _ _ _ _ _ _ _
     Sanskrit_Stemmer : This class two main functions -
                                                        1. verb_stem() which stems the input sanskrit verb
                                                        2. noun_stem() which stems the input sanskrit noun
"""

import csv
from devatrans import DevaTrans                                                     # for transliteration and back-transliteration
import re                                                                           # for pattern matching
from polyglot.detect import Detector                                                # for detecting entered text's language
from polyglot.detect.base import logger as polyglot_logger                          # polyglot logger
polyglot_logger.setLevel("ERROR")                                                   # to ignore warnings from polyglot
from sanstem.InputLanguageError import InputLanguageError
import os

class SanskritStemmer:
    """The Sanskrit_Stemmer class can be used for stemming sanskrit verbs as well as nouns

        Attributes
        _ _ _ _ _ _ _ _

        vowels : list
            a list of all vowels in both cases for preventing heavy over-stemming

        dt : DevaTrans object
            for transliterating the input Devanagari word to English letter. The Harvard-Kyoto convention is used here.

        suffix_list : list
            a list of suffixes in sanskrit for checking whether the input word contains any of the suffixes in the list.

        devanagari_list : list
            a list of languages in Devanagari script, to ensure that the input is a Sanskrit word.

        Methods
        _ _ _ _ _ _ _ _

        is_devanagari_text(word):
            used to check if the input language is Devanagari or not. Will not use this for noun stemming since proper nouns may not be detected by the polyglot package

        transliterate_devanagari_to_hk(word):
            transliterate input word in Devanagari to Harvard-Kyoto convention

        back_transliterate_hk_to_devanagari(word):
            back-transliterate input word in Harvard-Kyoto convention to Devanagari text.

        verb_stem(sanskrit_verb)
            stems the given sanskrit input verb and returns the stemmed word.

        remove_last_vowel (stemmed_word)
            it removes any of the vowel letter if remaining at end of the stemmed word. This is done to map more inflections into a single stem

    """
    def __init__(self):
        self.vowels = ['a','e','i','o','u','A','E','I','O','U']     # for reducing over-stemming
        self.dt = DevaTrans()                                       # devatrans object

        dirname = os.path.dirname(__file__)
        verb_suffix_file = open(os.path.join(dirname, 'Data','verb_suffixes.csv'), 'r', encoding='utf8')
        noun_suffix_file = open(os.path.join(dirname, 'Data','noun_suffixes.csv'), 'r', encoding='utf8')
        devanagari_file =  open(os.path.join(dirname, 'Data','devanagari_languages.csv'), 'r', encoding='utf8')

        self.verb_suffix_list = []
        self.devanagari_language_list = []
        self.noun_suffix_list = []

        csv_reader1 = csv.reader(verb_suffix_file)
        csv_reader2 = csv.reader(noun_suffix_file)
        csv_reader3 = csv.reader(devanagari_file)

        for row in csv_reader1:
            self.verb_suffix_list.append(row[0])

        for row in csv_reader2:
            self.noun_suffix_list.append(row[0])

        for row in csv_reader3:
            self.devanagari_language_list.append(row[0])

    def is_devanagari_text(self,word):
        detector = Detector(word)
        return True if detector.language.name in self.devanagari_language_list else False                      # validating input language

    def transliterate_devanagari_to_hk(self,word):
        word = re.sub('।|०|१|२|३|४|५|६|७|८|९|', '', word)
        return self.dt.transliterate(input_type = "sen", to_convention = "hk", sentence = word)  # transliterating the input word

    def back_transliterate_hk_to_devanagari(self,word):
        return self.dt.back_transliterate(input_type="sen", from_convention="hk", sentence=word)                 # back-transliterating to sanskrit

    def remove_last_vowel(self,word):
        return re.sub('a$|e$|i$|o$|u$|A$|E$|I$|O$|U$','',word)

    def verb_stem(self, sanskrit_verb):
        """This method is used to stem the input sanskrit verb and return the stemmed output

               Parameters
               _ _ _ _ _ _ _ _
               sanskrit_verb : str
                    this word is stemmed by the function to obtain the output

               Returns
               _ _ _ _ _ _ _
                back_trans : str
                    the stemmed output of the sanskrit verb

        """

        sanskrit_verb = sanskrit_verb.strip()
        trans_stemmed = ''
        stemming_success = False                                                            # initial state of the stemming operation

        if not self.is_devanagari_text(sanskrit_verb):
            raise InputLanguageError('Please check if the input is a Devanagari string')    # raise erorr if the input language is not in Devanagari Text
        else:
            trans = self.transliterate_devanagari_to_hk(sanskrit_verb)                      # transliterating the input word
            for i in self.verb_suffix_list:                                                      # iterating through suffix list
                if trans.endswith(i):                                                       # checking if suffix is matched
                    temp = trans[0:len(trans)-len(i)]                                       # removing the suffix
                    if (len(temp)<=2 and any(letter in temp for letter in self.vowels)) or len(temp)>2:                                 # preventing a heavy overstemming
                        trans_stemmed = temp                                                # storing the result
                        stemming_success = True                                             # setting the flag as true to prevent looping further
                        break                                                               # getting out of the inner loop

            if stemming_success:
                trans_stemmed = self.remove_last_vowel(trans_stemmed)
                trans_stemmed = re.sub('iSy$|iSya$|iSye$|isyA$', '', trans_stemmed)
                back_trans = self.back_transliterate_hk_to_devanagari(trans_stemmed)        # back-transliterating to sanskrit
            else:
                back_trans =  sanskrit_verb                                                 # return the same word in case it was not stemmed

        return back_trans

    def noun_stem(self, sanskrit_noun):
        """This method is used to stem the input sanskrit noun and return the stemmed output

               Parameters
               _ _ _ _ _ _ _ _
               sanskrit_noun : str
                    this word is stemmed by the function to obtain the output

               Returns
               _ _ _ _ _ _ _
                back_trans : str
                    the stemmed output of the sanskrit noun

        """
        sanskrit_noun = sanskrit_noun.strip()
        trans_stemmed = ''
        stemming_success = False                                                        # initial state of the stemming operation

        trans = self.transliterate_devanagari_to_hk(sanskrit_noun)                      # transliterating the input word
        for i in self.noun_suffix_list:                                                 # iterating through suffix list
            if trans.endswith(i):                                                       # checking if suffix is matched
                temp = trans[0:len(trans)-len(i)]                                       # removing the suffix
                if (len(temp)<=2 and any(letter in temp for letter in self.vowels)) or len(temp)>2:                                 # preventing a heavy overstemming
                    trans_stemmed = temp                                                # storing the result
                    stemming_success = True                                             # setting the flag as true to prevent looping further
                    break                                                               # getting out of the inner loop

        if stemming_success:
            trans_stemmed = self.remove_last_vowel(trans_stemmed)
            trans_stemmed = re.sub('iSy$|iSya$|iSye$|isyA$', '', trans_stemmed)
            back_trans = self.back_transliterate_hk_to_devanagari(trans_stemmed)        # back-transliterating to sanskrit
        else:
            back_trans = sanskrit_noun                                                  # return the same word in case it was not stemmed
        return back_trans

