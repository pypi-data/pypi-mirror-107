##############################################################################################
#
#       !!!! Do NOT edit this makefile with an editor which replace tabs by spaces !!!!    
#
##############################################################################################
# 
# On command line:
#
# make all = Create project
#
# make clean = Clean project files.
#
# To rebuild project do "make clean" and "make all".
#
#     nfer - a system for inferring abstractions of event streams
#    Copyright (C) 2017  Sean Kauffman
#
#    This file is part of nfer.
#    nfer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##############################################################################################
#

CC	= gcc
XXD	= xxd

# this really should not be necessary, but for some reason Make can't find the executable without this
COVERALLS = $(shell which coveralls)

# Set a default R_HOME variable, but get it from the environment if possible
R_HOME ?= /usr/lib/R

# Define project name here
PROJECT = nfer

# List all user C define here, like -D_DEBUG=1
DEFS = 

SRCDIR = src

BINDIR = bin

# Files that only go in the main binary
# decompress is in the rdc subdirectory
MAIN = main.c \
       compile.c \
       decompress.c

# List C source files here
SRC  = types.c \
       log.c \
       nfer.c \
       dict.c \
       learn.c \
       pool.c \
       file.c \
       map.c \
       analysis.c \
       stack.c \
       expression.c \
       ast.c \
       semantic.c \
       generate.c \
       astutil.c \
       memory.c \
       strings.c \
       debug.c


# List all user directories here
UINCDIR = inc
# List the directory to look for the libraries here
ULIBDIR =

# Lexer and Parser source
LEXER     = dsl.l
PARSER    = dsl.y

TESTSRCDIR = test/src

# List all test source files here
TESTSRC = test.c \
          test_dict.c \
          test_pool.c \
          test_map.c \
          test_stack.c \
          test_nfer.c \
          test_expression.c \
          test_memory.c \
          test_strings.c \
          test_semantic.c
#          test_learn.c


# List the test include directory
TESTINCDIR = test/inc
# List the directory to look for the libraries here
TESTLIBDIR = 
# functional test runner
FTEST = test/run_functional.sh

# List the r source, inc and lib dirs
RSRC    = rinterface.c
RINCDIR = "$(R_HOME)/include"
RLIBDIR = "$(R_HOME)/lib"

# List the source files used for the compiler output
# these files need to be preprocessed to include in the program
COMPILERSRC = types.c \
              memory.c \
              strings.c \
              dict.c \
              map.c \
              stack.c \
              pool.c \
              expression.c \
              nfer.c \
              file.c \
              log.c \
              target/linux.c \
              target/erika.c

COMPILERINC = types.h \
              memory.h \
              strings.h \
              dict.h \
              map.h \
              stack.h \
              pool.h \
              expression.h \
              file.h \
              log.h \
              nfer.h

# goes at the top, doesn't get comments stripped
TARGETINC   = target.h

# target for the headers and source code
HEADERSFILE = headers.h
SRCCODEFILE = srccode.c

# compression routines
RDCSRC     = compress.c \
             decompress.c \
             rdc.c \
             log.c

# List all libraries here
LIBS = 

# Define optimisation levels here -O0 -O1 -O2 -Os -03
OPT      = -O3
TESTOPT  = -O0
ROPT     = -O3
REDISOPT = -O3

# Define the build directories
BUILDDIR   = build
MAINBUILD  = $(BUILDDIR)/main
TESTBUILD  = $(BUILDDIR)/test
RBUILD     = $(BUILDDIR)/R
# for the data compression utility
RDCBUILD   = $(BUILDDIR)/rdc
RDCTARGET  = $(RDCBUILD)/rdc
# Define the directories for code generation
CODEGENDIR = gensrc
PARSBUILD  = $(CODEGENDIR)/parser
COMPBUILD  = $(CODEGENDIR)/compiler

#
# End of user defines
##############################################################################################


INCDIR     = $(patsubst %,-I%,$(UINCDIR) $(PARSBUILD))
TESTINC    = $(patsubst %,-I%,$(TESTINCDIR))
RINC       = $(patsubst %,-I%,$(RINCDIR))

LIBDIR     = $(patsubst %,-L%,$(ULIBDIR))
TESTLIBS   = $(patsubst %,-L%,$(TESTLIBDIR))
RLIBS      = $(patsubst %,-L%,$(RLIBDIR))

OBJS       = $(SRC:.c=.o)
MAINOBJS   = $(MAIN:.c=.o)
TESTOBJS   = $(TESTSRC:.c=.o)
ROBJS      = $(RSRC:.c=.o)
RDCOBJS    = $(RDCSRC:.c=.o)

