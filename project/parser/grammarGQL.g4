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
    | set_start
    | set_final
    | add_start
    | add_final
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
    | smb
    ;

intersect:  '&&';
concat: '..';
union:  '||';
star:   '(' expr ')**';
smb:    '(step' expr ')';

set_start: 'set start of (' expr ') to' var;
set_final: 'set final of (' expr ') to' var;
add_start: 'add start of (' expr ') to' var;
add_final: 'add final of (' expr ') to' var;

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


lambdasys: 'fun (' var ') ->' listops;
listops
    : op ';' listops
    | op
    ;

op
    : var 'in' expr
    | var '*' var
    | var '+' var
    | var
    ;

NEWLINE     : [\r\n]+ ;
INT         : [0-9]+ ;
IDENTIFIER  : 'I' [A-Za-z0-9]+ ;
STRING      : '\'' ~('\'')+ '\'';
WS          :   [ \t\r\n]+ -> skip;
