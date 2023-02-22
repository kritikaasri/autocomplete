# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 15:42:34 2021

@author: Kritika Srivastava
"""

from tkinter import *
from collections import defaultdict
import pickle
import sys
# from english_words import english_words_set
from nltk.corpus import words
import os

class Trie:
    
    def __init__(self, tree = defaultdict()):
        self.root = tree

    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})
        current.setdefault("_end")

    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current:
                return False
            current = current[letter]
        if "_end" in current:
            return True
        return False
    
    def autoSuggestions(self, key):
        node = self.root
        not_found = False
        temp_word = ''
        is_last = False
 
        for a in key:
            if a not in node:
                not_found = True
                break
 
            temp_word = temp_word+a
            node = node[a]
 
        if not_found:
            return (-1, [])
        
        if self.search(key):
            is_last = True
        
        word_list = []
        self.suggestions(node, temp_word, word_list)
        word_list.sort(key=len)
        #if key in word_list:
            #word_list.remove(key)
        """if len(word_list)>5:
            word_list = word_list[:5]"""
        return (is_last, word_list)
    
    def suggestions(self, node, prefix, word_list):
        for letter, nodes in node.items():
            if letter=='_end':
                word_list.append(prefix)
                return
            self.suggestions(nodes, prefix+letter, word_list)
        
    def startsWith(self, prefix):
        current = self.root
        for letter in prefix:
            if letter not in current:
                return -1
            current = current[letter]
        return True

    def save(self, fname):
        with open(fname, 'wb') as handle:
            pickle.dump(self.root, handle, protocol=pickle.HIGHEST_PROTOCOL)

if not os.path.exists('dict.pickle'):
    se = set(english_words_set)
    wrds = set(words.words())
    wrds = wrds|se
    tree = Trie()
    for wrd in wrds:
        tree.insert(wrd)  

with open('dict.pickle', 'rb') as handle:
    b = pickle.load(handle)
    
tree = Trie(b)
modified = False 
typed = ""

root = Tk()
root.title("Autocompleter")
root.iconbitmap("index.ico")
root.geometry("600x400")

my_label = Label(root, text="Start typing\nThe \"Add me!\" button saves your entry to the trie for future use after closing the screen.", font = ("Calibri", 12), fg = "grey")
my_label.pack(pady=20)
my_entry=Entry(root, font=("Calibri", 16))
my_entry.pack(pady = 5)

my_list = Listbox(root, width=60)
my_list.pack(pady=40)

def fn():
    if not tree.search(typed):
        global modified
        tree.insert(typed)
        modified = True
        print("Entry added to trie.")
    
btn = Button(root, text = 'Add me!', bd = '5',command = fn)
btn.pack(side = 'top')

def update(data):
    my_list.delete(0, END)
    for item in data:
        my_list.insert(END, item)

def fillout(e):
    my_entry.delete(0, END)
    my_entry.insert(0, my_list.get(ANCHOR))

def check(e):
    global modified
    global typed
    
    typed = my_entry.get()
    
    if typed=="":
        data = ls
    else:
        boo, data = tree.autoSuggestions(typed)
        """
        if boo==False:
            print("Word not found.")
            modified = True
            tree.insert(typed)
            data
        """
        """
        if boo==-1:
            print("Word not found.")
            modified = True
            print(modified)
            tree.insert(typed)
            data = [typed]
        """
    update(data)

boo, ls = tree.autoSuggestions("a")

update(ls)
my_list.bind("<<ListboxSelect>>", fillout)

my_entry.bind("<KeyRelease>", check)
root.mainloop()

print(modified)

if modified == True:
    tree.save('dict.pickle')
    print("All your additions have been saved.")

print("You've exited.")
sys.exit()
