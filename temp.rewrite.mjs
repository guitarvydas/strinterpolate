let parameters = {};
function pushParameter (name, v) {
    if (!parameters [name]) {
        parameters [name] = [];
    }
    parameters [name].push (v);
}
function popParameter (name) {
    parameters [name].pop ();
}
function getParameter (name) {
    return parameters [name];
}


let _rewrite = {

main : function (s,) {
enter_rule ("main");
    set_return (`
def strcat (s1, s2):
    return s1 + s2
    
${s.rwr ().join ('')}`);
return exit_rule ("main");
},
statement : function (_print,_spc,s,_ws,) {
enter_rule ("statement");
    set_return (`print (${s.rwr ()})${_ws.rwr ()}`);
return exit_rule ("statement");
},
expr_string : function (x,) {
enter_rule ("expr_string");
    set_return (`${x.rwr ()}`);
return exit_rule ("expr_string");
},
expr_iexpr : function (e,) {
enter_rule ("expr_iexpr");
    set_return (`str (${e.rwr ()})`);
return exit_rule ("expr_iexpr");
},
integerExpr_rec : function (i,_plus,e,) {
enter_rule ("integerExpr_rec");
    set_return (`${i.rwr ()} + ${e.rwr ()}`);
return exit_rule ("integerExpr_rec");
},
integerExpr_int : function (i,) {
enter_rule ("integerExpr_int");
    set_return (`${i.rwr ()}`);
return exit_rule ("integerExpr_int");
},
integer : function (ds,) {
enter_rule ("integer");
    set_return (`${ds.rwr ().join ('')}`);
return exit_rule ("integer");
},
string_empty : function (lq,rq,) {
enter_rule ("string_empty");
    set_return (`""`);
return exit_rule ("string_empty");
},
string_withInnards : function (lq,i,rq,) {
enter_rule ("string_withInnards");
    set_return (`${i.rwr ()}`);
return exit_rule ("string_withInnards");
},
innards_charsPair : function (s1,s2,) {
enter_rule ("innards_charsPair");
    set_return (`strcat ("${s1.rwr ()}", ${s2.rwr ()})`);
return exit_rule ("innards_charsPair");
},
innards_chars : function (s,) {
enter_rule ("innards_chars");
    set_return (`"${s.rwr ()}"`);
return exit_rule ("innards_chars");
},
innards_interpolationPair : function (s1,s2,) {
enter_rule ("innards_interpolationPair");
    set_return (`strcat (${s1.rwr ()}, ${s2.rwr ()})`);
return exit_rule ("innards_interpolationPair");
},
innards_interpolation : function (s,) {
enter_rule ("innards_interpolation");
    set_return (`${s.rwr ()}`);
return exit_rule ("innards_interpolation");
},
rawChars : function (cs,) {
enter_rule ("rawChars");
    set_return (`${cs.rwr ().join ('')}`);
return exit_rule ("rawChars");
},
interpolation : function (_dollar,_lb,e,rb,) {
enter_rule ("interpolation");
    set_return (`${e.rwr ()}`);
return exit_rule ("interpolation");
},
notSpecial : function (c,) {
enter_rule ("notSpecial");
    set_return (`${c.rwr ()}`);
return exit_rule ("notSpecial");
},
_terminal: function () { return this.sourceString; },
_iter: function (...children) { return children.map(c => c.rwr ()); }
}
