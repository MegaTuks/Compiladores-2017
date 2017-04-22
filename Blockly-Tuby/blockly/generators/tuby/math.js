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

goog.provide('Blockly.tuby.math');

goog.require('Blockly.tuby');


Blockly.tuby['math_number'] = function(block) {
  // Numeric value.
  var code = parseFloat(block.getFieldValue('NUM'));
  return [code, Blockly.tuby.ORDER_ATOMIC];
};

Blockly.tuby['math_arithmetic'] = function(block) {
  // Basic arithmetic operators, and power.
  var OPERATORS = {
    'ADD': [' + ', Blockly.tuby.ORDER_ADDITION],
    'MINUS': [' - ', Blockly.tuby.ORDER_SUBTRACTION],
    'MULTIPLY': [' * ', Blockly.tuby.ORDER_MULTIPLICATION],
    'DIVIDE': [' / ', Blockly.tuby.ORDER_DIVISION],
  };
  var tuple = OPERATORS[block.getFieldValue('OP')];
  var operator = tuple[0];
  var order = tuple[1];
  var argument0 = Blockly.tuby.valueToCode(block, 'A', order) || '0';
  var argument1 = Blockly.tuby.valueToCode(block, 'B', order) || '0';
  var code;
  // Power in tuby requires a special case since it has no operator.
  if (!operator) {
    code = 'Math.pow(' + argument0 + ', ' + argument1 + ')';
    return [code, Blockly.tuby.ORDER_FUNCTION_CALL];
  }
  code = argument0 + operator + argument1;
  return [code, order];
};

Blockly.tuby['math_arithmetic_par'] = function(block) {
  // Basic arithmetic operators, and power.
  var OPERATORS = {
    'ADD': [' + ', Blockly.tuby.ORDER_ADDITION],
    'MINUS': [' - ', Blockly.tuby.ORDER_SUBTRACTION],
    'MULTIPLY': [' * ', Blockly.tuby.ORDER_MULTIPLICATION],
    'DIVIDE': [' / ', Blockly.tuby.ORDER_DIVISION],
  };
  var tuple = OPERATORS[block.getFieldValue('OP')];
  var operator = tuple[0];
  var order = tuple[1];
  var argument0 = Blockly.tuby.valueToCode(block, 'A', order) || '0';
  var argument1 = Blockly.tuby.valueToCode(block, 'B', order) || '0';
  var code;
  // Power in tuby requires a special case since it has no operator.
  if (!operator) {
    code = 'Math.pow(' + '(' + argument0 + ', ' + argument1 + ')' + ')';
    return [code, Blockly.tuby.ORDER_FUNCTION_CALL];
  }
  code = '(' + argument0 + operator + argument1 + ')';
  return [code, order];
};



Blockly.tuby['math_modulo'] = function(block) {
  // Remainder computation.
  var argument0 = Blockly.tuby.valueToCode(block, 'DIVIDEND',
      Blockly.tuby.ORDER_MODULUS) || '0';
  var argument1 = Blockly.tuby.valueToCode(block, 'DIVISOR',
      Blockly.tuby.ORDER_MODULUS) || '0';
  var code = argument0 + ' % ' + argument1;
  return [code, Blockly.tuby.ORDER_MODULUS];
};