LEXERSRC   = $(LEXER:.l=.yy.c)
PARSERSRC  = $(PARSER:.y=.tab.c)
LPSRC      = $(patsubst %,$(PARSBUILD)/%,$(PARSERSRC) $(LEXERSRC))
LPOBJS     = $(PARSERSRC:.c=.o) $(LEXERSRC:.c=.o)

SRCCODE    = $(patsubst %,$(COMPBUILD)/%,$(COMPILERSRC))
SRCCODEBLD = $(patsubst %,$(COMPBUILD)/%,$(SRCCODEFILE))
SRCCODESRC = $(SRCCODEBLD:.c=.array.c)
SRCCODEOBJ = $(SRCCODESRC:.c=.o)

HEADERS    = $(patsubst %,$(COMPBUILD)/%,$(COMPILERINC))
HEADERSBLD = $(patsubst %,$(COMPBUILD)/%,$(HEADERSFILE))
HEADERSSRC = $(HEADERSBLD:.h=.array.c)
HEADERSOBJ = $(HEADERSSRC:.c=.o)

MAINO      = $(patsubst %,$(MAINBUILD)/%,$(LPOBJS) $(MAINOBJS) $(OBJS))
TESTO      = $(patsubst %,$(TESTBUILD)/%,$(LPOBJS) $(TESTOBJS) $(OBJS))
RO         = $(patsubst %,$(RBUILD)/%,$(LPOBJS) $(ROBJS) $(OBJS))
RDCO       = $(patsubst %,$(RDCBUILD)/%,$(RDCOBJS))

TARGET     = $(BINDIR)/$(PROJECT)
TESTTARGET = $(BINDIR)/$(PROJECT)-test
RTARGET    = $(BINDIR)/$(PROJECT)-R.so

CPFLAGS = -Wall -Wextra -fomit-frame-pointer -pipe $(DEFS)
LDFLAGS = $(LIBDIR) $(LIBS)

# Generate dependency information
CPFLAGS += -MD -MP -MF .dep/$(@F).d

# Set separate flags for the test binary
TESTCPFLAGS = $(CPFLAGS) -fverbose-asm -no-pie -fprofile-arcs -ftest-coverage

#
# makefile rules
#

.DEFAULT: default
.PHONY: default
default : $(TARGET)

.PHONY: all
all : $(TARGET) $(TESTTARGET) $(RTARGET)

.PHONY: build
build : $(TARGET)

$(MAINBUILD) :
	mkdir -p $(BINDIR)
	mkdir -p $(MAINBUILD)
	
$(TESTBUILD) :
	mkdir -p $(BINDIR)
	mkdir -p $(TESTBUILD)
	
$(RBUILD) :
	mkdir -p $(BINDIR)
	mkdir -p $(RBUILD)

$(PARSBUILD) :
	mkdir -p $(PARSBUILD)

$(COMPBUILD) :
	mkdir -p $(COMPBUILD)
	mkdir -p $(COMPBUILD)/target

$(RDCBUILD) :
	mkdir -p $(RDCBUILD)

.PHONY: test
test : $(TARGET) $(TESTTARGET)
	./$(TESTTARGET)
	./$(FTEST) ./$(TARGET)

.PHONY: coverage
coverage : $(TESTTARGET)
	./$(TESTTARGET)
	$(COVERALLS) --exclude ./test/src --exclude ./build/compiler --exclude ./build/parser --exclude ./src/dsl.l --exclude ./src/dsl.y --gcov-options '\-lp' --build-root ./

# these lines are here to ensure that the build directories exist
$(MAINO)      : | $(MAINBUILD)
$(TESTO)      : | $(TESTBUILD)
$(RO)         : | $(RBUILD)
$(LPSRC)      : | $(PARSBUILD)
$(SRCCODE)    : | $(COMPBUILD)
$(HEADERS)    : | $(COMPBUILD)
$(RDCO)       : | $(RDCBUILD)

# generate the lexer code using flex
$(PARSBUILD)/$(LEXERSRC) : $(SRCDIR)/$(LEXER)
	flex -o $@ $<

# generate the parser code using bison
$(PARSBUILD)/$(PARSERSRC) : $(SRCDIR)/$(PARSER)
	bison -d -o $@ $<

# this uses the rdc program to strip comments and such from source files for use in the compiler
$(COMPBUILD)/%.c : $(SRCDIR)/%.c $(RDCTARGET)
	$(RDCTARGET) s $< $@

# this is also for the compiler, concatenating source files together into one file
$(SRCCODEBLD) : $(SRCCODE)
	cat $^ > $@

# this uses rdc to compress the source and then xxd to generate a C file from the compressed version
$(SRCCODESRC) : $(SRCCODEBLD) $(RDCTARGET)
	$(RDCTARGET) c $< $<.rdc
	$(XXD) -i $<.rdc $@

