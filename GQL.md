## Описание абстрактного синтаксиса языка

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | // а здесь пространство для творчества
  | FinA of rsm                  // Для того, чтобы пересекать запросы c графам
  | CFG of cfg                   // Для хранения именно КС грамматики (вообще запрос просто строка, но для реализации может быть польезно именно кс,
                                 // хотя надо явно указывать, что запрос именно кс)

var = 
    Val of val
  | Name of string
  | NameAddresed of string * Set<int>
  | Tuple of tuple

tuple =
    LoneElem of var
    LoneTup of tuple
    Pipe of tuple * tuple

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход                           **пока нет яеткого функционала**

lambda =
    // а здесь пространство для творчества
    declFunct = Method of var * listops  //currentValue

listops =
      Pipe of op * listops
    | Emptylst

op = 
      Contains of val * Set<val>   // value in [1, 2, 3]
    | Var of var                   // value
    | Mult of var * var            // value1 * value2
    | Plus of var * var            // value1 + value2
```

## Конкретный синтаксис
```
prog -> stm | stm "\n" prog

stmt -> "let" var "=" expr
stmt -> "print" expr

var -> lexem | lexem addr
addr -> "[" int "]" | "[" int "]" addr 

val -> int | string

SetVal -> "{" SetElem "}"
SetElem -> epsilon | val "," SetElem

expr -> Var | Val | Set_start | Set_final | Add_start | Add_final | Get_start | Get_final | Get_reachable | Get_vertices | Get_edges | Get_labels | Map |Filter | Load | Intersect | Concat | Union | Star | Smb

Var -> var
Val -> val
Set_start -> "set start of (" expr ") to " var
Set_final -> "set final of (" expr ") to " var
Add_start -> "add start of (" expr ") to " var
Add_final -> "add final of (" expr ") to " var
Get_start -> "get starts of (" expr ")"
Get_final -> "get finals of (" expr ")"
Get_reachable -> "get reachable of (" expr ")"
Get_vertices -> "get vertices of (" expr ")"
Get_edges -> "get edges of (" expr ")"
Get_labels -> "get labels of (" expr ")"
Map -> "map(" lamda ")(" expr ")"
Filter -> "filter(" lamda ")(" expr ")"
Load ->   "load graph from" \'path\'
        | "load graph" \'path\'
Intersect -> expr "&&" expr
Concat -> expr ".." expr
Union -> expr "||" expr
Star -> "(" expr ")**"
Smb -> "(step" expr ")"

lambda -> "fun ( " var ") -> " listops

listops -> op "; " listops | op ";" 

op -> var " in " expr | var | var " * " var | var " + " var
```

## Скрипт
```
let g1 = load graph 'wine'                // загрузка графа
let g1 = load graph from 'home/wine.dot'  // загрузка графа из файла

let g = set start of (set finals of (g1) to (get vertices of (g1) )) to {0, 1, 2, 3,} 
// все вершины стартовые и финальные

let l1 = "l1" || "l2" // создание запроса (или)

let query1 = ("type" || l1)** // создание запроса (или + звезда клини)
let query2 = "sub_class_of" .. l1 // создание запроса (конкатенация)

let res1 = g && query1  // выполнение запроса 1
let res2 = g && query2  // выполнение запроса 2

print res1  // печать рещультата (всего объекта)

let s = get starts of (g) // получение стартовых вершин

let vertices1 = filter (fun (v) -> v in s)(map (fun (edge) -> edge[0])(get edges of (res1) ))
//получение только вершин, которые стартовые и являются началами некоторых путей

let vertices2 = filter (fun (v) -> v in s)(map (fun (edge) -> edge[0])(get edges of (res2) ))
//получение только вершин, которые стартовые и являются началами некоторых путей

let vertices = vertices1 && vertices2 // общие вершины обоих запросов

