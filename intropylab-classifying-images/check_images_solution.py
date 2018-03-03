#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images_solution.py
#                                                                             
# PROGRAMMER: Jennifer S.
# DATE CREATED: 01/30/2018                                  
# REVISED DATE: 02/27/2018  - reduce scope of program
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Main program function defined below
def main():
    # Measures total program runtime by collecting start time
    start_time = time()
    
    # Creates & retrieves Command Line Arugments
    in_arg = get_input_args()
    
    # Creates Pet Image Labels by creating a dictionary 
    answers_dic = get_pet_labels(in_arg.dir)

    # Creates Classifier Labels with classifier function, Compares Labels, 
    # and creates a results dictionary 
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)
    
    # Adjusts the results dictionary to determine if classifier correctly 
    # classified images as 'a dog' or 'not a dog'. This demonstrates if 
    # model can correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(result_dic, in_arg.dogfile)
    
    # Calculates results of run and puts statistics in results_stats_dic
    results_stats_dic = calculates_results_stats(result_dic)

    # Prints summary results, incorrect classifications of dogs
    # and breeds if requested
    print_results(result_dic, results_stats_dic, in_arg.arch, True, True)
    
    # Measure total program run time by collecting end time
    end_time = time()
    
    # Computes overall run time in seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    print("\n** Total Elapsed Run Time:",
          str(int((tot_time/3600)))+":"+str(int((tot_time%3600)/60))+":"
          +str(int((tot_time%3600)%60)) )
    


# Functions defined below
    
# get_input_args() - Handles retrieving and parsing the commandline 
# arguments created and defined using argparse module. This function 
# returns these arguments.
# @return parser.parse_args() - collection of commandline arguments 
def get_input_args():
    # Creates parse 
    parser = argparse.ArgumentParser()

    # Creates 3 command line arguments args.dir for path to images files,
    # args.arch which CNN model to use for classification, args.labels path to
    # text file with names of dogs.
    parser.add_argument('--dir', type=str, default='pet_images/', 
                        help='path to folder of images')
    parser.add_argument('--arch', type=str, default='vgg', 
                        help='chosen model')
    parser.add_argument('--dogfile', type=str, default='dognames.txt',
                        help='text file that has dognames')

    # returns parsed argument collection
    return parser.parse_args()


# get_pet_labels(image_dir) - Creates a dictionary of pet labels based upon 
# the filenames of the image files. This will be used to check the accuracy of 
# the image classifier model.
# @param image_dir - The (full) path to the folder of images that are to be
#                     classified by pretrained CNN models
# @return petlabels_dic - Dictionary with key = filename value = label  
def get_pet_labels(image_dir):
   # Creates list of files in directory
   in_files = listdir(image_dir)
   
   # Processes each of the files to create a dictionary where the key
   # is the filename and the value is the picture label (below).

   # Creates empty dictionary for the labels
   petlabels_dic = dict()
   
   # Processes through each file in the directory, extracting only the words
   # of the file that contain the pet image label
   for idx in range(0, len(in_files), 1):
       
       # Skips file if starts with . (like .DS_Store of Mac OSX) because it 
       # isn't an pet image file
       if in_files[idx][0] != ".":
           
           # Uses split to extract words of filename into list image_name 
           image_name = in_files[idx].split("_")
       
           # Creates temporary label variable to hold pet label name extracted 
           pet_label = ""
           
           # Processes each of the character strings(words) split by '_' in 
           # list image_name by processing each word - only adding to pet_label
           # if word is all letters - then process by putting blanks between 
           # these words and putting them in all lowercase letters
           for word in image_name:
               
               # Only add to pet_label if word is all letters add blank at end
               if word.isalpha():
                   pet_label += word.lower() + " "
                   
           # strips off trailing whitespace
           pet_label = pet_label.strip()
           
           # If filename doesn't already exist in dictionary add it and it's
           # pet label - otherwise print an error message because indicates 
           # duplicate files (filenames)
           if in_files[idx] not in petlabels_dic:
              petlabels_dic[in_files[idx]] = pet_label
              
           else:
               print("Warning: Duplicate files exist in directory", 
                     in_files[idx])

   # returns dictionary of labels
   return(petlabels_dic)