# this uses the rdc program to strip comments and such from header files for use in the compiler
$(COMPBUILD)/%.h : $(UINCDIR)/%.h $(RDCTARGET)
	$(RDCTARGET) s $< $@

# this is also for the compiler, concatenating header files together into one file
$(HEADERSBLD) : $(UINCDIR)/$(TARGETINC) $(HEADERS)
	cat $^ > $@

# this uses rdc to compress the source and then xxd to generate a C file from the compressed version
$(HEADERSSRC) : $(HEADERSBLD) $(RDCTARGET)
	$(RDCTARGET) c $< $<.rdc
	$(XXD) -i $<.rdc $@

# this is to compile the xxd generated source for the compiler
$(COMPBUILD)/%.o : $(COMPBUILD)/%.c
	$(CC) -c -gdwarf-2 $(CPFLAGS) $< -o $@

# this is to compile the rdc source
$(RDCBUILD)/%.o : $(SRCDIR)/rdc/%.c
	$(CC) -c -gdwarf-2 -I . $(INCDIR) $(CPFLAGS) $< -o $@

# this is to compile the source files rdc needs that are in the top level source directory
$(RDCBUILD)/%.o : $(SRCDIR)/%.c
	$(CC) -c -gdwarf-2 -I . $(INCDIR) $(CPFLAGS) $< -o $@

# this is the main source compilation for the nfer binary
$(MAINBUILD)/%.o : $(SRCDIR)/%.c
	$(CC) -c -gdwarf-2 -DCOMPILER $(CPFLAGS) -I . $(INCDIR) $< -o $@

# this is to compile the rds files for the nfer binary
$(MAINBUILD)/%.o : $(SRCDIR)/rdc/%.c
	$(CC) -c -gdwarf-2 -DCOMPILER $(CPFLAGS) -I . $(INCDIR) $< -o $@

# this is to compile the flex/bison generated source for the nfer binary
$(MAINBUILD)/%.o : $(PARSBUILD)/%.c
	$(CC) -c -gdwarf-2 -DCOMPILER $(CPFLAGS) -Wno-unused-function -I . $(INCDIR) $< -o $@

# this is the main source compilation for the nfer-test unit test binary
$(TESTBUILD)/%.o : $(SRCDIR)/%.c
	$(CC) -c -gdwarf-2 -DTEST $(TESTCPFLAGS) -I . $(INCDIR) $< -o $@

# this is the test source compilation for the nfer-test unit test binary
$(TESTBUILD)/%.o : $(TESTSRCDIR)/%.c
	$(CC) -c -gdwarf-2 -DTEST $(TESTCPFLAGS) -I . $(INCDIR) $(TESTINC) $< -o $@

# this is to compile the flex/bison generated source for the nfer-test unit test binary
$(TESTBUILD)/%.o : $(PARSBUILD)/%.c
	$(CC) -c -gdwarf-2 -DTEST $(TESTCPFLAGS) -Wno-unused-function -I . $(INCDIR) $< -o $@

# this is to build the main source for the R language library
$(RBUILD)/%.o : $(SRCDIR)/%.c
	$(CC) -c $(CPFLAGS) -I . $(INCDIR) $< -o $@

# this is to build the flex/bison generated source for the R language library
$(RBUILD)/%.o : $(PARSBUILD)/%.c
	$(CC) -c $(CPFLAGS) -Wno-unused-function -I . $(INCDIR) $< -o $@

$(TARGET) : CPFLAGS += $(OPT)
$(TARGET) : $(MAINO) $(SRCCODEOBJ) $(HEADERSOBJ)
	$(CC) $^ $(LDFLAGS) -o $@

$(TESTTARGET) : CPFLAGS += $(TESTOPT)
$(TESTTARGET) : $(TESTO)
	$(CC) $^ $(LDFLAGS) $(TESTLIBS) -lgcov --coverage -o $@

$(RTARGET) : CPFLAGS += -fpic $(ROPT)
$(RTARGET) : INCDIR += $(RINC)
$(RTARGET) : $(RO)
	$(CC) -shared $^ $(LDFLAGS) $(RLIBS) -lR -o $@

$(RDCTARGET) : CPFLAGS += $(OPT)
$(RDCTARGET) : $(RDCO)
	$(CC) $^ $(LDFLAGS) -o $@

.PHONY: clean
clean:
	-rm -rf $(BUILDDIR)
	-rm -rf $(CODEGENDIR)
	-rm -rf $(BINDIR)
	-rm -f *.dot
	-rm -fR .dep
	# remove artifacts from python builds too
	-rm -rf NferModule.egg-info
	-rm -rf dist
	-rm -rf wheelhouse

# 
# Include the dependency files, should be the last of the makefile
#
-include $(shell mkdir .dep 2>/dev/null) $(wildcard .dep/*)

# *** EOF ***