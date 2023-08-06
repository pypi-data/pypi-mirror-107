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

dyn.load("bin/nfer-R.so")
Rnfer <- function(specfile, logfile="nfer-R.log", loglevel=1) {
  stopifnot(class(specfile) == "character")
  stopifnot(class(logfile) == "character")
  stopifnot(class(loglevel) == "numeric")
  .Call("R_nfer", specfile, logfile, loglevel)  
}
RnferLearn <- function(events, logfile="nfer-R.log", loglevel=1) {
  # transform to char from factor
  f <- sapply(events, is.factor)
  events[f] <- lapply(events[f], as.character)

  # input validation
  stopifnot(length(events) == 2)
  stopifnot(sapply(events, class)[1] == "character")
  stopifnot(sapply(events, class)[2] == "numeric")
  stopifnot(class(logfile) == "character")
  stopifnot(class(loglevel) == "numeric")
  .Call("R_nfer_learn", events, logfile, loglevel)
}
RnferApply <- function(handle, events) {
  # transform to char from factor
  f <- sapply(events, is.factor)
  events[f] <- lapply(events[f], as.character)

  # input validation
  stopifnot(length(handle) == 2)
  stopifnot(sapply(handle, class)[1] == "character")
  stopifnot(sapply(handle, class)[2] == "integer")
  stopifnot(length(events) == 2)
  stopifnot(sapply(events, class)[1] == "character")
  stopifnot(sapply(events, class)[2] == "numeric")

  .Call("R_nfer_apply", handle, events)
}
factor2char <- function(events) {
  f <- sapply(events, is.factor)
  events[f] <- lapply(events[f], as.character)
  events
}
