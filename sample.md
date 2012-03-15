# Sample Document

Here is a line
Here's another line in the same paragraph.

## Code

This is a fenced codeblock:

```js
var foo;
function bar() { console.log("Hello, world!"); }
```

Or something better:

```python
#!/usr/bin/env python

from redtape import script

def main():
    script.main()

if __name__ == '__main__':
    main()
```

We can highlight it in a number of ways.

<span style="display: block;" class="alert alert-info">We can even include HTML markup, since markdown allows it!  This has the added
benefit of working quite well and being pretty awesome.  As you can see, we can
use all of twitter bootstrap's classes in here. Fortunately, [links](http://twitter.com) work 
inside spans, so use spans with `style="display: block;"` to have markdown 
syntax inside block elements.
</span>

Unfortunately, while we're inside other markup, simple markdown stuff like [a link](http://google.com) won't function.  Would be nice if it did though.