print vertices // вывод сета общих вершин
```

## Правила вывода типов

Константы типизируются очевидным образом.

Тип переменной определяется типом выражения, с которым она связана.
```
[b(v)] => t
_________________
[Var (v)](b) => t
```

Загрузить можно только автомат.
```
_________________________
[Load (p)](b) => FA<int>
```

Установка финальных состояний, а так же добавление стартовых и финальных типизируется аналогично типизации установки стартовых, которая приведена ниже.
```
[s](b) => Set<t> ;  [e](b) => FA<t>
___________________________________
[Set_start (s, e)](b) => FA<t>


[s](b) => Set<t> ;  [e](b) => RSM<t>
____________________________________
[Set_start (s, e)](b) => RSM<t>

```

Получение финальных типизируется аналогично получению стартовых, правила для которого приведены ниже.
```
[e](b) => FA<t>
____________________________
[Get_start (e)](b) => Set<t>


[e](b) => RSM<t>
____________________________
[Get_start (e)](b) => RSM<t>

```

```
[e](b) => FA<t>
__________________________________
[Get_reachable (e)](b) => Set<t*t>


[e](b) => RSM<t>
__________________________________
[Get_reachable (e)](b) => Set<t*t>

```

```
[e](b) => FA<t>
_______________________________
[Get_vertices (e)](b) => Set<t>


[e](b) => RSM<t>
_______________________________
[Get_vertices (e)](b) => Set<t>


[e](b) => FA<t>
______________________________________
[Get_edges (e)](b) => Set<t*string*t>


[e](b) => RSM<t>
______________________________________
[Get_edges (e)](b) => Set<t*string*t>

[e](b) => FA<t>
__________________________________
[Get_labels (e)](b) => Set<string>


[e](b) => RSM<t>
__________________________________
[Get_labels (e)](b) => Set<string>

```

Правила для ```map``` и ```filter``` традиционные.
```
[f](b) => t1 -> t2 ; [q](b) => Set<t1>
_______________________________________
[Map (f,q)](b) => Set<t2>


[f](b) => t1 -> bool ; [q](b) => Set<t1>
________________________________________
[Filter (f,q)](b) => Set<t1>
```

Пересечение для двух КС не определено.
```
[e1](b) => FA<t1> ;  [e2](b) => FA<t2>
______________________________________
[Intersect (e1, e2)](b) => FA<t1*t2>


[e1](b) => FA<t1> ;  [e2](b) => RSM<t2>
_______________________________________
[Intersect (e1, e2)](b) => RSM<t1*t2>


[e1](b) => RSM<t1> ;  [e2](b) => FA<t2>
_______________________________________
[Intersect (e1, e2)](b) => RSM<t1*t2>

```

Остальные операции над автоматами типизируются согласно формальных свойств классов языков.
```
[e1](b) => FA<t> ;  [e2](b) => FA<t>
_____________________________________
[Concat (e1, e2)](b) => FA<t>


[e1](b) => FA<t> ;  [e2](b) => RSM<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => FA<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => RSM<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>

```

```
[e1](b) => FA<t> ;  [e2](b) => FA<t>
______________________________________
[Union (e1, e2)](b) => FA<t>


[e1](b) => FA<t> ;  [e2](b) => RSM<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => FA<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => RSM<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>

```

```
[e](b) => FA<t>
______________________
[Star (e)](b) => FA<t>


[e](b) => RSM<t>
______________________
[Star (e](b) => RSM<t>

```

```
[e](b) => string
________________________
[Smb (e)](b) => FA<int>

```


## Динамическая семантика языка запросов

Связывание переопределяет имя.

```
[e](b1) => x,b2
_____________________________________
[Bind (v, e)](b1) => (), (b1(v) <= x)

```

Загрузить можно только автомат и у него все вершины будут стартовыми и финальными.

```
[p](b1) => s,b2 ; read_fa_from_file s => fa
_____________________________________
[Load (p)](b1) => (fa | fa.start = fa.vertices, fa.final = fa.vertices), b1

```