# classify_images(images_dir, petlabel_dic, model) - Creates classifier labels
# with classifier function, compares labels and creates a dictionary of 
# labels based upon the classification that is returned by the pretrained CNN 
# model whose architecture is defined by the input parameter model. Returns
# dictionary of both image labels and the comparison of them to each other
#
# PLEASE NOTE: You will be using the classifier() function defined in 
#  classifier.py within this function. The proper use of the
#  classifier() function can be found in test_classifier.py Please refer to
#  this program prior to using the classifier() function to classify images 
# @param images_dir - The (full) path to the folder of images that are to be
#                     classified by pretrained CNN models
# @param petlabel_dic - Dictionary that contains the pet image(true) labels
#                     that classify what's in the image key = filename & 
#                     value = pet image(true) label (lowercase with spaces) 
# @param model - pretrained CNN whose architecture is indicated by this 
#                parameter, choices are: resnet, alexnet, vgg
# @return results_dic - Dictionary with key = image filename  
#                      value = list[pet image label, classifier label, 1/0] 
#                      where 1 = match between pet image and classifer labels 
#                      and 0 = no match between labels
def classify_images(images_dir, petlabel_dic, model):
   # Creates dictionary that will have all the results key = filename
   # value = list [Pet Label, Classifier Label, Match(1=yes,0=no)]
   results_dic = dict()

   # Process all files in the petlabels_dic - use images_dir to give fullpath
   for key in petlabel_dic:
       
       # Runs classifier function to classify the images classifier function 
       # inputs: path + filename  and  model, returns model_label 
       # as classifier label
       model_label = classifier(images_dir+key, model)
       
       # Processes the results so they can be compared with pet image labels
       # set labels to lowercase (lower) and stripping off whitespace(strip)
       model_label = model_label.lower()
       model_label = model_label.strip()
       
       # defines truth as pet image label and trys to find it using find() 
       # string function to find it within classifier label(model_label).
       truth = petlabel_dic[key]
       found = model_label.find(truth)
       
       # If found (0 or greater) then make sure true answer wasn't found within
       # another word and thus not really found, if truely found then add to 
       # results dictionary and set match=1(yes) otherwise as match=0(no)
       if found >= 0:
           if ( (found == 0 and len(truth)==len(model_label)) or
                (  ( (found == 0) or (model_label[found - 1] == " ") )  and
                   ( (found + len(truth) == len(model_label)) or   
                      (model_label[found + len(truth): found+len(truth)+1] in 
                     (","," ") ) 
                   )      
                )
              ):
               # found label as stand-alone term (not within label)
               if key not in results_dic:
                   results_dic[key] = [truth, model_label, 1]
                   
           # found within a word/term not a label existing on its own 
           else:
               if key not in results_dic:
                   results_dic[key] = [truth, model_label, 0]
                   
       # if not found set results dictionary with match=0(no)
       else:
           if key not in results_dic:
               results_dic[key] = [truth, model_label, 0]
               
   # Return results dictionary
   return(results_dic)


