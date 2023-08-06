The nfer Language
=============================================================================
The nfer domain specific language (DSL) is a declarative, rule based logic 
for inferring a hierarchy of intervals from an event trace.  What that means
is that you must write rules that specify how new intervals are created from
old ones.

## Intervals

In nfer, everything is an interval.  The event trace that is its input is 
really a trace of intervals where the begin and end times are equal
(sometimes called an atomic interval).  When a new interval is created it
has begin and end timestamps, as well as arbitrary data properties. 
Intervals can have temporal relationships, and data relationship, and those
relationships define new intervals.  Note that intervals don't have to 
have names in all caps, but we use that convention in this document to help 
visually distinguish them from other identifiers.

An interval is defined by its _begin_ and _end_ timestamps.  It may also
contain arbitrary data elements, but we will ignore those for now.  Here is
a table containing six atomic intervals with three names:

| Name | Begin | End |
| ---- | ----- | --- |
| ON   | 10    | 10  |
| TEST | 15    | 15  |
| OFF  | 20    | 20  |
| ON   | 50    | 50  |
| TEST | 55    | 55  |
| OFF  | 65    | 65  |

Under normal circumstances, nfer expects _events_ on STDIN, so this trace
could be sent to nfer by the following shell command, where specfile.nfer is 
the file containing the specification to apply.

```Shell
echo "ON|10
TEST|15
OFF|20
ON|50
TEST|55
OFF|65" | ./nfer specfile.nfer
```

## Rules

Let's look at a simple, example rule:
```
OPERATING :- ON before OFF
```

This rule says that, when an ON interval is seen _before_ an OFF
interval, create an interval named OPERATING with a begin time equal to the
begin time of ON and an end time equal to the end time of OFF.  The
words OPERATING, ON, and OFF and all arbitrary and could be the names
of any intervals, while the word _before_ is a keyword that specifies a
temporal relationship.

If the example rule was applied to the atomic intervals listed above, it would 
result in the creation of two new intervals:

| Name      | Begin | End |
| --------- | ----- | --- |
| OPERATING | 10    | 20  |
| OPERATING | 50    | 65  |

You might have noticed that one interval appears to be missing!  The tool has
omitted the interval beginning at 10 and ending at 65.  The reason for this is
that nfer, by default, only creates _minimal_ intervals.  A minimal interval
is one where no interval with the same name occurs _during_ that interval. The 
OPERATING interval that begins at 10 and ends at 65 has two other intervals
with the same name that occur during that time span, so the longer interval
is omitted.  If you want to include all intervals regardless of minimality, 
you can use the --full option.

Another thing to note is that the TEST intervals have no effect on this rule.
Rules are only affected by the intervals they specify, so other intervals
are ignored.

## Temporal relations (inclusive)

Here are all of the available temporal relations, and the _begin_ and _end_
timestamps that they specify for the resulting interval:

| Relation     | Matches                              | Resulting Begin       | Resulting End     |
| ------------ | ------------------------------------ | --------------------- | ----------------- |
| A before B   | A.end < B.begin                      | A.begin               | B.end             |
| A meet   B   | A.end = B.begin                      | A.begin               | B.end             |
| A during B   | A.begin >= B.begin && A.end <= B.end | B.begin               | B.end             |
| A coincide B | A.begin = B.begin && A.end = B.end   | A.begin               | B.end             |
| A start B    | A.begin = B.begin                    | A.begin               | max(A.end, B.end) |
| A finish B   | A.end = B.end                        | min(A.begin, B.begin) | B.end             |
| A overlap B  | A.begin < B.end && B.begin < A.end   | min(A.begin, B.begin) | max(A.end, B.end) |
| A slice B    | A.begin < B.end && B.begin < A.end   | max(A.begin, B.begin) | min(A.end, B.end) |
| A also B     | Any pair of A and B                  | Must be specified     | Must be specified |

One thing to notice is that _before_ is really the only useful relation
for relating two atomic intervals (events), so most of the time your 
specifications will begin by creating intervals using _before_ relations.
Another thing to notice is that the _also_ relation is special, in that
it places no constraints on the temporal relationship.  When _also_ is
used, you *must* specify manual constraints and end points.

## Manual Constraints

