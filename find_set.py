import sys
import itertools
import subprocess
import json

# cards = [
#             {"count": 1, "shape": "s-shape"},
#             {"count": 2, "shape": "s-shape"},
#             {"count": 3, "shape": "s-shape"},
#             {"count": 1, "shape": "oval"},
#             {"count": 2, "shape": "oval"},
#             {"count": 3, "shape": "oval"},
#             {"count": 1, "shape": "diamond"},
#             {"count": 2, "shape": "diamond"},
#             {"count": 3, "shape": "diamond"}
#         ]
#
# cards_2 = [
#             {"count": 1, "shape": "s-shape"},
#             {"count": 2, "shape": "s-shape"},
#             {"count": 3, "shape": "s-shape"}
#         ]
#

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


def prediction(image, property):
    # result = subprocess.check_output("curl localhost/models/images/classificiation/classify_one.json -XPOST -F job_id=%s -F image_file=@%s" % ())
    # predictions = json.loads(result)
    if property == "shape":
        predictions = [["s_shape", 30],["diamond", 60], ["s_shape", 30]]
    else if property == "count"
        predictions = [["three", 30],["two", 60], ["one", 30]]

    sorted_predictions = sorted(predictions, key=lambda v: v[1], reverse=True)
    return sorted_predictions[0][0]

def assemble_card_from_image(image):
    shape_prediction = prediction(image, 1)
    count_prediction = prediction(image, 1)
    return {
        "count": count_prediction,
        "shape": shape_prediction
    }    

def main(files):
    cards = map(assemble_card_from_image, files)
    
    for found_set in find_sets(cards_2, ["count", "shape"]):
        print "Set was found %s" % str(found_set)
    

if __name__ == "__main__":
    files = sys.argv[1:]
    main(files)
        