# adjust_results4_isadog(results_dic, dogsfile) -  Adjusts the results 
# dictionary to determine if classifier correctly classified images 'as a dog'
# or 'not a dog' especially when not an match. Demonstrates if model 
# architecture correctly classifies dog images even if it gets dog breed wrong
# @param results_dic - Dictionary with key = image filename  
#             value = list[pet image label, classifier label, 1/0, 1/0*, 1/0**] 
#             For 1/0 where 1 = match between pet image and classifer labels &  
#             0 = no match.  1/0* and 1/0** added by this function.
#             For 1/0* where 1 = pet image is a dog & 0 = pet Image is NOT a 
#             dog.  For 1/0** 1 = Classifier classifies image as a dog &
#             0 = Classifier classifies image as NOT a dog.
# @param dogsfile - text file that contains names of all dogs from ImageNet 
#                   1000 labels (used by classifier model) and dog names from
#                   the pet image files. This file has one dog name per line
#                   dog names are all in lowercase with spaces separating the 
#                   distinct words of the dogname. 
def adjust_results4_isadog(results_dic, dogsfile):
    # Creates dognames dictionary for quick matching to results_dic labels from
    # real answer & classifier's answer
    dognames_dic = dict()

    # Reads in dognames from file, 1 name per line & automatically closes file
    with open(dogsfile, "r") as infile:
        # Reads in dognames from first line in file
        line = infile.readline()

        # Processes each line in file until reaching EOF (end-of-file) by 
        # processing line and adding dognames to dognames_dic with while loop
        while line != "":

            # Process line by striping newline from line
            line = line.rstrip()

            # adds dogname to dogsnames_dic if it doesn't already exist in dic
            if line not in dognames_dic:
                dognames_dic[line] = 1
            else:
                print("**Warning: Duplicate dognames", line)            

            # Reads in next line in file to be processed with while loop
            # if this line isn't empty (EOF)
            line = infile.readline()
    
    
    # Add to whether pet labels & classifier labels are dogs by appending
    # two items to end of value(List) in results_dic. 
    # List Index 3 = whether(1) or not(0) Pet Image Label is a dog AND 
    # List Index 4 = whether(1) or not(0) Classifier Label is a dog
    # How - iterate through results_dic if labels are found in dognames_dic
    # then label "is a dog" index3/4=1 otherwise index3/4=0 "not a dog"
    for key in results_dic:

        # Pet Image Label IS of Dog (e.g. found in dognames_dic)
        if results_dic[key][0] in dognames_dic:
            
            # Classifier Label IS image of Dog (e.g. found in dognames_dic)
            # appends (1, 1) because both labels are dogs
            if results_dic[key][1] in dognames_dic:
                results_dic[key].extend((1, 1))
                
            # Classifier Label IS NOT image of dog (e.g. NOT in dognames_dic)
            # appends (1,0) because only pet label is a dog
            else:
                results_dic[key].extend((1, 0))
            
        # Pet Image Label IS NOT a Dog image (e.g. NOT found in dognames_dic)
        else:
            # Classifier Label IS image of Dog (e.g. found in dognames_dic)
            # appends (0, 1)because only Classifier labe is a dog
            if results_dic[key][1] in dognames_dic:
                results_dic[key].extend((0, 1))
                
            # Classifier Label IS NOT image of Dog (e.g. NOT in dognames_dic)
            # appends (0, 0) because both labels aren't dogs
            else:
                results_dic[key].extend((0, 0))


# calculates_results_stats(results_dic) -  Calculates statistics
# of the results of the run using classifier's model architecture on 
# classifying images. Then puts the results statistics in a dictionary 
# (results_stats) so that it's returned for printing to help determine the 
# 'best' model for classifying images. results_stats dictionary has 
# key = statistic's name & value = statistic's value  
# @param results_dic - Dictionary with key = image filename
#             value = list[pet image label, classifier label, 1/0, 1/0*, 1/0**]
#             For 1/0 where 1 = match between pet image and classifer labels &
#             0 = no match.
#             For 1/0* where 1 = pet image is a dog & 0 = pet Image is NOT a
#             dog.
#             For 1/0** 1 = Classifier classifies image as a dog &
#             0 = Classifier classifies image as NOT a dog.
# @return results_stats - Dictionary with key = statistic's name value = 
#                      statistics value 
def calculates_results_stats(results_dic):
    # creates empty dictionary for results_stats
    results_stats=dict()
    
    # Sets all counters to initial values of zero so that they can 
    # be incremented while processing through the images in results_dic 
    results_stats['n_dogs_img'] = 0
    results_stats['n_match'] = 0
    results_stats['n_correct_dogs'] = 0
    results_stats['n_correct_notdogs'] = 0
    results_stats['n_correct_breed'] = 0       
    
    # process through the results dictionary
    for key in results_dic:
        # Labels Match Exactly
        if results_dic[key][2] == 1:
            results_stats['n_match'] += 1
            
            # Pet Image Label is a Dog AND Labels match- counts correct breed
            if results_dic[key][3] == 1:
                results_stats['n_correct_breed'] += 1
        
        # Pet Image Label is a Dog - counts number of dog images
        if results_dic[key][3] == 1:
            results_stats['n_dogs_img'] += 1
            
            # Classifier classifies image as Dog (& pet image is a dog)
            # counts number of correct dog classifications
            if results_dic[key][4] == 1:
                results_stats['n_correct_dogs'] += 1
                
        # Pet Image Label is NOT a Dog
        else:
            # Classifier classifies image as NOT a Dog(& pet image isn't a dog)
            # counts number of correct NOT dog clasifications.
            if results_dic[key][4] == 0:
                results_stats['n_correct_notdogs'] += 1

    # Calculates run statistics (counts & percentages) below that are calculated
    # using counters from above.
    
    # calculates number of total images
    results_stats['n_images'] = len(results_dic)

    # calculates number of not-a-dog images using - images & dog images counts
    results_stats['n_notdogs_img'] = (results_stats['n_images'] - 
                                      results_stats['n_dogs_img']) 

    # Calculates % correct for matches
    results_stats['pct_match'] = (results_stats['n_match'] / 
                                  results_stats['n_images'])*100.0
    
    # Calculates % correct dogs
    results_stats['pct_correct_dogs'] = (results_stats['n_correct_dogs'] / 
                                         results_stats['n_dogs_img'])*100.0    

    # Calculates % correct breed of dog
    results_stats['pct_correct_breed'] = (results_stats['n_correct_breed'] / 
                                          results_stats['n_dogs_img'])*100.0

    # Calculates % correct not-a-dog images
    # Uses conditional statement for when no 'not a dog' images were submitted 
    if results_stats['n_notdogs_img'] > 0:
        results_stats['pct_correct_notdogs'] = (results_stats['n_correct_notdogs'] /
                                                results_stats['n_notdogs_img'])*100.0
    else:
        results_stats['pct_correct_notdogs'] = 0.0
        
    # returns results_stast dictionary 
    return results_stats