To specify manual constraints, use the _where_ keyword.  The where keyword
specifies an expression that must evaluate to a Boolean (true/false) that
can refer to the end points and properties of the intervals specified
in the temporal relation part of the rule.  Where constraints are applied
_in addition_ to the constraints of the temporal relation, which is why
it is useful to have _also_.  Here is the same rule as before but with an 
extra constraint added.

```
SHORT_OP :- ON before OFF where OFF.begin - ON.end < 12
```

This version of the rule specifies that the difference between the end of
ON and the beginning of OFF should be less than 12.  This would omit
the second interval created before, because this value would be 15.

In an expression, properties and end points are specified by separating the 
interval name to reference and the property name with a dot (.).  What if
we want to reference two intervals with the same name, though?  For this
we can use _labels_, which are specified in the temporal relation and then
referenced in any expression.  Labels can be used in any nfer rule, not 
just in ones that reference two intervals of the same name, and can be 
helpful for keeping rules concise.

```
TWO_CLOSE_OPS :- op1:OPERATING before op2:OPERATING where op2.begin - op1.end < 50
```

## Manual begin and end times

To manually override the begin and end timestamps of the resulting interval
we can use expressions specified using the _begin_ and _end_ keywords.
These expressions must result in a number.  Here is the original OPERATING
rule manually specified using _also_.

```
OPERATING :- ON also OFF where ON.end < OFF.begin begin ON.begin end OFF.end
```

## Expressions

Expressions can be as complex as you want, and should generally behave as 
a programmer would expect.  That is, precedence follows normal convention 
and can be overridden by parentheses.  Constants can be specified as you 
might expect with numbers (both integer and real), Booleans (_true_ or 
_false_), and strings (using double quotation marks) supported.

The following table lists the available operators in expressions:

| Operator      | Binary / Unary | Types Supported         | Meaning                  |
| ------------- | -------------- | ----------------------- | ------------------------ |
| +             | Binary         | int,real                | Add                      |
| -             | Binary         | int,real                | Subtract                 |
| *             | Binary         | int,real                | Multiply                 |
| /             | Binary         | int,real                | Divide                   |
| %             | Binary         | int,real                | Modulo                   |
| -             | Unary          | int,real                | Negate                   |
| >             | Binary         | int,real                | Greater than             |
| <             | Binary         | int,real                | Less than                |
| >=            | Binary         | int,real                | Greater than or equal to |
| <=            | Binary         | int,real                | Less than or equal to    |
| =             | Binary         | int,real,string,Boolean | Equal to                 |
| !=            | Binary         | int,real,string,Boolean | Not equal to             |
| &             | Binary         | Boolean                 | Logical and              |
| <p>&#124;</p> | Binary         | Boolean                 | Logical or               |
| !             | Unary          | Boolean                 | Logical not              |

## Data maps

So far, we have mentioned that intervals can have arbitrary properties, 
but none have been shown in examples.  These arbitrary properties take 
the form of _maps_ which are associated with any interval where the keys
of the map are string identifiers and the values are of any type.
Events that are sent as inputs may have data maps associated with them, 
and keys can be set on any newly created interval.

To specify maps for input events, keys are listed first and then values,
where each member of the list of keys or values is separated by a
semicolon.  Let's add some properties to our example atomic intervals:

| Name | Begin | End | pid | comment  | success |
| ---- | ----- | --- | --- | -------- | ------- |
| ON   | 10    | 10  | 1   | starting |         |
| TEST | 15    | 15  | 1   |          | true    |
| OFF  | 20    | 20  | 1   | stopping |         |
| ON   | 50    | 50  | 2   | starting |         |
| TEST | 55    | 55  | 2   |          | false   |
| OFF  | 65    | 65  | 2   | stopping |         |

Notice that different events can have different keys set, which is why 
a CSV isn't necessarily the best way to input the data.  Here is how
it would be represented as a shell command, sending the events to nfer.

```Shell
echo "ON|10|pid;comment|1;starting
TEST|15|pid;success|1;true
OFF|20|pid;comment|1;stopping
ON|50|pid;comment|2;starting
TEST|55|pid;success|2;false
OFF|65|pid;comment|2;stopping" | ./nfer specfile.nfer
```

Now the nfer rules may refer to those properties in expressions.

```
OPERATING :- ON before OFF where ON.pid = OFF.pid
```

