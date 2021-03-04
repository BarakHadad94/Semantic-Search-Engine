import gensim
from gensim.models import Word2Vec
from gensim.models import TfidfModel
import xml.etree.ElementTree as ET
import re
import fasttext
import fasttext.util
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
from gensim.corpora import mmcorpus

if __name__ == '__main__':

    # LOAD MODEL OF HEBREW CORPUS
    model = gensim.models.KeyedVectors.load('wordVec')
    print("******** FINISHED LOADING CORPUS *********")

    # OPEN FILES CONTAINING LISTS OF LAWS AND DICTIONARY OF TF-IDF
    with open("main_law_list.txt", "rb") as main_law_file:  # Unpickling
        main_law_list = pickle.load(main_law_file)

    with open("words_val_dict.txt", "rb") as dictionary:  # Unpickling
        tfidf_dict = pickle.load(dictionary)

    # INPUT LOOP UNTIL GETS 'q' OR 'quit'
    # THE STRING TO SEARCH
    search_string = input("Please enter your search ('q' to quit) : ")
    while search_string != "q" and search_string != "quit":
        search_string_to_array = search_string.split()
        j = 0
        list_of_similar_lists = []
        while j < len(search_string_to_array):
            # CREATE MOST SIMILAR LIST FOR EACH WORD THAT WAS SEARCHED
            most_similar = model.most_similar(search_string_to_array[j], [], 30)
            similar_words = []
            # MAKE A LIST WITH ONLY THE WORDS, WITHOUT THE VALUES
            for item in most_similar:
                similar_words.append(item[0])
            # ADD THE ORIGINAL WORD TO THE LIST
            similar_words.append(search_string_to_array[j])
            # REMOVE DUPLICATES FROM similar_words LIST
            similar_words = list(dict.fromkeys(similar_words))
            # ADD THE LIST OF SIMILAR WORDS THE LIST OF ALL LISTS OF SIMILAR WORDS
            list_of_similar_lists.append(similar_words)
            j = j + 1
        # print(list_of_similar_lists)
        # print("###########################")


        # FOR EACH LAW, COUNT THE NUMBER OF TIMES IT HAS A WORD FROM THE SIMILAR WORDS LIST
        # THE LAW WITH THE HIGHEST RESULT WILL BE THE ANSWER
        count_temp_law_equal = 0
        count_first_law_equal = 0
        count_sec_law_equal = 0
        count_third_law_equal = 0
        count_forth_law_equal = 0
        count_fifth_law_equal = 0
        first_result = ""
        law_of_first_result = ""
        sec_result = ""
        law_of_sec_result = ""
        third_result = ""
        law_of_third_result = ""
        fourth_result = ""
        law_of_fourth_result = ""
        fifth_result = ""
        law_of_fifth_result = ""
        for law in main_law_list:
            for section in law:
                # SPLIT THE LAW SECTION STRING INTO AN ARRAY
                array_of_sec = section.split()
                for word_in_law in array_of_sec:
                    # FOR EVERY WORD IN THE LAW, CHECK IF IT'S EQUAL TO A WORD IN THE SIMILAR WORDS LISTS
                    for lst in list_of_similar_lists:
                        for sim_word in lst:
                            if sim_word == word_in_law:
                                # IF EQUAL, ADD THE VALUE OF THE WORD FROM TF-IDF DICT TO THE VALUE COUNTER OF THE SECTION
                                if word_in_law in tfidf_dict.keys():
                                    new_val = tfidf_dict[word_in_law] * 10
                                    new_val = new_val * new_val * new_val
                                    count_temp_law_equal = count_temp_law_equal + new_val
                # IF COUNTER OF THIS LAW IS BIGGER THAN PREV COUNTER, THIS LAW IS A BETTER ANSWER
                if count_temp_law_equal > count_first_law_equal:
                    # UPDATE ALL FIRST 5 PLACES OF THE RESULTS
                    count_fifth_law_equal = count_forth_law_equal
                    fifth_result = fourth_result
                    law_of_fifth_result = law_of_fourth_result

                    count_forth_law_equal = count_third_law_equal
                    fourth_result = third_result
                    law_of_fourth_result = law_of_third_result

                    count_third_law_equal = count_sec_law_equal
                    third_result = sec_result
                    law_of_third_result = law_of_sec_result

                    count_sec_law_equal = count_first_law_equal
                    sec_result = first_result
                    law_of_sec_result = law_of_first_result

                    count_first_law_equal = count_temp_law_equal
                    first_result = section
                    law_of_first_result = law[0]
                else:
                    if count_temp_law_equal > count_sec_law_equal:
                        # UPDATE PLACES 2,3,4,5 OF THE RESULTS
                        count_fifth_law_equal = count_forth_law_equal
                        fifth_result = fourth_result
                        law_of_fifth_result = law_of_fourth_result

                        count_forth_law_equal = count_third_law_equal
                        fourth_result = third_result
                        law_of_fourth_result = law_of_third_result

                        count_third_law_equal = count_sec_law_equal
                        third_result = sec_result
                        law_of_third_result = law_of_sec_result

                        count_sec_law_equal = count_temp_law_equal
                        sec_result = section
                        law_of_sec_result = law[0]
                    else:
                        if count_temp_law_equal > count_third_law_equal:
                            # UPDATE PLACES 3,4,5 OF THE RESULTS
                            count_fifth_law_equal = count_forth_law_equal
                            fifth_result = fourth_result
                            law_of_fifth_result = law_of_fourth_result

                            count_forth_law_equal = count_third_law_equal
                            fourth_result = third_result
                            law_of_fourth_result = law_of_third_result

                            count_third_law_equal = count_temp_law_equal
                            third_result = section
                            law_of_third_result = law[0]
                        else:
                            if count_temp_law_equal > count_forth_law_equal:
                                # UPDATE PLACES 4,5 OF THE RESULTS
                                count_fifth_law_equal = count_forth_law_equal
                                fifth_result = fourth_result
                                law_of_fifth_result = law_of_fourth_result

                                count_forth_law_equal = count_temp_law_equal
                                fourth_result = section
                                law_of_fourth_result = law[0]
                            else:
                                if count_temp_law_equal > count_fifth_law_equal:
                                    # UPDATE FIFTH PLACE OF THE RESULTS
                                    count_fifth_law_equal = count_temp_law_equal
                                    fifth_result = section
                                    law_of_fifth_result = law[0]
                count_temp_law_equal = 0

        # PRINT THE ANSWER FOR THE SEARCH
        print("The most suitable law sections for your search is : \n")
        print("(1)")
        array_of_first_result = first_result.split()
        check_if_found = 0
        for word_in_result in array_of_first_result:
            for lst in list_of_similar_lists:
                if word_in_result in lst:
                    print('\033[1m' + word_in_result, end=" ")
                    check_if_found = 1
                    break
            if check_if_found == 0:
                print('\033[0m' + word_in_result, end=" ")
            check_if_found = 0
        print('\033[0m' + "\n")
        print("with suitability percentage of : " + repr(round(count_first_law_equal / 100)) + "%")
        print("From the law : ")
        print(law_of_first_result)
        if sec_result != "":
            print("\n(2)")
            array_of_sec_result = sec_result.split()
            check_if_found = 0
            for word_in_result in array_of_sec_result:
                for lst in list_of_similar_lists:
                    if word_in_result in lst:
                        print('\033[1m' + word_in_result, end=" ")
                        check_if_found = 1
                        break
                if check_if_found == 0:
                    print('\033[0m' + word_in_result, end=" ")
                check_if_found = 0
            print('\033[0m' + "\n")
            print("with suitability percentage of : " + repr(round(count_sec_law_equal / 100)) + "%")
            print("From the law : ")
            print(law_of_sec_result)
            if third_result != "":
                print("\n(3)")
                array_of_third_result = third_result.split()
                check_if_found = 0
                for word_in_result in array_of_third_result:
                    for lst in list_of_similar_lists:
                        if word_in_result in lst:
                            print('\033[1m' + word_in_result, end=" ")
                            check_if_found = 1
                            break
                    if check_if_found == 0:
                        print('\033[0m' + word_in_result, end=" ")
                    check_if_found = 0
                print('\033[0m' + "\n")
                print("with suitability percentage of : " + repr(round(count_third_law_equal / 100)) + "%")
                print("From the law : ")
                print(law_of_third_result)
                if fourth_result != "":
                    print("\n(4)")
                    array_of_fourth_result = fourth_result.split()
                    check_if_found = 0
                    for word_in_result in array_of_fourth_result:
                        for lst in list_of_similar_lists:
                            if word_in_result in lst:
                                print('\033[1m' + word_in_result, end=" ")
                                check_if_found = 1
                                break
                        if check_if_found == 0:
                            print('\033[0m' + word_in_result, end=" ")
                        check_if_found = 0
                    print('\033[0m' + "\n")
                    print("with suitability percentage of : " + repr(round(count_forth_law_equal / 100)) + "%")
                    print("From the law : ")
                    print(law_of_fourth_result)
                    if fifth_result != "":
                        print("\n(5)")
                        array_of_fifth_result = fifth_result.split()
                        check_if_found = 0
                        for word_in_result in array_of_fifth_result:
                            for lst in list_of_similar_lists:
                                if word_in_result in lst:
                                    print('\033[1m' + word_in_result, end=" ")
                                    check_if_found = 1
                                    break
                            if check_if_found == 0:
                                print('\033[0m' + word_in_result, end=" ")
                            check_if_found = 0
                        print('\033[0m' + "\n")
                        print("with suitability percentage of : " + repr(round(count_fifth_law_equal / 100)) + "%")
                        print("From the law : ")
                        print(law_of_fifth_result)

        search_string = input("\nPlease enter your search ('q' to quit) : ")

    # CLOSE THE FILES
    main_law_file.close()
    dictionary.close()

    # ********************************************
    # BELOW IS HOW WE SAVED THE CORPUS ONCE AND FROM NOW ON WE ONLY LOAD IT, SO IT'S NOT NEEDED
    # model = Word2Vec(main_law_list, min_count=1,size= 50,workers=3, window =3, sg = 1)

    # model = gensim.models.KeyedVectors.load_word2vec_format('cc.he.300.vec')
    # model.init_sims(replace=True)
    # model.save('wordVec')
    # ********************************************


    # # ************************************************
    # # ************************************************
    # # BELOW IS CODE TO SAVE THE XML FILES INTO LISTS AND THEN INTO A FILE SO DOESNT NEED TO CREATE LISTS EVERY TIME
    #
    # tfidf_dict = {}
    #
    # # OPEN FILE
    # laws_names = ET.parse("./ReshumotXml/law_dictionary.xml")
    #
    # counter_of_laws_in_file = 0
    # main_law_list = []
    # list_for_tfidf = []
    # for path in laws_names.findall('.//lawPath'):
    #     if counter_of_laws_in_file == 220:
    #         break
    #     counter_of_laws_in_file = counter_of_laws_in_file + 1
    #     # law_content_list = []
    #     law_content_string = ""
    #     # FIX THE PATH TO THE CORRECT FOLDER OF THE LAW
    #     fixed_path = path.text.replace("\\", "/")
    #     law_content_path = "./ReshumotXml/" + fixed_path + "/he@/main.xml"
    #     # GET THE XML FILE OF THE LAW
    #     law_content = ET.parse(law_content_path)
    #     laws_sections_list = []
    #     # ADD THE PARAGRAPHS AND SIGNATURES (PERSON & ROLE) TO A STRING CONTAINING THE LAW
    #     for elem in law_content.findall('.//{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}p'):
    #         if isinstance(elem.text, str):
    #             # DELETE WHITE SPACES AND UNNECESSARY TOKENS
    #             fixed_text = re.sub(r'\s{2,}', ' ', elem.text)
    #             fixed_text = re.sub(r'@\w+', '', fixed_text)
    #             fixed_text = fixed_text.replace(",", "")
    #             fixed_text = fixed_text.replace("(", " ")
    #             fixed_text = fixed_text.replace(")", " ")
    #             fixed_text = fixed_text.replace("`", "")
    #             # fixed_text = fixed_text.replace("-", " ")
    #             fixed_text = fixed_text.replace(":", "")
    #             fixed_text = fixed_text.replace(";", "")
    #             fixed_text = fixed_text.replace(".", "")
    #             fixed_text = fixed_text.replace("]", "")
    #             fixed_text = fixed_text.replace("[", "")
    #             fixed_text = fixed_text.replace("\"", "")
    #             laws_sections_list.append(fixed_text)
    #             list_for_tfidf.append(fixed_text)
    #             # law_content_string = law_content_string + " " + fixed_text
    #     for elem in law_content.findall('.//{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}person'):
    #         if isinstance(elem.text, str):
    #             fixed_text = re.sub(r'\s{2,}', ' ', elem.text)
    #             laws_sections_list.append(fixed_text)
    #             list_for_tfidf.append(fixed_text)
    #             # law_content_string = law_content_string + " " + fixed_text
    #     for elem in law_content.findall('.//{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}role'):
    #         if isinstance(elem.text, str):
    #             fixed_text = re.sub(r'\s{2,}', ' ', elem.text)
    #             laws_sections_list.append(fixed_text)
    #             list_for_tfidf.append(fixed_text)
    #             # law_content_string = law_content_string + " " + fixed_text
    #     main_law_list.append(laws_sections_list)
    #
    #
    # # with open("main_law_list.txt", "wb") as fp:  # Pickling
    # #     pickle.dump(main_law_list, fp)
    # #
    # # with open("list_for_tfidf.txt", "wb") as fp:  # Pickling
    # #     pickle.dump(list_for_tfidf, fp)
    #
    # with open("list_for_tfidf.txt", "rb") as list_tfidf_file:  # Unpickling
    #     list_for_tfidf = pickle.load(list_tfidf_file)

    # list_tfidf_file.close()
    #
    # # CALCULATE THE TF-IDF OF EACH WORD IN THE LAWS FILE
    # vectorizer = TfidfVectorizer()
    # vectors = vectorizer.fit_transform(list_for_tfidf)
    # feature_names = vectorizer.get_feature_names()
    # dense = vectors.todense()
    # denselist = dense.tolist()
    # num_of_words_in_laws_file = len(feature_names)
    # num_of_sections_in_tfidf_list = len(list_for_tfidf)
    # #
    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    # # CREATE DICTIONARY FOR WORD AND ITS HIGHEST VALUE
    # i = 0
    # while i < num_of_words_in_laws_file:
    #     if feature_names[i] not in tfidf_dict:
    #         tfidf_dict[feature_names[i]] = 0
    #     j = 0
    #     while j < num_of_sections_in_tfidf_list:
    #         if denselist[j][i] > tfidf_dict[feature_names[i]]:
    #             tfidf_dict[feature_names[i]] = denselist[j][i]
    #         j = j + 1
    #     i = i + 1
    #
    # # *********************************************
    # # *********************************************


