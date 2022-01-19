grammar grammarGQL;


prog: ((stm NEWLINE)* EOF);


stm
    : 'let' var '=' expr
    | 'print' expr
    ;

var
    : IDENTIFIER addr
    | IDENTIFIER
    ;

addr
    : '[' INT ']' addr
    | '[' INT ']'
    ;

val:    INT | STRING;

setVal: '{' setElem '}';

setElem
    : val ',' setElem
    |
    ;

expr
    : var
    | val
    | set_start expr ') to' expr
    | set_final expr ') to' expr
    | add_start expr ') to' expr
    | add_final expr ') to' expr
    | get_start
    | get_final
    | get_reachable
    | get_vertices
    | get_edges
    | get_labels
    | mapsys
    | filtersys
    | load
    | expr intersect expr
    | expr concat expr
    | expr union expr
    | star
    | setVal
    ;

intersect:  '&&';
concat: '..';
union:  '||';
star:   '(' expr ')**';

set_start: 'set start of (';
set_final: 'set final of (';
add_start: 'add start of (';
add_final: 'add final of (';

get_start: 'get starts of (' expr ')';
get_final: 'get finals of (' expr ')';
get_reachable: 'get reachable of (' expr ')';
get_vertices: 'get vertices of (' expr ')';
get_edges: 'get edges of (' expr ')';
get_labels: 'get labels of (' expr ')';

mapsys:    'map (' lambdasys ')(' expr ')';
filtersys: 'filter (' lambdasys ')(' expr ')';

load
    : 'load graph from' path
    | 'load graph' path
    ;

path:   STRING;


lambdasys: 'fun (' var ') ->' op;

inop:  'in';
multop: '*';
plusop:  '+';

op
    : var inop expr
    | (var | val) multop (var | val)
    | (var | val) plusop (var | val)
    | (var | val)
    ;

NEWLINE     : [\r\n]+ ;
INT         : [0-9]+ ;
IDENTIFIER  : [A-Za-z0-9]+ ;
STRING      : '\'' ~('\'')+ '\'';
WS          :   [ \t\r\n]+ -> skip;
