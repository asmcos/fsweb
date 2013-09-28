Fsweb is a fast simple web framework base on python.
Fsweb from SimpleHTTPServer + uliweb template.

usage:

```
python HTTPServer
```

browser: 127.0.0.1:8000

Test:

```
example/*.pyhtml
```


```
$more example/1.pyhtml 

{{name='fsweb'}}
{{url='http://github.com/asmcos/%s'%name}}

<a href={{=url}}> {{=name}} </a>

```
