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

Main : function (s,) {
enter_rule ("Main");
    set_return (`${s.rwr ()}`);
return exit_rule ("Main");
},
Statement : function (_print,s,) {
enter_rule ("Statement");
    set_return (`print ${s.rwr ()}`);
return exit_rule ("Statement");
},
str1ng_recursive : function (_dollar,lb,s1,rb,s2,) {
enter_rule ("str1ng_recursive");
    set_return (`strcat (${s1.rwr ()}, ${s2.rwr ().join ('')})`);
return exit_rule ("str1ng_recursive");
},
str1ng_other : function (c,s,) {
enter_rule ("str1ng_other");
    set_return (`${c.rwr ()}${s.rwr ().join ('')}`);
return exit_rule ("str1ng_other");
},
_terminal: function () { return this.sourceString; },
_iter: function (...children) { return children.map(c => c.rwr ()); }
}
