Fsweb is a fast simple Python web framework .
Fsweb base on SimpleHTTPServer + uliweb template.
It looks like PHP, ASP.


usage:

```
python HTTPServer
```

browser: http://127.0.0.1:8000

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


Use subdir as root dir.

```
python HTTPServer 8000 -d example
```
