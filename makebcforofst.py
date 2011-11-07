#!/usr/bin/env python

import os, glob, sys

enumspath = "enumstemplate.txt"
enums = {}
def readenums():
    for line in open(enumspath):
      fs = line.strip().split()
      if len(fs) == 0:
        continue
      #prinat fs[1:]
      if fs[0] not in enums:
        enums[fs[0]] = []
      enums[fs[0]].append(fs[1:])
    print >> sys.stderr, enums


header = """
#1    2   3    4     5
#name cur prev pprev options
_completeenumerable ()
{
  if [[ $2 == = || $3 == = ]] ; then
    if [[ $3 == *$1 ]] ; then
      COMPREPLY=($(compgen -W "$5" -- ))
      return 0
    fi
    if [[ $4 == *$1 ]] ; then
      COMPREPLY=($(compgen -W "$5" -- $2))
      return 0
    fi
  fi
}
"""

cmd = """_CMD() 
{
    local cur prev opts filters len pprev
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    if (( $COMP_CWORD > 2)) ; then
      pprev="${COMP_WORDS[COMP_CWORD-2]}"
    else
      pprev="NULL"
    fi

    opts="OPTS"

    $ENUMS

    if [[ ${cur} == -* ]] ; then
    COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
    return 0
    fi
}
complete -o default -o nospace -F _CMD CMD"""

def getname(line):
  return line.split("(")[1].split(",")[0]

#print header


if __name__ == "__main__":
    readenums()
    for i in range(1, len(sys.argv)):
        binpath = sys.argv[i]
        for infile in glob.glob(os.path.join(binpath, '*.cc')):
            opts = ""
            base, ext = os.path.splitext(os.path.basename(infile))    
            print >> sys.stderr, "current file is: " + infile
            e = ""
            for line in open(infile):
              if "DEFINE_bool" in line:
                name = getname(line)
                opts = opts + "--" + name + " "
              elif "DEFINE" in line:
                name = getname(line)
                opts = opts + "--" + name + "= "
            if base in enums:
              for f in enums[base]:
                s ="_completeenumerable " + f[0] + " ${cur} ${prev} ${pprev} \""
                for g in f[1:]:
                  s = s + g +" "
                e = e + s.strip() + "\"\n    "
                #print >> sys.stderr, s
            #print  >> sys.stderr, e
            #print opts
            if len(opts) > 0:      
              ncmd  = cmd.replace("OPTS",opts).replace("CMD",base).replace("$ENUMS",e)
              print ncmd
              print ""
              print >> sys.stderr, "adding", base
            else:
              print >> sys.stderr, "ignoring", base
            

