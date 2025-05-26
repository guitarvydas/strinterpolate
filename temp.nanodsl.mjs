'use strict'

import * as ohm from 'ohm-js';

let verbose = false;

function top (stack) { let v = stack.pop (); stack.push (v); return v; }

function set_top (stack, v) { stack.pop (); stack.push (v); return v; }

let return_value_stack = [];
let rule_name_stack = [];
let depth_prefix = ' ';

function enter_rule (name) {
    if (verbose) {
	console.error (depth_prefix, ["enter", name]);
	depth_prefix += ' ';
    }
    return_value_stack.push ("");
    rule_name_stack.push (name);
}

function set_return (v) {
    set_top (return_value_stack, v);
}

function exit_rule (name) {
    if (verbose) {
	depth_prefix = depth_prefix.substr (1);
	console.error (depth_prefix, ["exit", name]);
    }
    rule_name_stack.pop ();
    return return_value_stack.pop ()
}

const grammar = String.raw`
strint {
  main = statement+
  statement =
    | "print" space+ expr spaces
  expr =
    | string -- string
    | digit+ -- integer
  string = 
    | "\"" "\"" -- empty
    | "\"" innards "\"" -- withInnards
  innards =
    | rawChars innards      -- charsPair
    | rawChars              -- chars
    | interpolation innards -- interpolationPair
    | interpolation         -- interpolation
  interpolation = "$" "{" expr "}"
  rawChars = notSpecial+
  notSpecial = ~("$" "{") ~"}" ~"\"" any
}

`;

let args = {};
function resetArgs () {
    args = {};
}
function memoArg (name, accessorString) {
    args [name] = accessorString;
};
function fetchArg (name) {
    return args [name];
}

// empty
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
expr_integer : function (ds,) {
enter_rule ("expr_integer");
    set_return (`str (${ds.rwr ().join ('')})`);
return exit_rule ("expr_integer");
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
import * as fs from 'fs';

function grammarname (s) {
    let n = s.search (/{/);
    return s.substr (0, n).replaceAll (/\n/g,'').trim ();
}

try {
    const argv = process.argv.slice(2);
    let srcFilename = argv[0];
    if ('-' == srcFilename) { srcFilename = 0 }
    let src = fs.readFileSync(srcFilename, 'utf-8');
    try {
	let parser = ohm.grammar (grammar);
	let cst = parser.match (src);
	if (cst.failed ()) {
	    //throw Error (`${cst.message}\ngrammar=${grammarname (grammar)}\nsrc=\n${src}`);
	    throw Error (cst.message);
	}
	let sem = parser.createSemantics ();
	sem.addOperation ('rwr', _rewrite);
	console.log (sem (cst).rwr ());
	process.exit (0);
    } catch (e) {
	//console.error (`${e}\nargv=${argv}\ngrammar=${grammarname (grammar)}\src=\n${src}`);
	console.error (`${e}\n\ngrammar = "${grammarname (grammar)}"`);
	process.exit (1);
    }
} catch (e) {
    console.error (`${e}\n\ngrammar = "${grammarname (grammar)}`);
    process.exit (1);
}

