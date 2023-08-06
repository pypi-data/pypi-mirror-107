This test amends a merge commit using various commands, including topics

  $ . $TESTDIR/testlib/common.sh

  $ cat >> $HGRCPATH << EOF
  > [extensions]
  > evolve =
  > topic =
  > EOF

  $ hg init amending-a-merge
  $ cd amending-a-merge

  $ mkcommit root
  $ mkcommit apple
  $ hg up 'desc("root")'
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ mkcommit banana
  created new head
  (consider using topic for lightweight branches. See 'hg help topic')
  $ hg up 'desc("apple")'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge 'desc("banana")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg ci -m merge
  $ hg diff -r 'p1(.)' -r '.'
  diff -r 88a060ab6523 -r c20705a6a8c4 banana
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/banana	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +banana
  $ hg diff -r 'p2(.)' -r '.'
  diff -r d8c7baf0ca58 -r c20705a6a8c4 apple
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/apple	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +apple

amend

  $ hg amend -m 'merge, amend'
  $ hg diff -r 'p1(.)' -r '.'
  diff -r 88a060ab6523 -r 456753fae3cd banana
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/banana	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +banana
  $ hg diff -r 'p2(.)' -r '.'
  diff -r d8c7baf0ca58 -r 456753fae3cd apple
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/apple	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +apple

metaedit

  $ hg metaedit -m 'merge, metaedit'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg diff -r 'p1(.)' -r '.'
  diff -r 88a060ab6523 -r 1528d42f3e83 banana
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/banana	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +banana
  $ hg diff -r 'p2(.)' -r '.'
  diff -r d8c7baf0ca58 -r 1528d42f3e83 apple
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/apple	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +apple

topics

  $ hg topics -r . foo
  switching to topic foo
  changed topic on 1 changesets to "foo"
  $ hg diff -r 'p1(.)' -r '.'
  diff -r 88a060ab6523 -r 52150b9639f7 banana
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/banana	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +banana
  $ hg diff -r 'p2(.)' -r '.'
  diff -r d8c7baf0ca58 -r 52150b9639f7 apple
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/apple	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +apple

  $ hg files
  apple
  banana
  root
  $ hg cat apple banana
  apple
  banana
