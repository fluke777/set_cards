import json
import os
import subprocess
import sys
import itertools

def list_same_or_different(the_list):
    """This function gets a list of values and respons True/False if they are all the same or all different
            [1,2,3] => True
            [1,1,1] => True
            [1,1,2] => False
    """
    return (len(set(the_list)) == 1 or len(set(the_list)) == 3)

def is_set(cards_triplet, properties):
    """Function expects list of dictionaries representing one combination of cards
       and list of properties that should be compared"""
    data = map(lambda prop: map(lambda t: t[prop], cards_triplet), properties)
    return all(map(lambda d: list_same_or_different(d), data))
        
def find_sets(cards, props):
    """Function that takes or the cards on the table. Creates combinations of three and evaluates if they contain any sets.
       The sets found are returned. If nothing is found empty list is returned
    """
    return filter(lambda triplet: is_set(triplet, props), itertools.combinations(cards, 3))

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

def prediction(image, job_id, prop):
    result = subprocess.check_output(["curl",  "127.0.0.1:3001/models/images/classification/classify_one.json", "-X", "POST", "-F", "job_id=%s" % job_id, "-F",  "image_file=@%s" % image])
    predictions = json.loads(result)['predictions']
    sorted_predictions = sorted(predictions, key=lambda v: v[1], reverse=True)
    return [prop, sorted_predictions[0][0]]

def assemble_card_from_image(image, job_spec):
    return dict(map(lambda (job_id, prop): prediction(image, job_id, prop), job_spec))


def main(dir, job_spec):
    files = list(absoluteFilePaths(dir))
    cards = map(lambda f: assemble_card_from_image(f, job_spec), files)
    
    for found_set in find_sets(cards, ["count", "shape"]):
         print "Set was found %s" % str(found_set)

if __name__ == "__main__":
    job_spec = [["20180508-055305-53fc", "shape"], ["20180508-051345-7660", "count"]]
    main(sys.argv[1], job_spec)
