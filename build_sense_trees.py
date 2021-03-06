from babelnet.structures import Sense, Tree
from babelnet.utils import *
import cPickle as pickle

import logging
import logging.config


# to later save the sense tree
def save(tree, fileName):
	with open(fileName, 'wb') as handle:
    		pickle.dump(tree, handle)
# to later load the sense tree
def load(fileName):
	with open(fileName, 'rb') as handle:
    		return  pickle.load(handle)

# to actually build the sense tree
def buildSenseTree(root, lang, key, maxLevel=5, weightThreshold=0):
    
    def dictToSense(d):
        return Sense(d['id'], d['lemma'], d['weight'], d['normalizedWeight'])    
                 
    def addChildren(root, level=0):
        if level < maxLevel:
            sense = root.value
            
            hyper, hypo, anto =  getHyperHypoAntoNyms(sense.id, lang, key)
            for h in hypo:
                if h['weight'] > weightThreshold:
                    root.add_child(Tree(dictToSense(h)))
            
            for child in root.children:
                addChildren(child, level +1)
            
    addChildren(root)
    
    return root

if __name__ == '__main__':

    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    lang = 'EN'
    key = 'key'
    emotions = ['love', 'happiness', 'surprise', 'emotionless', 'sad', 'disgust', 'anger', 'fear']
    treeDepth = 3

    for emotion in emotions:
        logger.info('Getting synsetIds for ' + emotion)
        id = getSynsetIds(emotion, lang, key)[0]
        
        logger.info('Building sense tree...')
        sense = Sense(id, emotion)
        tree = buildSenseTree(Tree(sense), lang, key, treeDepth, 0)
        
        logger.info('Saving sense tree...')
        
        save(tree, emotion + '.pickle')
        
        logger.info('Done!')
