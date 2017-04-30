/**
 * @license
 * Visual Blocks Language
 *
 * Copyright 2012 Google Inc.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


'use strict';

goog.provide('Blockly.tuby.procedures');

goog.require('Blockly.tuby');


Blockly.tuby['procedures_defreturn'] = function(block) {
  // Define a procedure with a return value.
  var funcName = Blockly.tuby.variableDB_.getName(
      block.getFieldValue('NAME'), Blockly.Procedures.NAME_TYPE);
  var branch = Blockly.tuby.statementToCode(block, 'STACK');
  if (Blockly.tuby.STATEMENT_PREFIX) {
    branch = Blockly.tuby.prefixLines(
        Blockly.tuby.STATEMENT_PREFIX.replace(/%1/g,
        '\'' + block.id + '\''), Blockly.tuby.INDENT) + branch;
  }
  if (Blockly.tuby.INFINITE_LOOP_TRAP) {
    branch = Blockly.tuby.INFINITE_LOOP_TRAP.replace(/%1/g,
        '\'' + block.id + '\'') + branch;
  }
  var returnValue = Blockly.tuby.valueToCode(block, 'RETURN',
      Blockly.tuby.ORDER_NONE) || '';
  if (returnValue) {
    returnValue = '  return ' + returnValue + ';\n';
  }
  var args = [];
  for (var x = 0; x < block.arguments_.length; x++) {
    args[x] = Blockly.tuby.variableDB_.getName(block.arguments_[x],
        Blockly.Variables.NAME_TYPE);
  }
  var code = 'function ' + funcName + '(' + args.join(', ') + ') {\n' +
      branch + returnValue + '}';
  code = Blockly.tuby.scrub_(block, code);
  Blockly.tuby.definitions_[funcName] = code;
  return null;
};

// Defining a procedure without a return value uses the same generator as
// a procedure with a return value.
Blockly.tuby['procedures_defnoreturn'] =
    Blockly.tuby['procedures_defreturn'];

Blockly.tuby['procedures_callreturn'] = function(block) {
  // Call a procedure with a return value.
  var funcName = Blockly.tuby.variableDB_.getName(
      block.getFieldValue('NAME'), Blockly.Procedures.NAME_TYPE);
  var args = [];
  for (var x = 0; x < block.arguments_.length; x++) {
    args[x] = Blockly.tuby.valueToCode(block, 'ARG' + x,
        Blockly.tuby.ORDER_COMMA) || 'null';
  }
  var code = funcName + '(' + args.join(', ') + ')';
  return [code, Blockly.tuby.ORDER_FUNCTION_CALL];
};

Blockly.tuby['procedures_callnoreturn'] = function(block) {
  // Call a procedure with no return value.
  var funcName = Blockly.tuby.variableDB_.getName(
      block.getFieldValue('NAME'), Blockly.Procedures.NAME_TYPE);
  var args = [];
  for (var x = 0; x < block.arguments_.length; x++) {
    args[x] = Blockly.tuby.valueToCode(block, 'ARG' + x,
        Blockly.tuby.ORDER_COMMA) || 'null';
  }
  var code = funcName + '(' + args.join(', ') + ');\n';
  return code;
};

Blockly.tuby['procedures_ifreturn'] = function(block) {
  // Conditionally return value from a procedure.
  var condition = Blockly.tuby.valueToCode(block, 'CONDITION',
      Blockly.tuby.ORDER_NONE) || 'false';
  var code = 'if (' + condition + ') {\n';
  if (block.hasReturnValue_) {
    var value = Blockly.tuby.valueToCode(block, 'VALUE',
        Blockly.tuby.ORDER_NONE) || 'null';
    code += '  return ' + value + ';\n';
  } else {
    code += '  return;\n';
  }
  code += '}\n';
  return code;
};

Blockly.tuby['procedures_expresion'] = function(block) {
  var statements_do = Blockly.tuby.statementToCode(block, 'expresion');
  statements_do = Blockly.tuby.addLoopTrap(statements_do, block.id);
  var statements_nom = Blockly.tuby.statementToCode(block, 'expresion');
  statements_nom = Blockly.tuby.addLoopTrap(statements_do, block.id);
  // TODO: Assemble tuby into code variable.
  var code = '(' + statements_nom + ')';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.tuby.ORDER_NONE];
}; 

Blockly.tuby['procedures_express'] = function(block) {
  var statements_name = Blockly.tuby.statementToCode(block, 'NAME');
  statements_name = Blockly.tuby.addLoopTrap(statements_name, block.id);
  // TODO: Assemble tuby into code variable.
  var code = '(' + statements_name + ')';
  return code;
};

Blockly.tuby['proced_exp'] = function(block) {
  var value_expression = Blockly.tuby.valueToCode(block, 'expresion', Blockly.tuby.ORDER_ATOMIC);
  var argument1 = Blockly.tuby.valueToCode(block, 'expresion',
    Blockly.tuby.ORDER_ASSIGNMENT) || 'NULL';
  // TODO: Assemble tuby into code variable.
  var code = '('+argument1+')';
  return code;
};

Blockly.tuby['create_main'] = function(block) {
  var value_expression = Blockly.tuby.valueToCode(block, 'expression', Blockly.tuby.ORDER_ATOMIC);
  var argument0 = Blockly.tuby.valueToCode(block, 'expression',
    Blockly.tuby.ORDER_ASSIGNMENT) || 'NULL';
  // TODO: Assemble tuby into code variable.
  var code = 'int main{' + '\n' + argument0 + '\n' + '}';
  return code;
};

Blockly.tuby['procedures_main2'] = function(block) {
  var statements_name = Blockly.tuby.statementToCode(block, 'NAME');
  statements_name = Blockly.tuby.addLoopTrap(statements_name, block.id);
  // TODO: Assemble tuby into code variable.
  var code = 'principal{' + '\n' + statements_name + '\n}';
  return code;
};

Blockly.tuby['pro_exp'] = function(block) {
  var value_name = Blockly.tuby.valueToCode(block, 'NAME', Blockly.tuby.ORDER_ATOMIC);
  var argument0 = Blockly.tuby.valueToCode(block, 'NAME',
    Blockly.tuby.ORDER_ASSIGNMENT) || 'NULL';
  // TODO: Assemble tuby into code variable.
  var code = '('+argument0+')';
  return code;
};

Blockly.tuby['proc_arg'] = function(block) {
  var dropdown_tipo = block.getFieldValue('tipo');
  var text_nombre = block.getFieldValue('parametro');
  var value_arg = Blockly.tuby.valueToCode(block, 'arg', Blockly.tuby.ORDER_ATOMIC);
  // TODO: Assemble tuby into code variable.
  if(value_arg == '')
  {
    var code = dropdown_tipo + ' ' + text_nombre;
  }
  else{
    var code = dropdown_tipo + ' ' + text_nombre + ', ' + value_arg;
  }
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.tuby.ORDER_NONE];
};

Blockly.tuby['proc_arg2'] = function(block) {
  var text_nombre = block.getFieldValue('parametro');
  var value_arg = Blockly.tuby.valueToCode(block, 'arg', Blockly.tuby.ORDER_ATOMIC);
  // TODO: Assemble tuby into code variable.
  if(value_arg == '')
  {
    var code =  ' ' + text_nombre;
  }
  else{
    var code =  ' ' + text_nombre + ', ' + value_arg;
  }
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.tuby.ORDER_NONE];
};


Blockly.tuby['proc'] = function(block) {
  var dropdown_tipo = block.getFieldValue('tipo');
  var text_nombre = block.getFieldValue('nomFuncion');
  var value_name = Blockly.tuby.valueToCode(block, 'NAME', Blockly.tuby.ORDER_ATOMIC);
  var statements_stats = Blockly.tuby.statementToCode(block, 'stats');
  // TODO: Assemble tuby into code variable.
  var code = 'funcion ' + dropdown_tipo + ' ' + text_nombre + ' (' +value_name + '){\n' + statements_stats + '\n}\n';
  return code;
};

Blockly.tuby['return'] = function(block) {
  var value_returnval = Blockly.tuby.valueToCode(block, 'returnVal', Blockly.tuby.ORDER_ATOMIC);
  // TODO: Assemble tuby into code variable.
  var code = 'retorno ' + value_returnval + ';\n';
  return code;
};

Blockly.tuby['func_call'] = function(block) {
  var text_name = block.getFieldValue('NAME');
  var value_return = Blockly.tuby.valueToCode(block, 'return', Blockly.tuby.ORDER_ATOMIC);
  // TODO: Assemble tuby into code variable.
  var code = text_name + '(' + value_return + ');\n';
  return code;
};

Blockly.tuby['func_calls'] = function(block) {
  var text_name = block.getFieldValue('NAME');
  var value_return = Blockly.tuby.valueToCode(block, 'return', Blockly.tuby.ORDER_ATOMIC);
  // TODO: Assemble tuby into code variable.
  var code = text_name + '(' + value_return + ')';

  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.tuby.ORDER_NONE];
};