The new intervals that are created have no data maps set by default, 
so you must specify any keys that you want to set on a new interval
using the _map_ keyword.  Map expects a list of keys and associated
expressions contained within curly braces ({}).

```
OPERATING :- ON before OFF where ON.pid = OFF.pid map { proc -> ON.pid, comment -> "running" }
```

Note that the order of the different clauses of a rule matters, and 
nfer expects you to specify the map _after_ the where constraints and
before the manual end points.  This example illustrates that the map
key you specify doesn't have to have anything to do with where the data
comes from.

## Nested rules

As we have mentioned but not demonstrated, rules may refer to intervals
created by nfer as well as those from input events.  Here is an example
where we create intervals and then use them in another rule.

```
OPERATING :- ON before OFF where ON.pid = OFF.pid map { proc -> ON.pid }
TESTING :- TEST during OPERATING where TEST.pid = OPERATING.proc
```

When applied to the above inputs (with data maps) we would get the 
following resulting intervals:

| Name      | Begin | End | proc |
| --------- | ----- | --- | ---- |
| OPERATING | 10    | 20  | 1    |
| TESTING   | 10    | 20  |      |
| OPERATING | 50    | 65  | 2    |
| TESTING   | 50    | 65  |      |

Suppose, however, that we don't actually care about the OPERATING 
intervals where no TEST event is present.  Our output would still
contain them, and this seems messy.  We can supress them by 
combining the two rules into one, _nested_ rule.  To do this, 
we simply combine temporal relations.  Note that nested temporal
relations *must* be surrounded by parentheses, as there is no
natural precedence.

```
TESTING :- TEST during (ON before OFF) where TEST.pid = ON.pid & ON.pid = OFF.pid
```

With this rule instead of the two listed before, we will only see
the TESTING intervals in the output.

## Atomic rules

All the examples so far have related two or more intervals using 
binary temporal relations, but it is possible to refer to only a 
single interval in a rule.  This is mostly useful for renaming an 
interval to something more meaningful, or to merge intervals into
a single namespace.

We call these rules _atomic rules_, and all the normal parts of a rule
can be specified, just like if there was a temporal relation.  By
default, the created interval will have the same begin and end 
times as the original interval, but map keys won't be copied unless
you specify them.

```
STARTING :- ON  map { pid -> ON.pid  }
ENDING   :- OFF map { pid -> OFF.pid }
SUCCESS  :- TEST where TEST.success
```

## Exclusive rules

Sometimes it is necessary to specify what should happen when an interval
is _missing_.  This is not possible with the rules we have described
so far, since they all require that the referenced interval be present.
These rules are called _exclusive rules_ and there are several restrictions
on how they can be used.  (The previously discussed rules are sometimes
called _inclusive_ rules.)

Here is an example exclusive rule that matches when an OPERATING interval
does not contain a TEST interval.

```
FAILURE :- OPERATING unless contain SUCCESS
```

Exclusive rules are specified using the _unless_ keyword and have their 
own temporal relations.

| Relation           | Matches                                                                        |
| ------------------ | ------------------------------------------------------------------------------ |
| A unless after B   | A where there does not exist a B such that A.begin > B.end                     |
| A unless follow B  | A where there does not exist a B such that A.begin = B.end                     |
| A unless contain B | A where there does not exist a B such that A.begin <= B.begin && A.end > B.end |

The begin and end times of the created interval are the same as the matched
interval by default, but can be overridden as in any rule.  The only 
restriction is that you cannot (not a bug!) refer to excluded intervals
in map or end point expressions, since that interval does not exist!

## Modules

Often, nfer specifications will start out fairly simply, just containing
a handful of rules.  In this case, it makes sense to simply put all
rules into a file with no real structure.  However, having a flat 
scheme with all rules at the same level can become cumbersome once
a specification gets too big.  To alleviate this, nfer supports
modules.

To declare rules in a module, simply surround the rules by a module
declaration.  Files can have arbitrary numbers of modules and nfer
will only load the rules from the first module in the specification 
file.  To use rules from other modules, include the names of those
modules in an _import_ declaration at the beginning of a loaded
module.

```
module test_module {
  import two_tests;

  TESTING :- TEST during (ON before OFF) where TEST.pid = ON.pid & ON.pid = OFF.pid
}

module two_tests {
  TWOTESTS :- t1:TESTING before t2:TESTING where t2.begin - t1.end < 50
}
```

