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

goog.provide('Blockly.tuby.logic');

goog.require('Blockly.tuby');


Blockly.tuby['controls_if'] = function(block) {
  // If/elseif/else condition.
  var n = 0;
  var argument = Blockly.tuby.valueToCode(block, 'IF' + n,
      Blockly.tuby.ORDER_NONE) || 'falso';
  var branch = Blockly.tuby.statementToCode(block, 'DO' + n);
  var code = 'si (' + argument + ') {\n' + branch + '\n}\n';
  for (n = 1; n <= block.elseifCount_; n++) {
    argument = Blockly.tuby.valueToCode(block, 'IF' + n,
        Blockly.tuby.ORDER_NONE) || 'falso';
    branch = Blockly.tuby.statementToCode(block, 'DO' + n);
    code += ' else if (' + argument + ') {\n' + branch + '}';
  }
  if (block.elseCount_) {
    branch = Blockly.tuby.statementToCode(block, 'ELSE');
    code += ' sino {\n' + branch + '\n}';
  }
  return code + '\n';
};

Blockly.tuby['logic_compare'] = function(block) {
  // Comparison operator.
  var OPERATORS = {
    'EQ': '~',
    'LT': '<',
    'GT': '>'
  };
  var operator = OPERATORS[block.getFieldValue('OP')];
  var order = (operator == '~') ?
      Blockly.tuby.ORDER_EQUALITY : Blockly.tuby.ORDER_RELATIONAL;
  var argument0 = Blockly.tuby.valueToCode(block, 'A', order) || '0';
  var argument1 = Blockly.tuby.valueToCode(block, 'B', order) || '0';
  var code = argument0 + ' ' + operator + ' ' + argument1;
  return [code, order];
};

Blockly.tuby['logic_operation'] = function(block) {
  // Operations 'and', 'or'.
  var operator = (block.getFieldValue('OP') == 'AND') ? '&&' : '||';
  var order = (operator == '&&') ? Blockly.tuby.ORDER_LOGICAL_AND :
      Blockly.tuby.ORDER_LOGICAL_OR;
  var argument0 = Blockly.tuby.valueToCode(block, 'A', order);
  var argument1 = Blockly.tuby.valueToCode(block, 'B', order);
  if (!argument0 && !argument1) {
    // If there are no arguments, then the return value is false.
    argument0 = 'falso';
    argument1 = 'falso';
  } else {
    // Single missing arguments have no effect on the return value.
    var defaultArgument = (operator == '&&') ? 'verdadero' : 'falso';
    if (!argument0) {
      argument0 = defaultArgument;
    }
    if (!argument1) {
      argument1 = defaultArgument;
    }
  }
  var code = argument0 + ' ' + operator + ' ' + argument1;
  return [code, order];
};

Blockly.tuby['logic_negate'] = function(block) {
  // Negation.
  var order = Blockly.tuby.ORDER_LOGICAL_NOT;
  var argument0 = Blockly.tuby.valueToCode(block, 'BOOL', order) ||
      'true';
  var code = '!' + argument0;
  return [code, order];
};

Blockly.tuby['logic_boolean'] = function(block) {
  // Boolean values true and false.
  var code = (block.getFieldValue('BOOL') == 'TRUE') ? 'verdadero' : 'falso';
  return [code, Blockly.tuby.ORDER_ATOMIC];
};

