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
    set_return (`${s.rwr ().join ('')}`);
return exit_rule ("main");
},
statement : function (_print,ws1,_dqleft,s,_dqright,ws2,) {
enter_rule ("statement");
    set_return (`${_print.rwr ()}${ws1.rwr ().join ('')}${_dqleft.rwr ()}${s.rwr ()}${_dqright.rwr ()}${ws2.rwr ()}`);
return exit_rule ("statement");
},
str1ng_basicPair : function (s1,s2,) {
enter_rule ("str1ng_basicPair");
    set_return (`${s1.rwr ()}${s2.rwr ()}`);
return exit_rule ("str1ng_basicPair");
},
str1ng_basic : function (s,) {
enter_rule ("str1ng_basic");
    set_return (`${s.rwr ()}`);
return exit_rule ("str1ng_basic");
},
str1ng_interpolationPair : function (s1,s2,) {
enter_rule ("str1ng_interpolationPair");
    set_return (`${s1.rwr ()}${s2.rwr ()}`);
return exit_rule ("str1ng_interpolationPair");
},
str1ng_finalInterpolation : function (s,) {
enter_rule ("str1ng_finalInterpolation");
    set_return (`${s.rwr ()}`);
return exit_rule ("str1ng_finalInterpolation");
},
basicString : function (cs,) {
enter_rule ("basicString");
    set_return (`${cs.rwr ().join ('')}`);
return exit_rule ("basicString");
},
interpolation : function (_dollar,_lb,s,_rb,) {
enter_rule ("interpolation");
    set_return (`${_dollar.rwr ()}${_lb.rwr ()}${s.rwr ()}${_rb.rwr ()}`);
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