# print_results(results_dic, results_stats, model,
#               print_incorrect_dogs = False, print_incorrect_breed = False) -
# Prints summary results on the classification and then prints incorrectly 
# classified dogs and incorrectly classified dog breeds if user indicates 
# they want those printouts (use non-default values)
# @param results_dic - Dictionary with key = image filename
#             value = list[pet image label, classifier label, 1/0, 1/0*, 1/0**]
#             For 1/0 where 1 = match between pet image and classifer labels &
#             0 = no match.
#             For 1/0* where 1 = pet image is a dog & 0 = pet Image is NOT a
#             dog.
#             For 1/0** 1 = Classifier classifies image as a dog &
#             0 = Classifier classifies image as NOT a dog.
# @param results_stats - Dictionary with key = statistic's name value =
#                      statistics value 
# @param model - pretrained CNN whose architecture is indicated by this 
#                parameter, choices are: resnet, alexnet, vgg
# @param print_incorrect_dogs - Boolean - True prints incorrectly classified 
#                               dog images default = False (no print) 
# @param print_incorrect_breed - Boolean - True prints incorrectly classified 
#                               dog breeds default = False (no print)
def print_results(results_dic, results_stats, model, 
                  print_incorrect_dogs = False, print_incorrect_breed = False):
    # Prints summary statistics over the run
    print("\n\n*** Results Summary for CNN Model Architecture",model.upper(),"***")
    print("%20s: %3d" % ('N Images', results_stats['n_images']))
    print("%20s: %3d" % ('N Dog Images', results_stats['n_dogs_img']))
    print("%20s: %3d" % ('N Not-Dog Images', results_stats['n_notdogs_img']))

    # Prints summary statistics (percentages) on Model Run
    print(" ")
    for key in results_stats:
        if key[0] == "p":
            print("%20s: %5.1f" % (key, results_stats[key]))
    

    # IF print_incorrect_dogs == True AND there were images incorrectly 
    # classified as dogs or vice versa - print out these cases
    if (print_incorrect_dogs and 
        ( (results_stats['n_correct_dogs'] + results_stats['n_correct_notdogs'])
          != results_stats['n_images'] ) 
       ):
        print("\nINCORRECT Dog/NOT Dog Assignments:")

        # process through results dict, printing incorrectly classified dogs
        for key in results_dic:

            # Pet Image Label is a Dog - Classified as NOT-A-DOG
            if results_dic[key][3] == 1 and results_dic[key][4] == 0:
                print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                          results_dic[key][1]))
                    
            # Pect Image Label is NOT-a-Dog - Classified as a-DOG
            if results_dic[key][3] == 0 and results_dic[key][4] == 1:
                print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                          results_dic[key][1]))

    # IF print_incorrect_breed == True AND there were dogs whose breeds 
    # were incorrectly classified - print out these cases                    
    if (print_incorrect_breed and 
        (results_stats['n_correct_dogs'] != results_stats['n_correct_breed']) 
       ):
        print("\nINCORRECT Dog Breed Assignment:")

        # process through results dict, printing incorrectly classified breeds
        for key in results_dic:

            # Pet Image Label is-a-Dog, classified as-a-dog but is WRONG breed
            if (results_dic[key][3] == 1 and results_dic[key][4] == 1 and
                results_dic[key][2] == 0):
                print("Real: %-26s   Classifier: %-30s" % (results_dic[key][0],
                                                          results_dic[key][1]))
                
                
                
# Call to main function to run the program.
main()

