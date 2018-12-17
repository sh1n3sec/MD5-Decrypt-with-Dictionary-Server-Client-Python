import os, time, sys

import datetime

from random import randint

import hashlib



pipe_dir = "."

pipe_name = 'so_server'

dic_path = "dicionario.txt"

withUppercase = True

N_ITERATIONS = 4



global time_ini_send



def getGroupsList(pipe_dir):

    groups = []

    files = os.listdir(pipe_dir)



    for file in files:

        if file.startswith("so_") and file != "so_server":

            groups.append(file)



    return groups





def getDictionary(dic_path):

    file = open(dic_path, "r")

    lines = file.readlines()

    file.close()



    return lines





def log(msg):

    ts = time.time()

    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    print("[" + st + "] " + msg)





def selectWord(dic, doUppercase):

    word = dic[randint(0, len(dic))]

    word = word[0:-1]



    w = list(word)

    for i in range(randint(0, len(w))):

        pos = randint(0, len(w) - 1)

        w[pos] = w[pos].upper()



    if doUppercase:

        word = "".join(w)



    return word





def encryptWord(word):

    md5 = hashlib.md5()

    my_bytes = str.encode(word)

    type(my_bytes)

    md5.update(my_bytes)

    res = md5.hexdigest()

    # encrypt = hashlib.md5(word).hexdigest()

    return res





def sendEncryptToGroups(pipe_dir, groups, encrypt_):

    global time_ini_send

    time_ini_send = time.time()



    for group in groups:

        pipeout = os.open(pipe_dir + "/" + group, os.O_WRONLY)

        my_byt = str.encode(encrypt_+"\n")

        type(my_byt)

        os.write(pipeout, my_byt )

        os.close(pipeout)

        log("> Sent to group " + group)





def waitResponseFromGroups(pipename, groups, word, encrypt):

    global time_ini_send

    results = {}



    #	log("Waiting for message from group")

    #	pipein = open(pipename, 'r')



    while True:

        log("Waiting for message from group")

        pipein = open(pipename, 'r')

        resp = pipein.readline()

        print ("Received: "+resp)

        resp = resp[:-1]

        l = resp.split(":")

        results[l[0]] = resp + ":" + str(time.time() - time_ini_send)

        log("Received: " + resp)

        pipein.close()



        if len(results) == len(groups):

            break



    return results







if __name__ == '__main__':





    """ Create named pipe """

    if not os.path.exists(pipe_dir + "/" + pipe_name):

        os.mkfifo(pipe_dir + "/" + pipe_name)



    groups = getGroupsList(pipe_dir);



    if len(groups) <= 0:

        log("No group is running!")

        exit()



    log("Starting...")



    niter = 0

    while(niter < N_ITERATIONS):

        dic = getDictionary(dic_path)

        log("- Dictionary size: " + str(len(dic)))



        word = selectWord(dic, doUppercase=withUppercase)

        log("- Word: " + word)



        encrypt = encryptWord(word)

        log(encrypt)



        sendEncryptToGroups(pipe_dir, groups, encrypt)



        results = waitResponseFromGroups( pipe_name, groups, word, encrypt)

        print("Results received!")

        print(results)



        #Only for first found

        ele = str(results.values())



        if ele is not None:

            l = ele.split(":")[2]

            if l.strip() == word.strip():

                print("Found word is equal server=" + word + " group=" + l)

                niter += 1



    print("All Done for " + str(niter))

