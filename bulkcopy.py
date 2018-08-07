# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 23:08:29 2018

@author: dilshad
"""

import os, random, time, subprocess

#os.system("rmdir dest /S /Q")
#os.system("mkdir dest")

os.system("chcp 65001")

src = "E:\\bulkCopy\\src"
dest = "E:\\bulkCopy\\dest"
maxthread = 8
maxsize = 100*1000*1000 #100 MB

def get_size(start_path = src):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    else:
        total_size = os.path.getsize(start_path)
    return total_size

print(get_size())

def copyfile(srcfile,destfile):
    action = False
    srcfilesize = get_size(start_path = srcfile)
    destfilesize = -1
    if os.path.exists(destfile):       
        destfilesize = get_size(start_path = destfile)
        if srcfilesize != destfilesize:
            action = True
    else:
        action = True
    if os.path.exists('stp'):
        action = False
#    print(srcfilesize,destfilesize, action,'\n')
#    print(srcfile,destfile, action,'\n')
    
    return action, srcfilesize
#Get number of live threads
global threadlist, live
def livethreads(threadlist,src,dest):
    nthreads = 0
#    newthread = []   
    for thread in threadlist:
        batfile=thread+'.bat'
        batex=os.path.exists(batfile)
        if batex: #Live thread
            nthreads += 1
    return nthreads
       
#        src7z=thread+'.7z'
#        dest7z=thread.replace(src,dest)+'.7z'
#        batex=os.path.exists(batfile)
#        src7zex=os.path.exists(src7z)
#        dest7zex=os.path.exists(dest7z)
#        donefile=thread+'.done'
#        doneex=os.path.exists(donefile)
#        if batex and (src7zex or dest7zex): #Live thread
#            nthreads += 1
#            newthread.append(thread)
##            print(batfile,batex,src7z,src7zex, dest7z, dest7zex)
#            print('live thread',thread,'\n')
#        elif batex and not (src7zex or dest7zex): # dead thread
##            os.system('del '+batfile)
##            os.system('del '+donefile)
##                live.pop(thread)
##            print(batfile,batex,src7z,src7zex, dest7z, dest7zex)
#            print('dead thread', thread, '\n')
#             
#        threadlist = newthread

#function to create bat file
def makebat(srcdirpath,batname,filelist,destdirpath):
    batfile=batname+'.bat'
    tex='''echo hi
chcp 65001

{}

cd "{}"

"c:\\Program Files\\7-Zip\\7z.exe" a -t7z -mx=9 -m0=LZMA2 -mmt2 {}.7z {}

robocopy {} {} {}.7z /MOV /MT:4

"c:\\Program Files\\7-Zip\\7z.exe" e -y -mmt2 "{}.7z" -o"{}"

del {}\\{}.7z

echo Finished job, deleting bat file

start /b " " cmd /C del "%~f0"&exit
'''
    text=tex.format(srcdirpath[0:2],srcdirpath,batname,filelist,srcdirpath,destdirpath,
                    batname,destdirpath+'\\'+batname,destdirpath,
                    destdirpath,batname)
    
    fh=open(srcdirpath+'\\'+batfile, 'w', encoding='utf-8')
    fh.write(text)
   
# Create folder structure at the destination
os.system("robocopy {} {}  /e /xf *".format(src,dest))

#def bulkcopy(source_path=src, counter=1):
threadlist=[]
for srcdirpath, srcdirnames, srcfilenames in os.walk(src):
    if os.path.exists('stp'): break
         
    copylist=[]
    sizemeter=0
    destdirpath=srcdirpath.replace(src,dest)
    time.sleep(0.1) #give some time to create bat files    
    for srcfilename in srcfilenames:
        srcfile = srcdirpath +'\\'+srcfilename
        destfile= destdirpath +'\\'+srcfilename
        
        [action, srcfilesize]=copyfile(srcfile,destfile)
        if action:                
            if sizemeter < maxsize:
                sizemeter +=srcfilesize
                copylist.append('"'+srcfilename+'"')
            else:
                #print(sizemeter, copylist)
    
                batname=str(random.randint(10,99))
                makebat(srcdirpath,batname, ' '.join(copylist),destdirpath)
                sizemeter = 0
                copylist=['"'+srcfilename+'"']
                #print(srcdirpath)

                #os.system('start a.bat')
                threadlist.append(srcdirpath+'\\'+batname)
                print('start '+srcdirpath+'\\'+batname+'.bat')
                print('Threads: ',livethreads(threadlist,src,dest))
                while livethreads(threadlist,src,dest) > maxthread -1:
                    print(' Live threads ',livethreads(threadlist,src,dest), '> '+str(maxthread-1)+' waiting')
                    time.sleep(1.0)
#                proc = subprocess.Popen([srcdirpath+'\\'+batname+'.bat'], 
#                             stdout=subprocess.PIPE, 
#                             stderr=subprocess.STDOUT)
#                print(proc.pid)
                time.sleep(1.0)
                os.system('start '+srcdirpath+'\\'+batname+'.bat')

#            subp=Popen(batname+'.bat',cwd=srcdirpath, shell=True, start_new_session=True)
#            subp.communicate()
    else:
        if action and sizemeter > 0:               
            batname=str(random.randint(10,99))
            makebat(srcdirpath,batname, ' '.join(copylist),destdirpath)
            #os.system('start a.bat')
            #print('start '+srcdirpath+'\\'+batname+'.bat')
            
            threadlist.append(srcdirpath+'\\'+batname)
            print('start '+srcdirpath+'\\'+batname+'.bat')
            print('Threads: ',livethreads(threadlist,src,dest))
            while livethreads(threadlist,src,dest)> maxthread -1:
                print(' Live threads ',livethreads(threadlist,src,dest), '> '+str(maxthread-1)+' waiting')
                time.sleep(1.0)
#            proc = subprocess.Popen([srcdirpath+'\\'+batname+'.bat'], 
#                        stdout=subprocess.PIPE, 
#                        stderr=subprocess.STDOUT)
#            print(proc.pid)
            time.sleep(1.0)
            os.system('start '+srcdirpath+'\\'+batname+'.bat')
                               
                #        print(action,srcfilesize)
        
#        srcfilesize.append(get_size(start_path = srcdirpath+'\\'+srcfile))
    
    print(srcdirpath,srcdirnames,srcfilenames,'\n\n')
    
#"c:\Program Files\7-Zip\7z.exe" a -t7z 1.7z TheFeetInSalahASalafiError.pdf TABAQAAT_E_IBN_E_SAAD_VOL_1.pdf
#
#robocopy src\islamicbookslibrary\2010-09\ dest\islamicbookslibrary\2010-09\ 1.7z /MT:4
#
#c:\Program Files\7-Zip\7z.exe" e dest\islamicbookslibrary\2010-09\1.7z -odest\islamicbookslibrary\2010-09\
##    
#for destdirpath, destdirnames, destfilenames in os.walk(dest):
#    destfilesize=[]
#    for destfile in destfilenames:
#        destfilesize.append(get_size(start_path = destdirpath+'\\'+destfile))
#    print(destdirpath,'\n',destfilenames,destfilesize)
#
#    
#    for file in filenames:
#        

#        size=get_size(start_path =dirpath)
#bulkcopy(source_path=src)